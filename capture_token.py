from mitmproxy import http
import os
import json
import signal

def request(flow: http.HTTPFlow):
    if "api.bedrocklearning.org/api/students" in flow.request.url:
        if flow.request.method == "GET" and "authorization" in flow.request.headers:
            token = flow.request.headers["authorization"]
            url = flow.request.url
            with open("captured.json", "w") as f:
                json.dump({"token": token, "url": url}, f)
            print(f"\nTOKEN_CAPTURED::{token}::{url}")
            os.kill(os.getppid(), signal.SIGTERM)
