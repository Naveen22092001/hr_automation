import smtplib
from email.mime.text import MIMEText
import logging

SENDER_EMAIL = "timesheetsystem2025@gmail.com"
SENDER_PASSWORD = "mhuv nxdf ciqz igws" 

def send_inventory_email_to_manager( employee_name, tool_needed, reason, manager_name, manager_email):
    try:
        subject = f"Inventory Request from {employee_name}"
        body = f"""
Dear {manager_name},

{employee_name} has requested the following item from inventory:

 Item: {tool_needed}
 Reason: {reason}
 

Please review the request in the admin panel.

Regards,
Timesheet System
        """

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = manager_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, manager_email, msg.as_string())

        logging.info(f"📨 Email sent to {manager_email}")
    except Exception as e:
        logging.error(f" Failed to send email: {e}")
