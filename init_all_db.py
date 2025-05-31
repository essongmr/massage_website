import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOOKINGS_DB = os.path.join(BASE_DIR, 'bookings.db')
ADMIN_DB = os.path.join(BASE_DIR, 'admin.db')

# ✅ bookings.db 초기화 (reservations + reviews)
conn1 = sqlite3.connect(BOOKINGS_DB)
cursor1 = conn1.cursor()

# reservations 테이블
cursor1.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# reviews 테이블
cursor1.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    is_public INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn1.commit()
conn1.close()

# ✅ admin.db 초기화
conn2 = sqlite3.connect(ADMIN_DB)
cursor2 = conn2.cursor()

cursor2.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL
)
''')

# 기본 관리자 계정 생성 (중복 방지)
cursor2.execute("SELECT * FROM admins WHERE username = ?", ('admin',))
if not cursor2.fetchone():
    hashed_pw = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())
    cursor2.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('admin', hashed_pw))

conn2.commit()
conn2.close()

print("✅ 모든 DB 초기화 완료 (bookings.db, admin.db 포함)")