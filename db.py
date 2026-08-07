import sqlite3
import os

# Путь к базе данных
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

def get_db_connection():
    """Создаёт и возвращает подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_orders():
    """Возвращает список всех заказов из БД"""
    conn = get_db_connection()
    orders = conn.execute(
        'SELECT id, username, amount, chat_id, payment_status FROM orders ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return orders

def update_order_status(order_id, status="completed"):
    """Обновляет статус заказа в БД"""
    conn = get_db_connection()
    conn.execute('UPDATE orders SET payment_status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()