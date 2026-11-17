#!/usr/bin/env python3
"""Compare curl and Lychee on identical URLs without changing production settings."""
import argparse
import concurrent.futures
from html import escape
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from urllib.parse import urlsplit

from network_probe import UA, content_info, emit, safe_headers

TARGETS = [
    ("sipb", "https://sipb.mit.edu/"),
    ("sipb-iap", "https://sipb.mit.edu/iap/2019/"),
    ("naver", "https://terms.naver.com/entry.nhn?docId=856345&cid=50376&categoryId=50376"),
    ("velog", "https://velog.io/@slaslaya/Semantic-Versioning-2.0.0-MAJOR-MINOR-PATCH%EC%99%80-%EB%AA%85%EC%84%B8%EC%97%90-%EA%B4%80%ED%95%98%EC%97%AC"),
    ("fosstodon", "https://fosstodon.org/@jonhoo/116098318361854057"),
    ("openuserjs", "https://openuserjs.org/#footer"),
]
ROOT = Path(__file__).resolve().parents[2]


def sanitize(text):
    for key, value in os.environ.items():
        if value and (key.lower().endswith("_proxy") or key in ("GITHUB_TOKEN", "GH_TOKEN")):
            text = text.replace(value, "<REDACTED>")
    return text


def run(command):
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=40)
        row = {"exit": result.returncode, "stdout": sanitize(result.stdout), "stderr": sanitize(result.stderr)}
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
        row = {"exit": 124, "stdout": sanitize(decode(error.stdout)),
               "stderr": sanitize(decode(error.stderr)), "deadline": True}
    row["seconds"] = round(time.monotonic() - started, 3)
    return row


def compare(target):
    name, url = target
    rows = []
    with tempfile.TemporaryDirectory(prefix="issue40-clients-") as directory:
        folder = Path(directory)
        fixture, body, headers = folder / "fixture.html", folder / "body", folder / "headers"
        fixture.write_text(f'<!doctype html><html><body><a href="{escape(url, quote=True)}">probe</a></body></html>')
        result = run(["curl", "-sS", "-L", "--compressed", "-H", "Accept-Encoding: gzip", "-A", UA,
                      "--connect-timeout", "10", "--max-time", "30", "--max-redirs", "8",
                      "--max-filesize", "2097152", "-D", str(headers), "-o", str(body), "-w", "%{json}", url])
        try:
            info = json.loads(result["stdout"])
            del result["stdout"]
        except ValueError:
            info = {}
        raw_headers = headers.read_text(errors="replace") if headers.exists() else ""
        selected = safe_headers(line.split(": ", 1) for line in raw_headers.splitlines() if ": " in line)
        text = body.read_text(errors="replace") if body.exists() else ""
        result.update(target=name, url=url, client="curl-frozen-gzip", status=info.get("http_code"),
                      effective_url=info.get("url_effective"), remote_ip=info.get("remote_ip"),
                      http_version=info.get("http_version"), bytes=info.get("size_download"),
                      headers=selected, response_statuses=[x for x in raw_headers.splitlines() if x.startswith("HTTP/")],
                      timings={key: info.get(key) for key in ("time_namelookup", "time_connect", "time_appconnect",
                               "time_starttransfer", "time_total")}, **content_info(text, url, selected))
        rows.append(result)
        emit(result)
        for label, arguments in (("lychee-default", []), ("lychee-frozen", ["--user-agent", UA])):
            time.sleep(15 if name == "openuserjs" else 2)
            result = run(["lychee", "--config", str(ROOT / ".lychee.toml"), "--no-progress",
                          "--max-concurrency", "1", "--host-concurrency", "1", "--timeout", "30",
                          "--max-retries", "0", "--include-fragments=anchor-only", "--format", "json",
                          *arguments, str(fixture)])
            result.update(target=name, url=url, client=label)
            try:
                result["report"] = json.loads(result["stdout"])
                del result["stdout"]
            except ValueError:
                pass
            rows.append(result)
            emit(result)
    return rows


def compare_host(targets):
    rows = []
    for index, target in enumerate(targets):
        if index:
            time.sleep(2)
        rows.extend(compare(target))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("client-results"))
    parser.add_argument("--label", default="unspecified")
    args = parser.parse_args()
    metadata = {"label": args.label, "platform": platform.platform(),
                "curl": run(["curl", "--version"])["stdout"].strip(),
                "lychee": run(["lychee", "--version"])["stdout"].strip()}
    emit({"kind": "metadata", **metadata})
    hosts = {}
    for target in TARGETS:
        hosts.setdefault(urlsplit(target[1]).hostname, []).append(target)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = [row for group in pool.map(compare_host, hosts.values()) for row in group]
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps({"metadata": metadata, "requests": rows}, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
