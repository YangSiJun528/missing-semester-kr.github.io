#!/usr/bin/env python3
"""Collect bounded network diagnostics; --check-baseline separately checks results."""
import argparse
import concurrent.futures
import datetime
from html import unescape
from html.parser import HTMLParser
import ipaddress
import json
import os
from pathlib import Path
import platform
import re
import socket
import subprocess
import tempfile
import threading
import time
from urllib.parse import unquote, urlsplit, urlunsplit

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.0.0 Safari/537.36"
TARGETS = {
    "warpspeed": "https://warpspeed.dev/",
    "fandom": "https://vim.fandom.com/wiki/Using_undo_branches#Persistent_undo",
    "openuserjs": "https://openuserjs.org/",
    "command-not-found": "https://command-not-found.com",
    "sipb": "https://sipb.mit.edu/",
    "openlearning": "https://openlearning.mit.edu/",
    "wikipedia": "https://ko.wikipedia.org/wiki/LaTeX",
}
HEADERS = {"server", "content-type", "content-length", "content-encoding", "transfer-encoding",
           "connection", "retry-after", "cf-mitigated", "location", "via", "x-cache"}
PRINT_LOCK = threading.Lock()


def emit(row):
    with PRINT_LOCK:
        print(json.dumps(row, ensure_ascii=False), flush=True)


def safe_url(value):
    parts = urlsplit(value)
    return urlunsplit((parts.scheme, parts.hostname or "", parts.path,
                       "REDACTED" if parts.query else "", parts.fragment))


def safe_headers(items):
    return [{"name": key.lower(), "value": safe_url(value) if key.lower() == "location" else value[:300]}
            for key, value in items if key.lower() in HEADERS]


def safe_error(value):
    for key, secret in os.environ.items():
        if key.lower().endswith("_proxy") and secret:
            value = value.replace(secret, "<PROXY_REDACTED>")
    value = re.sub(r"https?://[^\s'\"]+", lambda match: safe_url(match.group()), value)
    return re.sub(r"[^\s/@:]+:[^\s/@]+@", "<REDACTED>@", value)[:400]


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = set()

    def handle_starttag(self, tag, attrs):
        self.values.update(value for key, value in attrs if key in ("id", "name") and value)


def content_info(body, url, headers):
    title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    title = re.sub(r"\s+", " ", unescape(title.group(1))).strip()[:200] if title else None
    fragment = unquote(urlsplit(url).fragment)
    anchors = Anchors()
    anchors.feed(body)
    return {"title": title, "challenge": "cf-chl-" in body or "Just a moment" in (title or "")
            or any(h["name"] == "cf-mitigated" and h["value"] == "challenge" for h in headers),
            "parking_marker": bool(re.search(r"(?:location\s*(?:\.href)?\s*=|location\.replace\()\s*['\"]/lander", body)),
            "fragment": fragment, "fragment_exists": fragment in anchors.values if fragment else None}


def curl_probe(name, url, variant, options):
    with tempfile.TemporaryDirectory(prefix="issue40-probe-") as directory:
        body, headers = Path(directory) / "body", Path(directory) / "headers"
        command = ["curl", "-sS", "-L", "--connect-timeout", "10", "--max-time", "30",
                   "--max-filesize", "2097152", "--max-redirs", "8", "-A", UA,
                   "-D", str(headers), "-o", str(body), "-w", "%{json}", *options, url]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=35)
            info = json.loads(result.stdout) if result.stdout.strip() else {}
            code = result.returncode
            error = safe_error(info.get("errormsg") or result.stderr.strip())
        except (subprocess.TimeoutExpired, ValueError):
            info, code, error = {}, 124, "Probe deadline or invalid curl metadata"
        raw_headers = headers.read_text(errors="replace") if headers.exists() else ""
        text = body.read_text(errors="replace") if body.exists() else ""
        selected = safe_headers(line.split(": ", 1) for line in raw_headers.splitlines() if ": " in line)
        row = {"target": name, "client": "curl", "variant": variant, "url": url,
               "curl_exit": code, "error": error, "status": info.get("http_code"),
               "effective_url": safe_url(info.get("url_effective", url)),
               "remote_ip": info.get("remote_ip"), "http_version": info.get("http_version"),
               "ssl_verify_result": info.get("ssl_verify_result"), "bytes": info.get("size_download"),
               "timings": {key: info.get(key) for key in ("time_namelookup", "time_connect",
                   "time_appconnect", "time_starttransfer", "time_total")},
               "response_statuses": [line for line in raw_headers.splitlines() if line.startswith("HTTP/")],
               "headers": selected, **content_info(text, url, selected)}
        emit(row)
        return row


