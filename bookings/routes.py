# TODO: Add routes for bookings
import sqlite3
from flask import Blueprint, render_template, request, redirect
from . import bookings_bp
from datetime import datetime, timedelta, time as dtime
from flask import flash

# bookings_bp = Blueprint('bookings', __name__, url_prefix='/')

@bookings_bp.route('/')
def home():
    return render_template('index.html')

@bookings_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date_str = request.form['date']
        time_str = request.form['time']
        password = request.form['password']
        code = phone[-4:] + password

        # ▶ 날짜와 시간 문자열을 datetime으로 변환
        try:
            reserved_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            return "잘못된 날짜/시간 형식입니다."

        now = datetime.now()

        # ✅ [1] 과거 시간 금지
        if reserved_dt <= now:
            return "과거 시간은 예약할 수 없습니다."

        # ✅ [2] 현재 시점 기준 1시간 이내 금지
        if reserved_dt <= now + timedelta(hours=1):
            return "1시간 이내의 예약은 전화로 문의해주세요."

        # ✅ [3] 운영시간 체크: 오전 10시 ~ 익일 4시까지만 허용
        reservation_time = reserved_dt.time()
        if not (dtime(10, 0) <= reservation_time or reservation_time < dtime(4, 0)):
            return "예약은 오전 10시부터 익일 오전 4시까지만 가능합니다."

        # ▶ 예약 저장
        conn = sqlite3.connect(bookings_bp.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reservations (name, phone, date, time, code, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, phone, date_str, time_str, code, password))
        conn.commit()
        conn.close()

         # ✅ 예약번호는 표시하지 않고 안내 메시지만 전달
        return render_template('thanks.html', name=name, phone=phone)

    return render_template('reserve.html')


@bookings_bp.route('/modify_lookup', methods=['GET', 'POST'])
def modify_lookup():
    error = None
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = sqlite3.connect(bookings_bp.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE phone=? AND password=?", (phone, password))
        reservation = cursor.fetchone()
        conn.close()

        if reservation:
            return redirect(f"/modify/{reservation[5]}")
        else:
            error = "일치하는 예약이 없습니다. 전화번호와 비밀번호를 확인하세요."

    return render_template('modify_lookup.html', error=error)

@bookings_bp.route('/modify/<code>', methods=['GET', 'POST'])
def modify(code):
    conn = sqlite3.connect(bookings_bp.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE code=?", (code,))
    reservation = cursor.fetchone()

    if not reservation:
        return "<h3>해당 예약을 찾을 수 없습니다.</h3>"

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update':
            new_date = request.form['date']
            new_time = request.form['time']
            cursor.execute("UPDATE reservations SET date=?, time=? WHERE code=?", (new_date, new_time, code))
            conn.commit()
            conn.close()
            return f"<h3>예약이 변경되었습니다! 새로운 예약: {new_date} {new_time}</h3><a href='/'>홈으로</a>"
        elif action == 'cancel':
            cursor.execute("DELETE FROM reservations WHERE code=?", (code,))
            conn.commit()
            conn.close()
            return "<h3>예약이 취소되었습니다.</h3><a href='/'>홈으로</a>"

    conn.close()
    return render_template('modify.html', reservation=reservation)
