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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('books'))
    return render_template('login.html')
from flask import request, jsonify
from models import db, Book, Category

@app.route('/api/admin/books', methods=['POST'])
@login_required
def add_book():
  if current_user.role != 'admin':
    return jsonify({'success': False, 'error': 'Доступ запрещён'}), 403

  try:
    title = request.form['title']
    author = request.form['author']
    year = int(request.form['year'])
    category_id = int(request.form['category_id'])
    price = float(request.form['price'])
    rental_price = float(request.form['rental_price'])
    is_available = 'is_available' in request.form
    stock_quantity = int(request.form.get('stock_quantity', 0))

    book = Book(
      title=title,
      author=author,
      year=year,
      category_id=category_id,
      price=price,
      rental_price=rental_price,
      is_available=is_available,
      stock_quantity=stock_quantity
    )
    db.session.add(book)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Книга добавлена'})
  except Exception as e:
    db.session.rollback()
    return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/books/<int:book_id>', methods=['PUT'])
@login_required
def edit_book(book_id):
  if current_user.role != 'admin':
    return jsonify({'success': False, 'error': 'Доступ запрещён'}), 403

  book = Book.query.get_or_404(book_id)
  try:
    book.title = request.form['title']
    book.author = request.form['author']
    book.year = int(request.form['year'])
    book.category_id = int(request.form['category_id'])
    book.price = float(request.form['price'])
    book.rental_price = float(request.form['rental_price'])
    book.is_available = 'is_available' in request.form
    book.stock_quantity = int(request.form.get('stock_quantity', 0))
    db.session.commit()
    return jsonify({'success': True, 'message': 'Книга обновлена'})
  except Exception as e:
    db.session.rollback()
    return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/books/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
  if current_user.role != 'admin':
    return jsonify({'success': False, 'error': 'Доступ запрещён'}), 403

  book = Book.query.get_or_404(book_id)
  try:
    db.session.delete(book)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Книга удалена'})
  except Exception as e:
    db.session.rollback()
    return jsonify({'success': False, 'error': str(e)}), 500
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('register.html')

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('index'))
