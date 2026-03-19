from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Message
from app import app, db, mail  # предполагаем, что Flask‑Mail настроен

def check_rental_reminders():
    """Проверяет аренды и отправляет напоминания за 3 дня до окончания"""
    three_days_later = datetime.utcnow() + timedelta(days=3)
    three_days_ago = datetime.utcnow() - timedelta(days=1)

    # Находим аренды, которые закончатся через 3 дня
    upcoming_expirations = RentalTransaction.query.filter(
        RentalTransaction.is_active == True,
        RentalTransaction.end_date >= three_days_later.date(),
        RentalTransaction.end_date < (three_days_later + timedelta(days=1)).date()
    ).all()

    # Находим просроченные аренды (закончились вчера или сегодня)
    expired_rentals = RentalTransaction.query.filter(
        RentalTransaction.is_active == True,
        RentalTransaction.end_date >= three_days_ago.date(),
        RentalTransaction.end_date <= datetime.utcnow().date()
    ).all()

    for rental in upcoming_expirations:
        # Проверяем, не было ли уже отправлено напоминание
        existing_reminder = RentalReminder.query.filter_by(
            rental_id=rental.id,
            reminder_type='warning'
        ).first()

        if not existing_reminder:
            # Создаём запись напоминания
            reminder = RentalReminder(
                user_id=rental.user_id,
                book_id=rental.book_id,
                rental_id=rental.id,
                reminder_type='warning',
                is_sent=False
            )
            db.session.add(reminder)

            # Отправляем email
            send_reminder_email(rental, 'warning')
            reminder.is_sent = True
            db.session.commit()

    for rental in expired_rentals:
        existing_expired = RentalReminder.query.filter_by(
            rental_id=rental.id,
            reminder_type='expired'
        ).first()

        if not existing_expired:
            reminder = RentalReminder(
                user_id=rental.user_id,
                book_id=rental.book_id,
                rental_id=rental.id,
                reminder_type='expired',
                is_sent=False
            )
            db.session.add(reminder)

            # Отправляем email о просрочке
            send_reminder_email(rental, 'expired')
            reminder.is_sent = True
            db.session.commit()

def send_reminder_email(rental, reminder_type):
    """Отправляет email‑напоминание пользователю"""
    with app.app_context():
        msg = Message()
        if reminder_type == 'warning':
            msg.subject = 'Напоминание: срок аренды книги истекает'
            msg.body = f'''
Уважаемый {rental.user.username}!

Напоминаем, что срок аренды книги "{rental.book.title}" истекает {rental.end_date.strftime('%d.%m.%Y')}.

Пожалуйста, верните книгу или продлите аренду.

С уважением,
Команда библиотеки
'''
        else:  # expired
            msg.subject = 'Просрочка: срок аренды книги истёк'
            msg.body = f'''
Уважаемый {rental.user.username}!

Срок аренды книги "{rental.book.title}" истёк {rental.end_date.strftime('%d.%m.%Y')}.

Пожалуйста, верните книгу как можно скорее.

С уважением,
Команда библиотеки
'''

        msg.recipients = [rental.user.email]
        try:
            mail.send(msg)
        except Exception as e:
            print(f'Ошибка отправки email: {e}')
            db.session.rollback()
