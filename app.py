from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# --- Ваши данные для связи с Telegram ---
# ТОКЕН ОСНОВНОГО БОТА (StarSeller)
BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"  
ADMIN_ID = "6305430094"  # Ваш Telegram ID

# --- Главная страница ---
@app.route('/')
def index():
    # Здесь вы можете передать список заказов из базы данных
    # В этом примере мы показываем тестовый заказ
    orders = [
        {
            'id': 123,
            'username': 'crdkl',
            'amount': 50,
            'chat_id': 123456789
        }
    ]
    return render_template('dashboard.html', orders=orders)

# --- API для подтверждения заказа ---
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

    # 2. Отправляем админу уведомление
    admin_message = f"✅ Заказ #{order_id} подтверждён через сайт!"
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": ADMIN_ID, "text": admin_message}
    )

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)