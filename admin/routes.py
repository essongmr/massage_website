# TODO: Add routes for admin
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
import bcrypt
import io
import xlsxwriter
from datetime import datetime
from . import admin_bp
from bookings import bookings_bp


# admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(admin_bp.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admins WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            session['logged_in'] = True
            return redirect(url_for('admin.admin_home'))
        else:
            error = '아이디 또는 비밀번호가 올바르지 않습니다.'

    return render_template('login.html', error=error)

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
def admin_home():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))
    return render_template('admin_home.html')

@admin_bp.route('/reviews')
def admin_reviews():
  
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    conn = sqlite3.connect(current_app.config['REVIEWS_DB_PATH'])
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, content, rating, is_public FROM reviews ORDER BY created_at DESC")
    reviews = cursor.fetchall()
    conn.close()

    return render_template('admin_review.html', reviews=reviews)

@admin_bp.route('/reservations')
def admin_reservations():
    
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    conn = sqlite3.connect(bookings_bp.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations ORDER BY id DESC")
    all_reservations = cursor.fetchall()
    conn.close()

    # 페이지네이션 설정
    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(all_reservations)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page

    return render_template('admin_reservations.html',
                           reservations=all_reservations,
                           page=page,
                           total_pages=total_pages,
                           start=start,
                           end=end)

    return render_template('admin_reservations.html', reservations=reservations)
