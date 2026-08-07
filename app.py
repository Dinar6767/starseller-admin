from flask import Flask, render_template, request, jsonify
import requests
import os
from db import get_all_orders, update_order_status  # 👈 Импортируем из db.py

app = Flask(__name__)

# Ваши данные для связи с Telegram
BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"
ADMIN_ID = "6305430094"

@app.route('/')
def index():
    # Берём заказы из отдельной функции db.py
    orders = get_all_orders()
    return render_template('dashboard.html', orders=orders)

@app.route('/api/confirm_order', methods=['POST'])
def confirm_order_api():
    data = request.get_json()
    order_id = data.get('order_id')
    chat_id = data.get('chat_id')
    username = data.get('username')
    amount = data.get('amount')

    # 1. Отправляем клиенту сообщение в Telegram
    client_message = (
        f"🎉 **Заказ #{order_id} подтверждён!**\n"
        f"⭐ {amount} звёзд зачислены на @{username}\n"
        f"🚀 Спасибо за покупку! Желаем удачи!"
    )
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": client_message, "parse_mode": "Markdown"}
    )

    # 2. Обновляем статус в БД через отдельную функцию
    update_order_status(order_id)

    # 3. Отправляем админу уведомление
    admin_message = f"✅ Заказ #{order_id} подтверждён через сайт!"
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": ADMIN_ID, "text": admin_message}
    )

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)