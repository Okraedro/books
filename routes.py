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

