
import os
from flask import Flask
from bookings import bookings_bp
from admin import admin_bp
from reviews import reviews_bp
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def debug_tables():
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📌 현재 bookings.db에 존재하는 테이블 목록:", tables)
    conn.close()


# 절대 경로 DB 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKINGS_DB_PATH = os.path.join(BASE_DIR, 'bookings.db')
ADMIN_DB_PATH = os.path.join(BASE_DIR, 'admin.db')
REVIEWS_DB_PATH = BOOKINGS_DB_PATH

# DB 경로 주입
bookings_bp.db_path = BOOKINGS_DB_PATH
admin_bp.db_path = ADMIN_DB_PATH
reviews_bp.db_path = REVIEWS_DB_PATH

# 블루프린트 등록
app.register_blueprint(bookings_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(reviews_bp)

app.config['REVIEWS_DB_PATH'] = BOOKINGS_DB_PATH

if __name__ == '__main__':
    app.run(debug=True)
