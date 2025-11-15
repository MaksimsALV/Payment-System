from datetime import datetime, timezone

import psycopg2

def insertOrder():
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
        1,
        "test_product",
        None,
        100,
        "EUR",
        1,
        "maksims.ahmetovs@va.lv",
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
    ))
    conn.commit()
    cursor.close()
    conn.close()
insertOrder()