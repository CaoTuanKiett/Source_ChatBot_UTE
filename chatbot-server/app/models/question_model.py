from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import table_models as models
from app import schemas
from datetime import datetime
from typing import List


# Get all table CauHoiNguoiDung join table Chatbot
def get_questions(db: Session) -> List[schemas.UserQuestion2]:
    questions = (
        db.query(
            models.CauHoiNguoiDung.id_cau_hoi.label("id_cau_hoi"),
            models.CauHoiNguoiDung.ho_ten.label("ho_ten"),
            models.CauHoiNguoiDung.cau_hoi.label("cau_hoi"),
            models.CauHoiNguoiDung.cau_tra_loi.label("cau_tra_loi"),
            models.CauHoiNguoiDung.email.label("email"),
            models.CauHoiNguoiDung.trang_thai.label("trang_thai"),
            models.CauHoiNguoiDung.thoi_gian_tao.label("thoi_gian_tao"),
            models.CauHoiNguoiDung.nguoi_tra_loi.label("nguoi_tra_loi"),
            models.CauHoiNguoiDung.thoi_gian_xu_ly.label("thoi_gian_xu_ly"),
            models.CauHoiNguoiDung.chat_bot_id.label("chat_bot_id"),
            # models.ChatBot.id_chat_bot.label("id_chat_bot"),  # Trường `id` từ Chatbot
            models.ChatBot.ten_chat_bot.label(
                "ten_chat_bot"
            ),  # Trường `name` từ Chatbot
        )
        .join(
            models.ChatBot,
            models.CauHoiNguoiDung.chat_bot_id == models.ChatBot.id_chat_bot,
        )  # Join với Chatbot
        .all()
    )
    return questions


# Create new question
def create_question(
    db: Session, question: schemas.UserQuestion2
) -> models.CauHoiNguoiDung:
    new_question = models.CauHoiNguoiDung(
        ho_ten=question.ho_ten,
        email=question.email,
        cau_hoi=question.cau_hoi,
        trang_thai="Chưa xử lý",
        thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        chat_bot_id=question.chat_bot_id,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


# Update Answer for question
def update_answer(
    db: Session, id_question: int, question: schemas.UserQuestion2
) -> models.CauHoiNguoiDung:
    question_db = (
        db.query(models.CauHoiNguoiDung)
        .filter(models.CauHoiNguoiDung.id_cau_hoi == id_question)
        .first()
    )
    if question_db is None:
        raise HTTPException(status_code=404, detail="Question not found")

    question_db.cau_tra_loi = question.cau_tra_loi
    question_db.trang_thai = "Đã xử lý"
    question_db.nguoi_tra_loi = question.nguoi_tra_loi
    question_db.thoi_gian_xu_ly = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    db.refresh(question_db)
    return question_db


# Search question by all attributes
def search_question(db: Session, search: str) -> List[schemas.UserQuestion2]:
    questions = (
        db.query(
            models.CauHoiNguoiDung.id_cau_hoi.label("id_cau_hoi"),
            models.CauHoiNguoiDung.ho_ten.label("ho_ten"),
            models.CauHoiNguoiDung.cau_hoi.label("cau_hoi"),
            models.CauHoiNguoiDung.cau_tra_loi.label("cau_tra_loi"),
            models.CauHoiNguoiDung.email.label("email"),
            models.CauHoiNguoiDung.trang_thai.label("trang_thai"),
            models.CauHoiNguoiDung.thoi_gian_tao.label("thoi_gian_tao"),
            models.CauHoiNguoiDung.nguoi_tra_loi.label("nguoi_tra_loi"),
            models.CauHoiNguoiDung.thoi_gian_xu_ly.label("thoi_gian_xu_ly"),
            models.CauHoiNguoiDung.chat_bot_id.label("chat_bot_id"),
            # models.ChatBot.id_chat_bot.label("id_chat_bot"),  # Trường `id` từ Chatbot
            models.ChatBot.ten_chat_bot.label(
                "ten_chat_bot"
            ),  # Trường `name` từ Chatbot
        )
        .join(
            models.ChatBot,
            models.CauHoiNguoiDung.chat_bot_id == models.ChatBot.id_chat_bot,
        )  # Join với Chatbot
        .filter(
            models.CauHoiNguoiDung.ho_ten.like(f"%{search}%")
            | models.CauHoiNguoiDung.email.like(f"%{search}%")
            | models.CauHoiNguoiDung.cau_hoi.like(f"%{search}%")
            | models.CauHoiNguoiDung.cau_tra_loi.like(f"%{search}%")
            | models.CauHoiNguoiDung.trang_thai.like(f"%{search}%")
            | models.CauHoiNguoiDung.nguoi_tra_loi.like(f"%{search}%")
            | models.CauHoiNguoiDung.thoi_gian_tao.like(f"%{search}%")
            | models.CauHoiNguoiDung.thoi_gian_xu_ly.like(f"%{search}%")
        )
        .all()
    )
    return questions
