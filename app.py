from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/bookstore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

if __name__ == '__main__':
    app.run(debug=True)
from models import db, User, Category, Book, Order

@app.before_first_request
def create_tables():
    db.create_all()

    # Добавляем тестовые данные
    if not Category.query.first():
        categories = ['Фантастика', 'Детектив', 'Роман', 'Научная литература']
        for name in categories:
            db.session.add(Category(name=name))
        db.session.commit()
from routes import *

# Инициализация планировщика
scheduler = BackgroundScheduler()

# Запускаем задачу проверки напоминаний каждый день в 9:00
scheduler.add_job(
    func=check_rental_reminders,
    trigger='cron',
    hour=9,
    minute=0
)

# Запуск планировщика при старте приложения
@app.before_first_request
def initialize_scheduler():
    if not scheduler.running:
        scheduler.start()

# Остановка планировщика при завершении приложения
import atexit
atexit.register(lambda: scheduler.shutdown())
