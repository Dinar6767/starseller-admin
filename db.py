import os
import psycopg2
from urllib.parse import urlparse

# Берём URL базы данных из переменной окружения (на Railway она называется DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        raise Exception("❌ DATABASE_URL не найден! Проверьте переменные на Railway.")
    
    # Парсим URL для psycopg2
    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    return conn

def get_all_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, amount, chat_id, payment_status FROM orders ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    # Преобразуем в список словарей для HTML
    orders = [{'id': r[0], 'username': r[1], 'amount': r[2], 'chat_id': r[3], 'payment_status': r[4]} for r in rows]
    return orders

def add_test_order():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO orders (chat_id, username, amount, payment_status) VALUES (%s, %s, %s, %s)',
        (6305430094, 'crdkl', 50, 'pending')
    )
    conn.commit()
    conn.close()

def update_order_status(order_id, status="completed"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE orders SET payment_status = %s WHERE id = %s', (status, order_id))
    conn.commit()
    conn.close()