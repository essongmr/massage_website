# TODO: Add routes for reviews
import sqlite3
from flask import render_template, request, redirect
from . import reviews_bp

@reviews_bp.route('/reviews')
def show_reviews():
    conn = sqlite3.connect(reviews_bp.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, content, rating FROM reviews WHERE is_public = 1 ORDER BY created_at DESC")
    reviews = cursor.fetchall()
    conn.close()
    return render_template('review_form.html', reviews=reviews)

@reviews_bp.route('/form')
def review_form():
    return render_template('review_form.html')

@reviews_bp.route('/submit', methods=['POST'])
def submit_review():
    name = request.form['name']
    content = request.form['content']
    rating = int(request.form.get('rating', 0))

    conn = sqlite3.connect(reviews_bp.db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (name, content, rating, is_public) VALUES (?, ?, ?, 0)", (name, content, rating))
    conn.commit()
    conn.close()

    return render_template('review_thanks.html', name=name)
