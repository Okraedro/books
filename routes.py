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
from flask import render_template, request, redirect, url_for, flash
from models import db, Book

@app.route('/my-books')
@login_required
def my_books():
    books = Book.query.order_by(Book.date_added.desc()).all()
    return render_template('my_books.html', books=books)

@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form.get('genre', '')
        year_published = request.form.get('year_published')
        pages = request.form.get('pages')
        rating = request.form.get('rating', 0.0)
        status = request.form.get('status', 'not_started')
        notes = request.form.get('notes', '')
        cover_url = request.form.get('cover_url', '')
        is_favorite = 'is_favorite' in request.form

        book = Book(
            title=title,
            author=author,
            genre=genre,
            year_published=int(year_published) if year_published else None,
            pages=int(pages) if pages else None,
            rating=float(rating),
            status=status,
            notes=notes,
            cover_url=cover_url,
            is_favorite=is_favorite
        )
        db.session.add(book)
        db.session.commit()
        flash('Книга добавлена в коллекцию!', 'success')
        return redirect(url_for('my_books'))

    return render_template('add_book.html')

@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form.get('genre')
        book.year_published = int(request.form.get('year_published')) if request.form.get('year_published') else None
        book.pages = int(request.form.get('pages')) if request.form.get('pages') else None
        book.rating = float(request.form.get('rating'))
        book.status = request.form.get('status')
        book.notes = request.form.get('notes')
        book.cover_url = request.form.get('cover_url')
        book.is_favorite = 'is_favorite' in request.form
        db.session.commit()
        flash('Данные книги обновлены!', 'success')
        return redirect(url_for('my_books'))
    return render_template('edit_book.html', book=book)

@app.route('/delete-book/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Книга удалена из коллекции!', 'info')
    return redirect(url_for('my_books'))
@app.route('/book/<int:book_id>')
@login_required
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('view_book.html', book=book)
@app.route('/my-books')
@login_required
def my_books():
    # Получаем параметры сортировки из URL
    sort_by = request.args.get('sort_by', 'date_added')  # По умолчанию — по дате добавления
    order = request.args.get('order', 'desc')  # По умолчанию — убывание

    # Определяем поле для сортировки
    sort_field = None
    if sort_by == 'title':
        sort_field = Book.title
    elif sort_by == 'author':
        sort_field = Book.author
    elif sort_by == 'year_published':
        sort_field = Book.year_published
    elif sort_by == 'genre':
        sort_field = Book.genre
    else:
        sort_field = Book.date_added

    # Применяем порядок сортировки
    if order == 'desc':
        books = Book.query.order_by(sort_field.desc()).all()
    else:
        books = Book.query.order_by(sort_field.asc()).all()

    return render_template('my_books.html', books=books, sort_by=sort_by, order=order)
from flask import request, jsonify

@app.route('/my-books')
@login_required
def my_books():
    # Получаем параметры сортировки из URL
    sort_by = request.args.get('sort_by', 'date_added')
    order = request.args.get('order', 'desc')

    # Определяем поле для сортировки
    sort_field = None
    if sort_by == 'title':
        sort_field = Book.title
    elif sort_by == 'author':
        sort_field = Book.author
    elif sort_by == 'year_published':
        sort_field = Book.year_published
    elif sort_by == 'genre':
        sort_field = Book.genre
    else:
        sort_field = Book.date_added

    # Применяем порядок сортировки
    if order == 'desc':
        books = Book.query.order_by(sort_field.desc()).all()
    else:
        books = Book.query.order_by(sort_field.asc()).all()

    # Если это AJAX‑запрос, возвращаем только HTML для списка книг
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Рендерим только часть с книгами
        from flask import render_template_string
        books_html = render_template('books_list.html', books=books)
        return jsonify({'html': books_html})

    return render_template('my_books.html', books=books, sort_by=sort_by, order=order)
