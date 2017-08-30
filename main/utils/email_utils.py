from django.core.mail import EmailMessage


def send_email(title, body, to):
    email = EmailMessage(title, body, to=[to])
    email.send()

