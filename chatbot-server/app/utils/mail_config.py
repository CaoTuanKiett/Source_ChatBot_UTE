from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings

MAIL_USERNAME = settings.MAIL_USERNAME
MAIL_PASSWORD = settings.MAIL_PASSWORD
MAIL_FROM = settings.MAIL_FROM
MAIL_PORT = settings.MAIL_PORT
MAIL_SERVER = settings.MAIL_SERVER
MAIL_TLS = settings.MAIL_TLS
MAIL_SSL = settings.MAIL_SSL


# Cấu hình email server
class EmailConfig(BaseModel):
    MAIL_USERNAME: str = MAIL_USERNAME  # Email của bạn
    MAIL_PASSWORD: str = MAIL_PASSWORD  # Mật khẩu
    MAIL_FROM: EmailStr = MAIL_FROM  # Email gửi đi
    MAIL_PORT: int = MAIL_PORT  # Port SMTP
    MAIL_SERVER: str = MAIL_SERVER  # Server SMTP (VD: Gmail)
    MAIL_STARTTLS: bool = True  # Sử dụng STARTTLS
    MAIL_SSL_TLS: bool = False


# Tạo đối tượng cấu hình email
email_config = EmailConfig()

# Kết nối email
config = ConnectionConfig(
    MAIL_USERNAME=email_config.MAIL_USERNAME,
    MAIL_PASSWORD=email_config.MAIL_PASSWORD,
    MAIL_FROM=email_config.MAIL_FROM,
    MAIL_PORT=email_config.MAIL_PORT,
    MAIL_SERVER=email_config.MAIL_SERVER,
    MAIL_STARTTLS=email_config.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_config.MAIL_SSL_TLS,
)
