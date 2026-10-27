"""Validate Fandom article identity, contents and anchors through its read-only API.

This does not claim that the ordinary HTML URL returned HTTP 200.
"""
import argparse
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import urlencode, urlsplit, unquote


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.anchors, self.text = set(), set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.add(attrs["href"])
        for key in ["id", "name"]:
            if attrs.get(key):
                self.anchors.add(attrs[key])

    def handle_data(self, data):
        self.text.append(data)


def title_for(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "vim.fandom.com" or not parsed.path.startswith("/wiki/") or parsed.query:
        raise ValueError("Unsupported URL: " + url)
    return unquote(parsed.path[len("/wiki/"):]).replace("_", " ")


class API:
    def __init__(self):
        self.requests = []
        self.parsed = {}

    def request(self, params):
        url = "https://vim.fandom.com/api.php?" + urlencode({**params, "format": "json", "formatversion": "2"})
        with tempfile.TemporaryDirectory(prefix="fandom-api-") as tmp:
            body_path, headers_path = Path(tmp) / "body", Path(tmp) / "headers"
            command = ["curl", "-sS", "--location", "--connect-timeout", "30", "--max-time", "120",
                       "--user-agent", "MissingSemesterLinkDiagnostics/1.0 (+https://github.com/YangSiJun528/missing-semester-kr.github.io)",
                       "--dump-header", str(headers_path), "--output", str(body_path), "--write-out", "%{json}", url]
            response = subprocess.run(command, capture_output=True, text=True, timeout=130)
            metrics = json.loads(response.stdout)
            body = body_path.read_bytes() if body_path.exists() else b""
            headers = headers_path.read_text(errors="replace") if headers_path.exists() else ""
            headers = "\n".join("Set-Cookie: [redacted]" if line.lower().startswith("set-cookie:") else line for line in headers.splitlines())
            record = {"url": url, "headers": headers, "exit_code": response.returncode, "stderr": response.stderr,
                      "body_sha256": hashlib.sha256(body).hexdigest(), "body_bytes": len(body),
                      "metrics": {k: metrics.get(k) for k in ["http_code", "url_effective", "remote_ip", "time_namelookup", "time_connect", "time_appconnect", "time_starttransfer", "time_total"]}}
            self.requests.append(record)
            if response.returncode or metrics.get("http_code") != 200:
                raise RuntimeError("API request failed: " + json.dumps(record))
            data = json.loads(body)
            if "error" in data:
                raise RuntimeError("API returned an error: " + json.dumps(data["error"]))
            return data

    def load(self, urls):
        titles = sorted({title_for(url) for url in urls})
        if len(titles) > 50:
            raise ValueError("This experiment supports at most 50 article titles")
        data = self.request({"action": "query", "prop": "info", "inprop": "url", "titles": "|".join(titles)})
        self.pages = {p["title"]: p for p in data["query"]["pages"]}

    def validate(self, url):
        title = title_for(url)
        page = self.pages.get(title)
        result = {"url": url, "valid": False}
        if page is None or page.get("missing") or page.get("invalid"):
            return {**result, "reason": "missing_page"}
        pageid = page.get("pageid")
        if not isinstance(pageid, int) or pageid <= 0 or page.get("length", 0) <= 0:
            return {**result, "reason": "empty_or_invalid_page"}
        canonical = page.get("canonicalurl", "")
        if title_for(canonical) != title:
            return {**result, "reason": "canonical_url_mismatch", "canonical_url": canonical}
        if pageid not in self.parsed:
            parsed = self.request({"action": "parse", "pageid": str(pageid), "prop": "text|revid"})["parse"]
            if parsed.get("pageid") != pageid or parsed.get("title") != title:
                raise RuntimeError("Parse response does not identify the expected article")
            document = Document()
            document.feed(parsed["text"])
            self.parsed[pageid] = (parsed, document)
        parsed, document = self.parsed[pageid]
        text_length = len("".join(document.text).strip())
        if not text_length:
            return {**result, "reason": "empty_article"}
        fragment = unquote(urlsplit(url).fragment)
        details = {"canonical_url": canonical, "pageid": pageid, "revision_id": parsed.get("revid"),
                   "article_characters": text_length, "fragment": fragment, "anchor_exists": not fragment or fragment in document.anchors}
        if fragment and fragment not in document.anchors:
            return {**result, **details, "reason": "missing_anchor"}
        return {**result, **details, "valid": True, "reason": "article_and_anchor_verified_via_api"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    urls = set()
    for filename in Path(args.site).rglob("*.html"):
        document = Document()
        document.feed(filename.read_text(errors="replace"))
        urls.update(url for url in document.links if urlsplit(url).hostname == "vim.fandom.com")
    urls = sorted(urls)
    missing_page = "https://vim.fandom.com/wiki/MissingSemesterDiagnosticMissingPage_20261028_58542c5"
    missing_anchor = "https://vim.fandom.com/wiki/Using_undo_branches#MissingSemesterDiagnosticMissingAnchor_20261028_58542c5"
    api = API()
    report = {"started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "scope": "API article/anchor validation, not ordinary HTML reachability", "urls": urls, "passed": False}
    try:
        if len(urls) != 5:
            raise RuntimeError(f"Expected the five baseline Fandom URLs, found {len(urls)}")
        api.load(urls + [missing_page, missing_anchor])
        report["results"] = [api.validate(url) for url in urls]
        report["negative_controls"] = [api.validate(missing_page), api.validate(missing_anchor)]
        report["passed"] = all(r["valid"] for r in report["results"]) and [r["reason"] for r in report["negative_controls"]] == ["missing_page", "missing_anchor"] and not any(r["valid"] for r in report["negative_controls"])
    except Exception as error:
        report["error"] = str(error)
    finally:
        report["requests"] = api.requests
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({key: value for key, value in report.items() if key != "requests"}, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
