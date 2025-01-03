from fastapi import FastAPI, BackgroundTasks
from utils.config import MailBody
from utils.mailer import send_mail

app = FastAPI()


@app.get("/")
async def index():
    return {"status": "fastapi mailserver is running."}


@app.post("/send-email")
async def schedule_mail(req: MailBody, tasks: BackgroundTasks):
    data = req.dict()
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}