@app.route('/delete-book/<int:book_id>', methods=['GET', 'DELETE'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    # Если это AJAX‑запрос, возвращаем JSON‑ответ
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})

    flash('Книга успешно удалена из коллекции', 'success')
    return redirect(url_for('my_books'))
@app.route('/book/<int:book_id>/purchase', methods=['GET', 'POST'])
@login_required
def purchase_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        # Создаём транзакцию покупки
        transaction = RentalTransaction(
            user_id=current_user.id,
            book_id=book.id,
            transaction_type='purchase',
            price=book.price
        )
        db.session.add(transaction)
        db.session.commit()

        flash('Книга успешно куплена!', 'success')
        return redirect(url_for('view_book', book_id=book.id))

    return render_template('purchase.html', book=book, transaction_type='purchase')

@app.route('/book/<int:book_id>/rent', methods=['GET', 'POST'])
@login_required
def rent_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        rental_period = request.form.get('rental_period')

        # Расчёт цены аренды (например, 30 % от цены книги за месяц)
        price_multipliers = {'2_weeks': 0.15, '1_month': 0.3, '3_months': 0.7}
        price = book.price * price_multipliers.get(rental_period, 0)

        transaction = RentalTransaction(
            user_id=current_user.id,
            book_id=book.id,
            transaction_type='rental',
            rental_period=rental_period,
            price=price
        )
        transaction.calculate_end_date()
        db.session.add(transaction)
        db.session.commit()

        flash(f'Книга арендована на {rental_period.replace("_", " ")}!', 'success')
        return redirect(url_for('view_book', book_id=book.id))

    return render_template('rent.html', book=book)
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

@app.route('/admin/books')
@login_required
def admin_books():
    if not current_user.is_admin:
        flash('Доступ запрещён', 'error')
        return redirect(url_for('my_books'))

    books = Book.query.all()
    return render_template('admin/books.html', books=books)

@app.route('/admin/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_book(book_id):
    if not current_user.is_admin:
        flash('Доступ запрещён', 'error')
        return redirect(url_for('my_books'))

    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.year_published = request.form['year_published']
        book.price = float(request.form['price'])
        book.is_available = 'is_available' in request.form
        book.status = request.form['status']

        db.session.commit()
        flash('Книга обновлена', 'success')
        return redirect(url_for('admin_books'))

    return render_template('admin/edit_book.html', book=book)

@app.route('/admin/rentals')
@login_required
def admin_rentals():
    if not current_user.is_admin:
        flash('Доступ запрещён', 'error')
        return redirect(url_for('my_books'))

    # Получаем все активные аренды с информацией о пользователях
    rentals = RentalTransaction.query.filter_by(is_active=True).all()
    return render_template('admin/rentals.html', rentals=rentals)
@app.route('/admin/rental/<int:rental_id>/send-reminder', methods=['POST'])
@login_required
def send_rental_reminder(rental_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещён'}), 403

    rental = RentalTransaction.query.get_or_404(rental_id)

    # Создаём напоминание
    reminder = RentalReminder(
        user_id=rental.user_id,
        book_id=rental.book_id,
        rental_id=rental.id,
        reminder_type='warning'
    )
    db.session.add(reminder)
    db.session.commit()

    # Здесь должна быть логика отправки email/уведомления пользователю
    # Например, через Flask‑Mail или другой сервис
    send_email(
        subject='Напоминание об окончании срока аренды',
        recipient=rental.user.email,
        body=f'Срок аренды книги "{rental.book.title}" истекает {rental.end_date.strftime("%d.%m.%Y")}.'
    )

    reminder.is_sent = True
    db.session.commit()

    return jsonify({'success': 'Напоминание отправлено'})

@app.route('/admin/reminders')
@login_required
def admin_reminders():
    if not current_user.is_admin:
        flash('Доступ запрещён', 'error')
        return redirect(url_for('my_books'))

    reminders = RentalReminder.query.order_by(RentalReminder.sent_date.desc()).all()
    return render_template('admin/reminders.html', reminders=reminders)
