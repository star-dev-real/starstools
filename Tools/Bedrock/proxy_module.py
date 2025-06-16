import json
from mitmproxy import http

class ProxyModifier:
    def __init__(self, state):
        self.state = state

    def request(self, flow: http.HTTPFlow):
        pass

    def response(self, flow: http.HTTPFlow):
        if not flow.response or not flow.request:
            return
        url = flow.request.pretty_url

        if "api.bedrocklearning.org/api/students" in url and "dashboard" in url:
            try:
                data = json.loads(flow.response.content.decode("utf-8"))
                data["firstname"] = f"{data.get('firstname', '')} (Star)"
                data["points"] = self.state["points"]
                data["pointsWeek"] = self.state["points"]
                data["time"] = self.state["time"]
                data["timeweek"] = self.state["time"]
                data["lesson"] = self.state["lesson"]
                flow.response.content = json.dumps(data).encode("utf-8")
            except:
                pass

        if "api.bedrocklearning.org/api/notifications/" in url:
            flow.response.content = json.dumps({
                "count": 999,
                "unread": 999,
                "items": []
            }).encode("utf-8")
