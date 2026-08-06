from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Ваши данные (они уже есть в вашем проекте)
BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"
ADMIN_ID = "6305430094"

@app.route('/')
def index():
    # Возвращаем красивую визитку
    return render_template('dashboard.html')

@app.route('/api/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    stars = data.get('stars')
    username = data.get('username')

    # Отправляем уведомление в Telegram
    message = f"🛒 **НОВЫЙ ЗАКАЗ С САЙТА!**\n\n⭐ Количество: {stars}\n👤 Получатель: @{username}"
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_ID, "text": message, "parse_mode": "Markdown"}
        )
        return {"status": "ok"}
    except:
        return {"status": "error"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)