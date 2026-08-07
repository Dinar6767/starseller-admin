import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    if not DATABASE_URL:
        print("❌ DATABASE_URL не найден! Проверьте переменные на Railway.")
        return
    
    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    cur = conn.cursor()
    
    # Создаём таблицу заказов в PostgreSQL
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT,
            username TEXT,
            amount INTEGER,
            payment_status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Проверяем, есть ли уже заказы
    cur.execute('SELECT COUNT(*) FROM orders')
    count = cur.fetchone()[0]
    
    if count == 0:
        cur.execute(
            'INSERT INTO orders (chat_id, username, amount, payment_status) VALUES (%s, %s, %s, %s)',
            (6305430094, 'crdkl', 50, 'pending')
        )
        print("✅ Добавлен тестовый заказ в PostgreSQL!")
    
    conn.commit()
    conn.close()
    print("✅ База данных PostgreSQL инициализирована!")

if __name__ == "__main__":
    init_db()