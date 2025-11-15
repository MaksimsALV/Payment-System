from datetime import datetime, timezone

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
        id, product_name, is_paid, amount, currency, quantity, customer_email, created_at_utc, updated_at_utc)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
        responseJson["id"],
        payload["product_name"],
        responseJson["payment_status"] == "paid",
        payload["amount"] / 100,
        payload["currency"].upper(),
        payload["quantity"],
        payload["customer_email"],
        datetime.utcnow(),
        datetime.utcnow()
    ))
    conn.commit()
    cursor.close()
    conn.close()