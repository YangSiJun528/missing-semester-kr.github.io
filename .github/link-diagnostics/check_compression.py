"""Compare the production HTMLProofer library with one HTTP option changed."""
import json
from pathlib import Path
import subprocess
import tempfile
import time

RUNNER = '''require "html-proofer"
options = {
  checks: ["Links"], check_external_hash: true, enforce_https: false,
  hydra: {max_concurrency: 1},
  typhoeus: {followlocation: true, connecttimeout: 10, timeout: 30,
    headers: {"User-Agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.0.0 Safari/537.36"}}
}
options[:typhoeus][:accept_encoding] = "" if ENV["COMPRESSED"] == "true"
HTMLProofer.check_file("/fixture/index.html", options).run
'''

results = []
for name, compressed, fragment, expected in [
    ("baseline", False, "footer", 1),
    ("compressed", True, "footer", 0),
    ("missing-fragment", True, "issue40-missing-fragment", 1),
]:
    if results:
        time.sleep(15)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "check.rb").write_text(RUNNER)
        (root / "index.html").write_text(
            f'<html lang="en"><body><a href="https://openuserjs.org/#{fragment}">OpenUserJS</a></body></html>')
        command = ["docker", "run", "--rm", "--entrypoint", "ruby",
                   "-v", f"{root}:/fixture:ro", "-e", f"COMPRESSED={str(compressed).lower()}",
                   "anishathalye/proof-html:2.2.5", "/fixture/check.rb"]
        start = time.monotonic()
        result = subprocess.run(command, capture_output=True, text=True, timeout=90)
        row = {"name": name, "exit": result.returncode, "expected": expected,
               "seconds": round(time.monotonic() - start, 2), "output": result.stdout + result.stderr}
        results.append(row)
        print(json.dumps(row), flush=True)

Path("compression-results.json").write_text(json.dumps(results, indent=2) + "\n")
assert all(r["exit"] == r["expected"] for r in results), "Compression comparison failed"
assert "time out" in results[0]["output"], "Baseline failed for another reason"
assert "issue40-missing-fragment" in results[2]["output"], "Negative control did not check the anchor"
