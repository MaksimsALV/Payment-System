from datetime import datetime, timezone
from random import random

import psycopg2

def insertOrder(payload, responseJson):
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="payment_system",
        user="postgres",
        password="root"
    )

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public.orders (
        id, product_name, payment_status, amount, currency, quantity, customer_email, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
        responseJson["id"],
        payload["product_name"],
        responseJson["payment_status"],
        payload["amount"],
        payload["currency"].upper(),
        payload["quantity"],
        payload["customer_email"],
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
    ))
    conn.commit()
    cursor.close()
    conn.close()