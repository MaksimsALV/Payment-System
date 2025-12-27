import threading
from src.API.endpoints.getTransactionStatus import run_forever
from src.API.endpoints.postCheckout import app

if __name__ == "__main__":
    # start Stripe status polling in background
    threading.Thread(target=run_forever, daemon=True).start()

    # start Flask in main thread
    app.run(host="127.0.0.1", port=5000)