from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StarSeller Админ-панель</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0d0e1a;
            color: #fff;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #7a42f4;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
        }
        .order-card {
            background: #1a1c2e;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            border-left: 4px solid #7a42f4;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .order-info { display: flex; flex-direction: column; gap: 6px; }
        .order-id { font-weight: bold; color: #7a42f4; }
        .btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
        }
        .btn:hover { background: #218838; }
    </style>
</head>
<body>
    <h1>📦 StarSeller Админ-панель</h1>
    <p style="color: #a0a3bd;">✅ Сайт успешно запущен! Вот тестовый заказ:</p>

    <div class="order-card">
        <div class="order-info">
            <div class="order-id">Тестовый заказ #1</div>
            <div>👤 @crdkl</div>
            <div>⭐ 50 звёзд</div>
        </div>
        <button class="btn" onclick="alert('✅ Тестовая кнопка сработала!')">Подтвердить</button>
    </div>

    <p style="color: #a0a3bd; margin-top: 20px;">Для работы с настоящей базой данных добавьте код позже.</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)