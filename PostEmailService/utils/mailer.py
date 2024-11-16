import logging
from .config import HOST, USERNAME, PASSWORD, PORT, MailBody
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def send_mail(data: dict | None = None):
    logging.info("Start sending email...")
    try:
        msg = MailBody(**data)
        message = MIMEText(msg.body, "html")
        message["From"] = USERNAME
        message["To"] = ", ".join(msg.to)
        message["Subject"] = msg.subject

        logging.info(f"Prepared email: {message.as_string()}")

        if int(PORT) == 465:
            with SMTP_SSL(HOST, int(PORT)) as server:
                server.login(USERNAME, PASSWORD)
                server.send_message(message)
                logging.info("Email sent via SSL.")
        else:
            with SMTP(HOST, int(PORT)) as server:
                server.ehlo()
                server.starttls()
                server.login(USERNAME, PASSWORD)
                server.send_message(message)
                logging.info("Email sent via STARTTLS.")

        return {"status": 200, "errors": None}
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return {"status": 500, "errors": str(e)}
