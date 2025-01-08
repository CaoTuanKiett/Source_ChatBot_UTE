from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from app.database.database import SessionLocal
from app.models import feedback_model
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


# Get all feedbacks
@router.get("/feedbacks", response_model=List[schemas.Feedback])
def get_feedbacks(db: Session = Depends(get_db)):
    return feedback_model.get_feedbacks(db)


# Create a new feedback
@router.post("/feedback", response_model=schemas.Feedback)
def create_feedback(feedback: schemas.Feedback, db: Session = Depends(get_db)):
    return feedback_model.create_feedback(db, feedback)


# Update feedback trang_thai
@router.put("/feedback/{feedback_id}", response_model=schemas.Feedback)
def update_feedback(
    feedback_id: int, feedback: schemas.Feedback, db: Session = Depends(get_db)
):
    return feedback_model.update_feedback(db, feedback_id, feedback)


# search feedback
@router.get("/feedback/search/{search}", response_model=List[schemas.Feedback])
def search_feedback(search: str, db: Session = Depends(get_db)):
    return feedback_model.search_feedback(db, search)
