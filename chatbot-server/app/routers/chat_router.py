from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.background import BackgroundTasks
from app.config import settings
from app.database.database import SessionLocal
from app.models import chat_model, chatbot_model
from sqlalchemy.orm import Session
from app import schemas
from app.gemini_api.genai_model import embed_text
from datetime import datetime, timezone
import pytz
from app.utils.config_pinecone import get_pinecone
from app.gemini_api.genai_model import generate_response, preprocess_with_gemini
import numpy as np

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter()
local_timezone = pytz.timezone("Asia/Ho_Chi_Minh")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_vector(vector, dimension):
    if len(vector) != dimension:
        raise ValueError(
            f"Vector dimension mismatch. Expected {dimension}, got {len(vector)}"
        )
    if not np.isfinite(vector).all():
        raise ValueError(f"Vector contains invalid values: {vector}")

    print("Vector hợp lệ:")  # In 10 giá trị đầu để kiểm tra


async def save_message_in_background(db: Session, tin_nhan: schemas.TinNhan):
    chat_model.create_tin_nhan(db, tin_nhan)


# API chat
@router.post("/chat")
async def chat_api(
    message: schemas.MessageRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # Kiểm tra luồng có tồn tại không
    luong_id = message.threadId
    luong = chat_model.get_luong(db, luong_id)
    if luong is None:
        # Tạo luồng mới
        luong = chat_model.create_luong(
            db, schemas.LuongCreate(chatbotId=message.chatbotId)
        )
        luong_id = luong.idLuong
    else:
        print("Luồng đã tồn tại", schemas.Luong(**luong.__dict__))

    # Lưu tin nhắn không đồng bộ
    background_tasks.add_task(
        save_message_in_background,
        db=db,
        tin_nhan=schemas.TinNhan(
            noi_dung=message.content,
            nguoi_gui=message.sender,
            thoi_gian_gui=datetime.now(local_timezone).strftime("%Y-%m-%d %H:%M:%S"),
            luong_id=luong_id,
        ),
    )

    # Get tin nhắn của luồng
    listMessages = chat_model.get_tin_nhan_by_luong(db, luong_id, message.chatbotId)
    # print("listMessages:", listMessages)

    # xử lý câu hỏi
    question = preprocess_with_gemini(message.content, listMessages)
    print("message.content:", question)

    # Chuyển câu hỏi thành vector
    # question_vector = embed_text(message.content)
    question_vector = embed_text(question)  # dùng câu hỏi đã qua xử lý
    # dimension = 768  # Đảm bảo đúng dimension theo cấu hình index
    # validate_vector(question_vector, dimension)
    # print("question_vector:", question_vector)

    # Get Namespace (FolderId)
    namespace = chatbot_model.get_folderId_by_chatbotId(db, message.chatbotId)

    search_results = get_pinecone().query(
        vector=[question_vector],
        top_k=3,
        include_metadata=True,
        include_values=False,
        namespace=str(namespace),
    )
    # print("search_results:", search_results)

    # Tổng hợp nội dung từ Pinecone
    context = "\n".join(
        [result["metadata"]["text"] for result in search_results["matches"]]
    )

    print("context:", context)

    # Gửi câu hỏi tới Gemini
    bot_response = generate_response(
        schemas.QuestionRequest(
            question=question,
            document=context,
            historyMessages=listMessages,
            # question=message.content, document=context, historyMessages=listMessages
        )
    )
    # Lưu tin nhắn của chatbot
    response = chat_model.create_tin_nhan(
        db,
        schemas.TinNhan(
            noi_dung=bot_response,
            nguoi_gui="Chatbot",
            thoi_gian_gui=datetime.now(local_timezone).strftime("%Y-%m-%d %H:%M:%S"),
            # thoi_gian_gui=datetime.now(timezone.utc).isoformat(),
            luong_id=luong_id,
        ),
    )

    return {
        "id": response.id_tin_nhan,
        "threadId": luong_id,
        "content": response.noi_dung,
        "sender": response.nguoi_gui,
        "sentTime": response.thoi_gian_gui,
    }


# API get tin nhắn theo luồng
@router.get("/messages/{threadId}/{chatbotId}")
async def get_messages(threadId: int, chatbotId: int, db: Session = Depends(get_db)):
    if threadId is None:
        raise HTTPException(status_code=400, detail="threadId không được để trống")

    listMessages = chat_model.get_tin_nhan_by_luong(db, threadId, chatbotId)

    return listMessages


# API save one message
@router.post("/message")
async def save_message(message: schemas.MessageRequest, db: Session = Depends(get_db)):
    # Kiểm tra luồng có tồn tại không
    luong_id = message.threadId
    luong = chat_model.get_luong(db, luong_id)
    if luong is None:
        # Tạo luồng mới
        luong = chat_model.create_luong(
            db, schemas.LuongCreate(chatbotId=message.chatbotId)
        )
        luong_id = luong.idLuong
    else:
        print("Luồng đã tồn tại", schemas.Luong(**luong.__dict__))

    # Lưu tin nhắn
    response = chat_model.create_tin_nhan(
        db,
        schemas.TinNhan(
            noi_dung=message.content,
            nguoi_gui=message.sender,
            thoi_gian_gui=datetime.now(local_timezone).strftime("%Y-%m-%d %H:%M:%S"),
            luong_id=luong_id,
        ),
    )

    return {
        "id": response.id_tin_nhan,
        "threadId": luong_id,
        "content": response.noi_dung,
        "sender": response.nguoi_gui,
        "sentTime": response.thoi_gian_gui,
    }
