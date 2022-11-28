from datetime import datetime

from django.core.mail import send_mail
from manager import models

from src.celery import app


@app.task()
def send_email_report():
    accounts = models.Account.objects.all()
    for account in accounts:
        if account.user.email is True:
            send_mail("Everyday balance info",
                      f"Dear Mr(s) {account.user.username}, your balance rest for {datetime.now()} is "
                      f"{account.balance} rubles. For looking last transactions, use bank app. ",
                      'djangoprojectdrf@yandex.by',
                      [account.user.email, ])
