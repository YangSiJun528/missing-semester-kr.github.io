"""Check the real candidate against deterministic success, 404, and bad anchors."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import tempfile
import threading


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'<html><body><h1 id="present">Fixture</h1></body></html>'
        self.send_response(200 if self.path == "/page" else 404)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
results = []
try:
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory) / "input.html"
        for path, expected in [("/page#present", 0), ("/missing", 2), ("/page#absent", 2)]:
            fixture.write_text(f'<a href="http://127.0.0.1:{server.server_port}{path}">Test</a>')
            result = subprocess.run(["lychee", "--config", ".lychee.toml", str(fixture)],
                                    capture_output=True, text=True, timeout=30)
            row = {"path": path, "exit": result.returncode, "expected": expected,
                   "output": result.stdout + result.stderr}
            results.append(row)
            print(json.dumps(row), flush=True)
finally:
    server.shutdown()
    server.server_close()
Path("lychee-controls.json").write_text(json.dumps(results, indent=2) + "\n")
assert all(r["exit"] == r["expected"] for r in results), "Candidate rejected valid links or accepted broken links"
assert "404" in results[1]["output"]
assert "absent" in results[2]["output"]
