from sqlalchemy.orm import Session
from app.database import table_models as models
from app.schemas import LuongCreate, TinNhan, Luong
from datetime import datetime
from fastapi import HTTPException
from typing import List
from sqlalchemy import asc


# Tạo luồng mới
def create_luong(db: Session, luong: LuongCreate):
    print("chatbotId11:", luong)
    # Kiểm tra chatbotId có tồn tại không
    chatbot = (
        db.query(models.ChatBot)
        .filter(models.ChatBot.id_chat_bot == luong.chat_bot_id)
        .first()
    )
    if chatbot is None:
        raise HTTPException(status_code=404, detail="Chatbot không tồn tại")

    db_luong = models.Luong(chat_bot_id=luong.chat_bot_id)
    db.add(db_luong)
    db.commit()
    db.refresh(db_luong)
    return Luong(**db_luong.__dict__)


# Lấy luồng theo id
def get_luong(db: Session, luong_id: int):
    return db.query(models.Luong).filter(models.Luong.id_luong == luong_id).first()


# Lưu tin nhắn
def create_tin_nhan(db: Session, tin_nhan: TinNhan):
    print("tin_nhan:", tin_nhan)
    db_tin_nhan = models.TinNhan(
        noi_dung=tin_nhan.content,
        nguoi_gui=tin_nhan.sender,
        thoi_gian_gui=tin_nhan.sentTime,
        luong_id=tin_nhan.threadId,
    )
    db.add(db_tin_nhan)
    db.commit()
    db.refresh(db_tin_nhan)
    print("db_tin_nhan:", db_tin_nhan)
    return db_tin_nhan


# Kết thúc luồng
def end_luong(db: Session, luong_id: int):
    luong = db.query(models.Luong).filter(models.Luong.id_luong == luong_id).first()
    if luong:
        luong.thoi_gian_ket_thuc = datetime.utcnow().isoformat()
        db.commit()
        return luong
    return None


# Lấy tin nhắn của một luồng
def get_tin_nhan_by_luong(db: Session, luong_id: int, chatbotId: int) -> List[dict]:
    listMessages = (
        db.query(models.TinNhan)
        .join(
            models.Luong, models.TinNhan.luong_id == models.Luong.id_luong
        )  # Join đúng cách
        .filter(models.Luong.chat_bot_id == chatbotId)  # Điều kiện chatbotId
        .filter(models.TinNhan.luong_id == luong_id)  # Điều kiện luong_id
        .order_by(asc(models.TinNhan.thoi_gian_gui))  # Sắp xếp theo thoi_gian_gui
        .all()
    )
    # Chuyển đổi danh sách các đối tượng ORM thành danh sách dict rõ ràng
    # converted_messages = [
    #     TinNhan.from_orm(message).dict(by_alias=True) for message in listMessages
    # ]
    # return converted_messages
    converted_messages = []
    for message in listMessages:
        message_dict = message.__dict__.copy()
        message_dict["thoi_gian_gui"] = message.thoi_gian_gui.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        message_detail = {
            "id": message_dict["id_tin_nhan"],
            "content": message_dict["noi_dung"],
            "sender": message_dict["nguoi_gui"],
            "sentTime": message_dict["thoi_gian_gui"],
            "threadId": message_dict["luong_id"],
        }
        converted_messages.append(message_detail)

        # converted_messages.append(TinNhan(**message_dict).dict(by_alias=True))

    return converted_messages


# Lấy các luồng của một chatbot
def get_luongs_by_chatbot(db: Session, chat_bot_id: int):
    return db.query(models.Luong).filter(models.Luong.chat_bot_id == chat_bot_id).all()
