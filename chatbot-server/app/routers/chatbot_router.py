from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from app.database.database import SessionLocal
from app.models import chatbot_model
from pinecone import Pinecone
import uuid
from app.gemini_api.genai_model import embed_text
from app.config import settings
import os
import shutil
from datetime import datetime
from app.utils.file_processing import process_file
from app.utils.config_cloudinary import upload_to_cloudinary
import json


# Create a new router
router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all chatbots
@router.get("/chatbots/", response_model=List[schemas.ChatBot])
def get_chatbots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    listChatBot = chatbot_model.get_chatbots(db, skip=skip, limit=limit)
    # if not listChatBot:
    #     raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")
    return listChatBot


# Get a chatbot by ID
@router.get("/chatbot/{chatbot_id}", response_model=schemas.ChatBot2)
def get_chatbot_by_id(chatbot_id: int, db: Session = Depends(get_db)):
    chatbot = chatbot_model.get_chatbot_by_id(db, chatbot_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")
    return chatbot


# Get all chatbot by schoolId
@router.get("/chatbots/school/{schoolId}", response_model=List[schemas.ChatBot2])
def get_chatbot_by_schoolId(schoolId: int, db: Session = Depends(get_db)):
    listChatBot = chatbot_model.get_chatbot_by_schoolId(db, schoolId)
    # if not listChatBot:
    #     raise HTTPException(status_code=404, detail="Không tìm thấy chatbot")
    return listChatBot


# Create a new chatbot
@router.post("/chatbot/", response_model=schemas.ChatBot2)
def create_chatbot(
    chatbot: schemas.ChatBot,
    # chatbot: str = Form(...),
    # fileAvt: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    return chatbot_model.create_chatbot(db, chatbot)


# Update a chatbot by ID
@router.put("/chatbot/{chatbot_id}")
def update_chatbot(
    chatbot_id: int, chatbot: schemas.ChatBot, db: Session = Depends(get_db)
):
    idChatbot = chatbot_model.update_chatbot_by_id(db, chatbot_id, chatbot)

    return {"idChatbot": idChatbot, "message": "Cập nhật chatbot thành công"}


# Delete a chatbot by ID
@router.delete("/chatbot/{chatbot_id}")
def delete_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    idChatbot = chatbot_model.delete_chatbot_by_id(db, chatbot_id)
    return {"idChatbot": idChatbot, "message": "Xóa chatbot thành công"}


# Search chatbot by every field
@router.post("/chatbot/search", response_model=List[schemas.ChatBot2])
def search_chatbot(
    dataSearch: schemas.SearchData,
    db: Session = Depends(get_db),
):
    listChatBot = chatbot_model.search_chatbot(db, dataSearch)
    return listChatBot
