from fastapi import FastAPI, BackgroundTasks, APIRouter
from fastapi_mail import FastMail, MessageSchema
from pydantic import BaseModel, EmailStr

from app.utils.mail_config import config

app = FastAPI()
router = APIRouter()


# Dữ liệu request gửi email
class EmailRequest(BaseModel):
    email: EmailStr
    subject: str
    body: str


# API gửi email
@router.post("/send-email")
async def send_email(email_data: EmailRequest, background_tasks: BackgroundTasks):
    # Tạo nội dung email
    message = MessageSchema(
        subject=email_data.subject,
        recipients=[email_data.email],  # Danh sách người nhận
        body=email_data.body,
        subtype="html",  # Có thể là "html" hoặc "plain"
    )

    # Khởi tạo FastMail
    fm = FastMail(config)

    # Gửi email trong background (không chặn API)
    background_tasks.add_task(fm.send_message, message)
    return {"message": f"Email sent to {email_data.email}"}
