from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from app.database.database import SessionLocal
from app.models import question_model
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


# Get all questions
@router.get("/questions/", response_model=List[schemas.UserQuestion2])
def get_questions(db: Session = Depends(get_db)):
    questions = question_model.get_questions(db)
    return questions


# Create a new question
@router.post("/question", response_model=schemas.UserQuestionResponse)
def create_question(question: schemas.UserQuestion2, db: Session = Depends(get_db)):
    new_question = question_model.create_question(db, question)
    return schemas.UserQuestionResponse(
        idQuestion=new_question.id_cau_hoi, message="Question created successfully"
    )


# Update Answer for question
@router.put("/question/{id_question}", response_model=schemas.UserQuestionResponse)
def update_answer(
    id_question: int, question: schemas.UserQuestion2, db: Session = Depends(get_db)
):
    question_update = question_model.update_answer(db, id_question, question)
    return schemas.UserQuestionResponse(
        idQuestion=question_update.id_cau_hoi, message="Answer updated successfully"
    )


# search question
@router.get("/question/search/{search}", response_model=List[schemas.UserQuestion2])
def search_question(
    db: Session = Depends(get_db),
    search: str = "",
):
    questions = question_model.search_question(db, search)
    return questions
