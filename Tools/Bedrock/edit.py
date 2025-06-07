from mitmproxy import http
import json

def config():
    with open('api.json', 'r') as fp:
        config = json.loads(fp) 
        amount = config['amount']
        return amount

def request(flow: http.HTTPFlow):
    if flow.request.pretty_url.endswith(".png" or ".jpeg" or ".jpg") or "img" or "image" in flow.request.pretty_url:
        flow.request.pretty_url = "https://mario.wiki.gallery/images/thumb/d/d6/Captain_toad_powerstar.png/1200px-Captain_toad_powerstar.png"

def response(flow: http.HTTPFlow, amount):
    amount = config()

    if "https://api.bedrocklearning.org/api/students" and "dashboard" in flow.request.pretty_url:
        print(f"Found URL: {flow.request.pretty_url}")

        items = ['points', 'pointsWeek', 'time', 'timeweek']

        response_text = flow.response.content.decode('utf-8')
        data = json.loads(response_text)

        data['firstname'] = f"{data['firstname']} (StarTools Running)"

        for item in items:
            data[item] = amount
            print(f"Changed {item} to {amount}")


        json.dumps(data).encode('utf-8')

        

