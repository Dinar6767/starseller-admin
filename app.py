from flask import Flask, render_template, request
import requests
import sqlite3
import os

app = Flask(__name__)

# --- ТОКЕН ОСНОВНОГО БОТА (StarSeller) ---
BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"
ADMIN_ID = "6305430094"

# --- ПУТЬ К БАЗЕ ДАННЫХ ---
# Вставьте тот путь, который вы нашли в консоли (скорее всего /app/db.sqlite3)
DB_PATH = "/app/db.sqlite3"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # Заказы со статусом "pending"
    orders = conn.execute(
        'SELECT rowid, chat_id, username, amount, payment_status FROM orders WHERE payment_status = "pending" ORDER BY rowid DESC'
    ).fetchall()
    conn.close()
    return render_template('dashboard.html', orders=orders)

@app.route('/api/confirm_order', methods=['POST'])
def confirm_order_api():
    data = request.get_json()
    order_id = data.get('order_id')
    chat_id = data.get('chat_id')
    username = data.get('username')
    amount = data.get('amount')

    # Отправляем клиенту сообщение в Telegram через ОСНОВНОГО бота
    client_message = (
        f"🎉 **Заказ #{order_id} подтверждён!**\n"
        f"⭐ {amount} звёзд зачислены на @{username}\n"
        f"🚀 Спасибо за покупку! Желаем удачи!"
    )
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": client_message, "parse_mode": "Markdown"}
    )

    # Обновляем статус заказа в базе
    conn = get_db_connection()
    conn.execute('UPDATE orders SET payment_status = "completed" WHERE rowid = ?', (order_id,))
    conn.commit()
    conn.close()

    # Отправляем админу уведомление
    admin_message = f"✅ Заказ #{order_id} подтверждён через сайт!"
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": ADMIN_ID, "text": admin_message}
    )

    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)