import sqlite3
import os

# Путь к базе данных (в этой же папке)
DB_PATH = "site_db.sqlite3"

def init_db():
    """Создаёт таблицу orders, если её нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создаём таблицу заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            username TEXT,
            amount INTEGER,
            payment_status TEXT DEFAULT 'pending'
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ База данных создана: {DB_PATH}")

# Если запускаем этот файл напрямую, создаём БД
if __name__ == "__main__":
    init_db()