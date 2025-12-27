import http.client
import json
import urllib
from src.DB.insertOrderToDatabase import insertOrder
from src.web.shop import shop_ui


from flask import Flask, request, jsonify

HOST = "api.stripe.com"
ENDPOINT = "/v1/checkout/sessions"
AUTH_TOKEN = open(r"C:\Users\mhu\PycharmProjects\PaymentSystem\config\config.properties").read().partition("=")[2].strip().strip('"')

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded",
}

app = Flask(__name__)
app.register_blueprint(shop_ui)
@app.post("/checkout")
def checkoutEndpoint():
    payload = request.get_json()
    parameters = {
        "mode": "payment",
        "success_url": "https://b.stripecdn.com/docs-statics-srv/assets/succeeded.949bd1ab653cc1b01743b30d117d92eb.svg",
        "line_items[0][price_data][currency]": payload["currency"],
        "line_items[0][price_data][unit_amount]": payload["amount"],
        "line_items[0][quantity]": payload["quantity"],
        "line_items[0][price_data][product_data][name]": payload["product_name"],
        "customer_email": payload["customer_email"],
    }
    body = urllib.parse.urlencode(parameters)

    connect = http.client.HTTPSConnection(HOST)
    connect.request("POST", ENDPOINT, headers=headers, body=body)
    response = connect.getresponse()
    responseData = response.read().decode()
    connect.close()

    responseJson = json.loads(responseData)
    if response.status == 200:
        insertOrder(payload, responseJson)
    return jsonify(responseJson.get("url"))

app.run(host="127.0.0.1", port=5000)