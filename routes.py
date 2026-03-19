from app import app, db
from models import Book, Category
from flask import render_template, request, redirect, url_for

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    sort_by = request.args.get('sort_by', 'title')
    books = Book.query.order_by(getattr(Book, sort_by)).all()
    categories = Category.query.all()
    return render_template('books.html', books=books, categories=categories)

@app.route('/login')
def login():
    return render_template('login.html')

from flask_login import login_required, current_user
from models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
@login_required
def books():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    # Логика для пользовательского интерфейса
    sort_by = request.args.get('sort_by', 'title')
    books = Book.query.order_by(getattr(Book, sort_by)).all()
    categories = Category.query.all()
    return render_template('books.html', books=books, categories=categories)


@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)  # Запрет доступа
    # Статистика для админа
    total_books = Book.query.count()
    active_orders = Order.query.filter_by(status='active').count()
    return render_template('admin/dashboard.html',
                        total_books=total_books, active_orders=active_orders)

@app.route('/admin/books')
@login_required
def admin_books():
    if current_user.role != 'admin':
        abort(403)
    books = Book.query.all()
    categories = Category.query.all()
    return render_template('admin/books_management.html', books=books, categories=categories)