def cffi_probe(name, url, chrome):
    variant = "chrome" if chrome else "default"
    row = {"target": name, "client": "curl_cffi", "variant": variant, "url": url}
    try:
        from curl_cffi import requests
        started = time.monotonic()
        response = requests.get(url, headers={"User-Agent": UA}, timeout=20,
                                **({"impersonate": "chrome"} if chrome else {}))
        headers = safe_headers(response.headers.items())
        row.update(status=response.status_code, effective_url=safe_url(response.url),
                   http_version_code=int(response.http_version), remote_ip=getattr(response, "primary_ip", None),
                   seconds=round(time.monotonic() - started, 3),
                   headers=headers, bytes=len(response.content), **content_info(response.text, url, headers))
    except ImportError:
        row["skipped"] = "curl_cffi not installed"
    except Exception as error:
        row.update(error_type=type(error).__name__, curl_exit=getattr(error, "code", None), error=safe_error(str(error)))
    emit(row)
    return row


def probe_target(item, resolve_ip):
    name, url = item
    host = urlsplit(url).hostname
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        dns = {"A": sorted({x[4][0] for x in addresses if x[0] == socket.AF_INET}),
               "AAAA": sorted({x[4][0] for x in addresses if x[0] == socket.AF_INET6})}
    except OSError as error:
        dns = {"error_type": type(error).__name__}
    emit({"kind": "dns", "target": name, **dns})
    variants = [("head", ["-I"]), ("get", []), ("get-compressed", ["--compressed"])]
    if name == "warpspeed":
        variants = [("get", []), ("ipv4", ["-4"]), ("ipv6", ["-6"]),
                    ("http1.1", ["--http1.1"]), ("tls1.2", ["--tlsv1.2", "--tls-max", "1.2"])]
        if resolve_ip:
            variants.append(("resolve-ipv4", ["--resolve", f"{host}:443:{resolve_ip}"]))
    elif name == "openuserjs":
        variants = [("get", []), ("get-compressed", ["--compressed"]),
                    ("get-compressed-repeat", ["--compressed"]), ("get-repeat", [])]
    rows = []
    for index, (variant, options) in enumerate(variants):
        if index:
            time.sleep(15 if name == "openuserjs" else 2)
        rows.append(curl_probe(name, url, variant, options))
    if name in ("warpspeed", "fandom"):
        for chrome in (False, True):
            time.sleep(2)
            rows.append(cffi_probe(name, url, chrome))
    return {"target": name, "dns": dns, "requests": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--label", default="unspecified")
    parser.add_argument("--resolve-ip", type=lambda x: str(ipaddress.IPv4Address(x)))
    parser.add_argument("--check-baseline", type=Path, metavar="SUMMARY_JSON")
    args = parser.parse_args()
    if args.check_baseline:
        summary = json.loads(args.check_baseline.read_text())
        rows = [r for target in summary["targets"] for r in target["requests"]
                if r["client"] == "curl" and r["variant"] == "get"]
        failures = [r["target"] for r in rows if r["curl_exit"] != 0 or not 200 <= (r["status"] or 0) < 300
                    or r["challenge"] or r["parking_marker"] or r["fragment_exists"] is False
                    or (r["target"] == "command-not-found" and urlsplit(r["effective_url"]).hostname != "command-not-found.com")]
        emit({"kind": "baseline_verdict", "checked": len(rows), "failed": failures})
        return int(bool(failures) or len(rows) != len(TARGETS))
    if args.output is None:
        parser.error("--output is required when collecting diagnostics")
    args.output.mkdir(parents=True, exist_ok=True)
    metadata = {"label": args.label, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "platform": platform.platform(), "architecture": platform.machine(),
                "curl_version": subprocess.check_output(["curl", "--version"], text=True).strip(),
                "proxy_env_present": {key: bool(os.environ.get(key)) for key in
                    ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy")}}
    try:
        import curl_cffi
        metadata["curl_cffi_version"] = curl_cffi.__version__
        handle = curl_cffi.Curl()
        metadata["curl_cffi_libcurl"] = handle.version().decode(errors="replace")
        handle.close()
    except ImportError:
        metadata["curl_cffi_version"] = None
    emit({"kind": "metadata", **metadata})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        targets = list(pool.map(lambda item: probe_target(item, args.resolve_ip), TARGETS.items()))
    (args.output / "summary.json").write_text(json.dumps({"metadata": metadata, "targets": targets}, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
