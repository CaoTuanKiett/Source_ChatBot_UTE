import logging
from fastapi import FastAPI
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    gemini_api,
    users_router,
    document_router,
    auth_router,
    role_router,
    mail_router,
    chat_router,
    chatbot_router,
    school_router,
    folder_router,
    question_router,
    feedback_router,
)

# from app.database.database import engine, Base
import sys
import os

# Thêm thư mục gốc của dự án vào sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


API_VERSION = settings.API_VERSION

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL frontend được phép truy cập
    allow_credentials=True,  # Cho phép gửi cookie/authorization header
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, ...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# Import router từ các module
app.include_router(users_router.router, prefix=API_VERSION, tags=["User"])
app.include_router(document_router.router, prefix=API_VERSION, tags=["Document"])
app.include_router(auth_router.router, prefix=API_VERSION, tags=["Auth"])
app.include_router(role_router.router, prefix=API_VERSION, tags=["Role"])
app.include_router(mail_router.router, prefix=API_VERSION, tags=["Mail"])
app.include_router(chat_router.router, prefix=API_VERSION, tags=["Chat"])
app.include_router(chatbot_router.router, prefix=API_VERSION, tags=["Chatbot"])
app.include_router(school_router.router, prefix=API_VERSION, tags=["School"])
app.include_router(folder_router.router, prefix=API_VERSION, tags=["Folder"])
app.include_router(question_router.router, prefix=API_VERSION, tags=["Question"])
app.include_router(feedback_router.router, prefix=API_VERSION, tags=["Feedback"])

# Include router cho API của Gemini
app.include_router(gemini_api.router, prefix=API_VERSION, tags=["Gemini"])

# Khởi tạo cơ sở dữ liệu
# Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():
    logger.info("Uvicorn running on http://127.0.0.1:8000")


@app.get("/")
def read_root():
    return {"message": "Hello, Chatbot UTE readyyyyyyyy!"}
