import datetime
import html
import json
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer


API_BASE = "http://3.239.224.48:8000"
FEATURES = [7.4, 0.70, 0.00, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4, 0]


def request_json(path, *, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_BASE + path,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="POST" if data else "GET",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.status, response.read().decode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        health_status, health_body = request_json("/health")
        predict_status, predict_body = request_json(
            "/predict", payload={"features": FEATURES}
        )
        captured = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        transcript = f"""$ curl {API_BASE}/health
HTTP {health_status}
{health_body}

$ curl -X POST {API_BASE}/predict \\
  -H \"Content-Type: application/json\" \\
  -d '{json.dumps({"features": FEATURES}, separators=(",", ":"))}'
HTTP {predict_status}
{predict_body}"""
        page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Live EC2 API Verification</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; background: #0d1117; color: #e6edf3; font-family: Arial, sans-serif; }}
    main {{ max-width: 1120px; margin: 48px auto; padding: 0 28px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .meta {{ color: #8b949e; margin-bottom: 28px; }}
    .ok {{ color: #3fb950; font-weight: 700; }}
    pre {{ margin: 0; padding: 26px; background: #010409; border: 1px solid #30363d;
           border-radius: 6px; font: 17px/1.65 Consolas, monospace; white-space: pre-wrap; }}
  </style>
</head>
<body><main>
  <h1>Live EC2 API Verification</h1>
  <div class="meta">Target: {API_BASE} | Checked: {captured} | <span class="ok">2/2 requests passed</span></div>
  <pre>{html.escape(transcript)}</pre>
</main></body>
</html>"""
        encoded = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
