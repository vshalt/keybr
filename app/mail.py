from flask import current_app, render_template, Flask
from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail

def send_async_mail(app: Flask, msg: Message) -> None:
    with app.app_context():
        mail.send(msg)

def send_mail(template: str, to: str, subject: str, **kwargs) -> None:
    msg = Message(
        subject=subject,
        recipients=[to],
        sender=current_app.config['MAIL_SENDER']
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(
        target=send_async_mail, args=[current_app._get_current_object(), msg]
    )
    thr.start()
    return thr
