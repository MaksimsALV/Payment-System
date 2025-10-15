import http.client
import json
import urllib

from flask import Flask, jsonify

HOST = "api.stripe.com"
ENDPOINT = "/v1/checkout/sessions"
AUTH_TOKEN = open(r"/config/config.properties").read().partition("=")[2].strip().strip('"')

parameters = {
    "mode": "payment",
    "success_url": "https://via.lv/test",
    "line_items[0][price_data][currency]": "eur",
    "line_items[0][price_data][unit_amount]": "1500",
    "line_items[0][quantity]": "1",
    "line_items[0][price_data][product_data][name]": "testa_produkts_abc",
    "customer_email": "maksims.ahmetovs@va.lv",
}

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded",
}

app = Flask(__name__)
@app.post("/checkout")
def checkoutEndpoint():
    body = urllib.parse.urlencode(parameters)

    connect = http.client.HTTPSConnection(HOST)
    connect.request("POST", ENDPOINT, headers=headers, body=body)
    response = connect.getresponse()
    responseData = response.read().decode()
    connect.close()

    responseJson = json.loads(responseData)
    return jsonify(responseJson.get("url"))

app.run(host="127.0.0.1", port=5000)