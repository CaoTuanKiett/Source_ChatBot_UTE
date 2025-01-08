from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app import schemas
from app.database import table_models as models
from datetime import datetime
from app.utils.auth import create_chatbot_token
from typing import Optional, List


# Get all chatbots
def get_chatbots(db: Session, skip: int = 0, limit: int = 100):
    print("get_chatbots")
    # Query all chatbots from database
    chatbots = db.query(models.ChatBot).offset(skip).limit(limit).all()

    chatbot_schemas = []
    # Convert SQLAlchemy object to Pydantic schema
    for chatbot in chatbots:
        chatbot_dict = chatbot.__dict__.copy()
        # chatbot_dict["ngay_tao"] = chatbot.ngay_tao.strftime("%Y-%m-%d %H:%M:%S")
        if chatbot.ngay_cap_nhat:
            chatbot_dict["ngay_cap_nhat"] = chatbot.ngay_cap_nhat.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        else:
            chatbot_dict["ngay_cap_nhat"] = None
        chatbot_schemas.append(schemas.ChatBot(**chatbot_dict))

    return chatbot_schemas


# Get all chatbot by truong_id
def get_chatbot_by_schoolId(db: Session, schoolId: int):
    print("get_chatbot_by_schoolId")
    # Query all chatbots from database
    chatbots = (
        db.query(models.ChatBot).filter(models.ChatBot.truong_id == schoolId).all()
    )

    # Convert SQLAlchemy objects to Pydantic schemas
    return [schemas.ChatBot2.from_orm(chatbot) for chatbot in chatbots]


# Get a chatbot by ID
def get_chatbot_by_id(db: Session, chatbot_id: int):
    print("get_chatbot_by_id")
    # Query the chatbot by ID
    chatbot = (
        db.query(models.ChatBot)
        .filter(models.ChatBot.id_chat_bot == chatbot_id)
        .first()
    )

    # If the chatbot is not found, raise an HTTPException
    if not chatbot:
        raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")

    # Convert SQLAlchemy object to Pydantic schema
    chatbot_dict = chatbot.__dict__.copy()
    # chatbot_dict["ngay_tao"] = chatbot.ngay_tao.strftime("%Y-%m-%d %H:%M:%S")

    return schemas.ChatBot(**chatbot_dict)


# Create a new chatbot
def create_chatbot(db: Session, chatbot: schemas.ChatBot2):
    print("create_chatbot", chatbot)
    # Create a new chatbot object
    new_chatbot = models.ChatBot(
        ten_chat_bot=chatbot.chatBotName,
        mo_ta=chatbot.description,
        thu_muc_id=chatbot.folderId,
        truong_id=chatbot.schoolId,
        avatarUrl="",
        trang_thai=chatbot.status,
        ngay_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        them_boi=chatbot.createdBy,
    )

    # Add the new chatbot to the database
    db.add(new_chatbot)
    db.commit()
    db.refresh(new_chatbot)
    # Convert SQLAlchemy object to Pydantic schema
    new_chatbot_dict = new_chatbot.__dict__.copy()
    # new_chatbot_dict["ngay_tao"] = new_chatbot.ngay_tao.strftime("%Y-%m-%d %H:%M:%S")
    print("new_chatbot_dict", new_chatbot_dict)
    # Tạo token cho chatbot
    token = create_chatbot_token(new_chatbot_dict)
    new_chatbot.token = token
    db.commit()
    new_chatbot_dict["token"] = token

    return schemas.ChatBot2(**new_chatbot_dict)


# Update a chatbot by ID
def update_chatbot_by_id(db: Session, chatbot_id: int, chatbot: schemas.ChatBot2):
    print("update_chatbot_by_id", chatbot)
    # Query the chatbot by ID
    db_chatbot = (
        db.query(models.ChatBot)
        .filter(models.ChatBot.id_chat_bot == chatbot_id)
        .first()
    )

    # If the chatbot is not found, raise an HTTPException
    if not db_chatbot:
        raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")

    # Update the chatbot attributes
    if chatbot.chatBotName:
        db_chatbot.ten_chat_bot = chatbot.chatBotName
    if chatbot.description:
        db_chatbot.mo_ta = chatbot.description
    if chatbot.folderId:
        db_chatbot.thu_muc_id = chatbot.folderId
    if chatbot.schoolId:
        db_chatbot.truong_id = chatbot.schoolId
    if chatbot.status is not None:
        db_chatbot.trang_thai = chatbot.status
    if chatbot.updatedTime:
        db_chatbot.ngay_cap_nhat = chatbot.updatedTime
    if chatbot.updateBy:
        db_chatbot.nguoi_cap_nhat = chatbot.updateBy

    db_chatbot.ngay_cap_nhat = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)

    db_chatbot.token = create_chatbot_token(db_chatbot.__dict__)

    # Commit the changes to the database
    db.commit()

    # Convert SQLAlchemy object to Pydantic schema
    chatbot_dict = db_chatbot.__dict__.copy()
    print("chatbot_dict", chatbot_dict)
    # chatbot_dict["ngay_tao"] = db_chatbot.ngay_tao.strftime("%Y-%m-%d %H:%M:%S")

    return db_chatbot.id_chat_bot


# Delete a chatbot by ID
def delete_chatbot_by_id(db: Session, chatbot_id: int):
    print("delete_chatbot_by_id")
    # Query the chatbot by ID
    chatbot = (
        db.query(models.ChatBot)
        .filter(models.ChatBot.id_chat_bot == chatbot_id)
        .first()
    )

    # If the chatbot is not found, raise an HTTPException
    if not chatbot:
        raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")

    # Delete the chatbot from the database
    db.delete(chatbot)
    db.commit()
    return chatbot.id_chat_bot


# Get folderID by chatbotID
def get_folderId_by_chatbotId(db: Session, chatbot_id: int):
    print("get_folderId_by_chatbotId")
    try:
        # Truy vấn chỉ lấy thu_muc_id
        thu_muc_id = (
            db.query(models.ChatBot.thu_muc_id)
            .filter(models.ChatBot.id_chat_bot == chatbot_id)
            .scalar()  # Trả về giá trị duy nhất thay vì đối tượng
        )

        # Nếu không tìm thấy chatbot, raise exception
        if thu_muc_id is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy thu_muc_id")

        return thu_muc_id

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")


# Search chatbot by every field and schoolId
def search_chatbot(db: Session, dataSearch: schemas.SearchData):
    print("search_chatbot")
    # Khởi tạo query ban đầu
    query = db.query(models.ChatBot).filter(
        models.ChatBot.truong_id == dataSearch.schoolId
    )

    # Chỉ thêm điều kiện tìm kiếm nếu có giá trị searchValue
    if dataSearch.searchValue:
        search_value = f"%{dataSearch.searchValue}%"

        # Lọc các trường kiểu chuỗi với ilike
        query = query.filter(
            models.ChatBot.ten_chat_bot.ilike(search_value)
            | models.ChatBot.mo_ta.ilike(search_value)
            | models.ChatBot.them_boi.ilike(search_value)
            | models.ChatBot.ngay_tao.ilike(f"%{dataSearch.searchValue}%")
        )

    # Lấy kết quả (sử dụng phân trang nếu cần)
    chatbots = query.all()

    # Convert SQLAlchemy objects sang Pydantic schemas
    return [schemas.ChatBot2.from_orm(chatbot) for chatbot in chatbots]
