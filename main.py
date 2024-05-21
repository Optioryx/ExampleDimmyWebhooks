from flask import Flask, request
import requests
from svix.webhooks import Webhook

app = Flask(__name__)
secret = "<WEBHOOK SIGNING SECRET>"
dimmy_api_key = "<DIMMY API KEY>"
dimmy_api_url = "https://dimmy.api.optioryx.com"

@app.route('/webhook', methods=['POST'])
def hook():
    headers = request.headers
    payload = request.data

    wh = Webhook(secret)
    payload = wh.verify(payload, headers)

    for id in payload["item_ids"]:
        res = requests.get(f"{dimmy_api_url}/items/{id}", headers={"X-API-KEY": dimmy_api_key})
        print(id, res.json())

    return "OK"

if __name__ == '__main__':
    app.run()