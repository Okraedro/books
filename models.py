
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' или 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    price = db.Column(db.Numeric(10, 2), nullable=False)  # цена покупки
    rental_price = db.Column(db.Numeric(10, 2), nullable=False)  # цена аренды
    is_available = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    order_type = db.Column(db.String(20), nullable=False)  # 'purchase' или 'rental'
    rental_period = db.Column(db.String(20))  # '2_weeks', '1_month', '3_months'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # 'active', 'expired', 'cancelled'
# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Название книги
    author = db.Column(db.String(100), nullable=False)  # Автор
    genre = db.Column(db.String(50))  # Жанр
    year_published = db.Column(db.Integer)  # Год издания
    pages = db.Column(db.Integer)  # Количество страниц
    rating = db.Column(db.Float, default=0.0)  # Рейтинг (1–5)
    status = db.Column(db.String(20), default='not_started')  # Статус чтения
    notes = db.Column(db.Text)  # Личные заметки
    cover_url = db.Column(db.String(300))  # Ссылка на обложку
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Дата добавления
    is_favorite = db.Column(db.Boolean, default=False)  # Любимая книга

    def __repr__(self):
        return f'<Book {self.title}>'
# init_db.py
from app import app, db
from models import Book

def create_sample_books():
    sample_books = [
        {
            'title': 'Мастер и Маргарита',
            'author': 'Михаил Булгаков',
            'genre': 'Роман',
            'year_published': 1966,
            'pages': 480,
            'rating': 5.0,
            'status': 'finished',
            'notes': 'Потрясающее произведение! Сочетание сатиры и мистики.',
            'cover_url': 'https://example.com/covers/master_margarita.jpg',
            'is_favorite': True
        },
        {
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'genre': 'Антиутопия',
            'year_published': 1949,
            'pages': 328,
            'rating': 4.8,
            'status': 'reading',
            'notes': 'Мрачное видение будущего, которое иногда кажется слишком реальным.',
            'cover_url': 'https://example.com/covers/1984.jpg'
        },
        {
            'title': 'Преступление и наказание',
            'author': 'Фёдор Достоевский',
            'genre': 'Психологический роман',
            'year_published': 1866,
            'pages': 671,
            'rating': 4.9,
            'status': 'finished',
            'notes': 'Глубокий анализ человеческой природы и морали.',
            'cover_url': 'https://example.com/covers/crime_punishment.jpg',
            'is_favorite': True
        }
    ]

    for book_data in sample_books:
        book = Book(**book_data)
        db.session.add(book)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_books()
        print("База данных создана и заполнена тестовыми данными!")
