import http.client
import json
import time
from datetime import datetime, timezone

import psycopg2

HOST = "api.stripe.com"
AUTH_TOKEN = open(r"C:\Users\mhu\PycharmProjects\PaymentSystem\config\config.properties").read().partition("=")[2].strip().strip('"')

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded",
}

def now_utc():
    return datetime.now(timezone.utc)

def check_paidStatus_and_update():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="payment_system",
        user="postgres",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM public.orders WHERE is_paid = false;")
    ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    print(f"\n[{now_utc()}] Unpaid orders: {len(ids)}")

    for session_id in ids:
        try:
            stripe = http.client.HTTPSConnection(HOST)
            stripe.request("GET", f"/v1/checkout/sessions/{session_id}", headers=headers)
            response = stripe.getresponse()
            data = response.read().decode()
            stripe.close()

            if response.status != 200:
                print(f"[{now_utc()}] Checking {session_id} -> Stripe error {response.status}")
                time.sleep(5)
                continue

            session = json.loads(data)
            status = session.get("payment_status")

            if status == "paid":
                print(f"[{now_utc()}] Checking {session_id} -> PAID, updating DB")

                conn = psycopg2.connect(
                    host="localhost",
                    port="5432",
                    database="payment_system",
                    user="postgres",
                    password="root"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE public.orders
                    SET is_paid = true,
                        updated_at_utc = %s
                    WHERE id = %s;
                """, (now_utc(), session_id))
                conn.commit()
                cursor.close()
                conn.close()
            else:
                print(f"[{now_utc()}] Checking {session_id} | Status: {status}")

            time.sleep(2)  #delay between each API call

        except Exception as e:
            print(f"[{now_utc()}] Checking {session_id} -> ERROR: {e}")
            time.sleep(5)

def run_forever():
    while True:
        check_paidStatus_and_update()
        time.sleep(60)  #full scan runs every 1 minute

if __name__ == "__main__":
    run_forever()
