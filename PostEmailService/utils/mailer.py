from aiosmtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from utils.config import HOST, USERNAME, PASSWORD, PORT, MailBody


async def send_mail(data: dict | None = None):
    try:
        msg = MailBody(**data)
        message = MIMEText(msg.body, "html")
        message["From"] = USERNAME
        message["To"] = ", ".join(msg.to)
        message["Subject"] = msg.subject

        async with SMTP(hostname=HOST, port=int(PORT), use_tls=(int(PORT) == 465)) as smtp:
            await smtp.connect()
            if int(PORT) != 465:
                await smtp.starttls()

            await smtp.login(USERNAME, PASSWORD)
            await smtp.send_message(message)
        return {"status": 200, "errors": None}

    except SMTPException as e:
        return {"status": 500, "errors": str(e)}

    except Exception as e:
        return {"status": 500, "errors": str(e)}
