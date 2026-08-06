from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Автоматический поиск базы данных (работает и на компе, и на Railway)
# Ищем db.sqlite3 в текущей папке или на уровень выше
def find_db():
    possible_paths = [
        "db.sqlite3",                      # в текущей папке
        "../db.sqlite3",                   # на уровень выше (рядом с ботом)
        "/app/db.sqlite3",                 # внутри контейнера Railway
        os.path.join(os.path.dirname(__file__), "db.sqlite3")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    # Если не нашли, просто возвращаем путь, где должна быть база (для ошибки)
    return "db.sqlite3"

DB_PATH = find_db()
print(f"✅ Подключена база данных: {DB_PATH}")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        # Ищем таблицу orders. Если у вас она называется по-другому, поменяйте название
        orders = conn.execute('SELECT rowid, * FROM orders ORDER BY rowid DESC').fetchall()
        conn.close()
        return render_template('dashboard.html', orders=orders)
    except Exception as e:
        return f"❌ Ошибка при загрузке: {str(e)}"

@app.route('/confirm/<int:order_id>')
def confirm_order(order_id):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE rowid = ?', ('completed', order_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/reject/<int:order_id>')
def reject_order(order_id):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE rowid = ?', ('canceled', order_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        new_price = request.form.get('price')
        print(f"Цена обновлена до: {new_price}")
        return redirect(url_for('index'))
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)