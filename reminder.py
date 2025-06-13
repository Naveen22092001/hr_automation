import smtplib
from email.mime.text import MIMEText

def send_reminder_email(to_email, subject, body):
    from_email = "your_email@gmail.com"         # Your Gmail
    password = "your_app_password_here"         # Gmail App Password (not your real password)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.send_message(msg)
