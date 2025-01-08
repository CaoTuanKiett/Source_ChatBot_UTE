from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import table_models as models
from app import schemas
from datetime import datetime
from typing import List


# Get all table GopY join table Chatbot
def get_feedbacks(db: Session) -> List[schemas.Feedback]:
    feedbacks = (
        db.query(
            models.GopY.id_gop_y.label("id_gop_y"),
            models.GopY.ho_ten.label("ho_ten"),
            models.GopY.email.label("email"),
            models.GopY.noi_dung.label("noi_dung"),
            models.GopY.loai_gop_y.label("loai_gop_y"),
            models.GopY.trang_thai.label("trang_thai"),
            models.GopY.thoi_gian_tao.label("thoi_gian_tao"),
            models.GopY.nguoi_xu_ly.label("nguoi_xu_ly"),
            models.GopY.thoi_gian_xu_ly.label("thoi_gian_xu_ly"),
            models.GopY.chat_bot_id.label("chat_bot_id"),
            models.ChatBot.ten_chat_bot.label("ten_chat_bot"),
        )
        .join(
            models.ChatBot,
            models.GopY.chat_bot_id == models.ChatBot.id_chat_bot,
        )
        .all()
    )
    return feedbacks


# Create feedback
def create_feedback(db: Session, feedback: schemas.Feedback):
    new_feedback = models.GopY(
        ho_ten=feedback.ho_ten,
        email=feedback.email,
        noi_dung=feedback.noi_dung,
        loai_gop_y=feedback.loai_gop_y,
        trang_thai="Chưa xử lý",
        thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        chat_bot_id=feedback.chat_bot_id,
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


# Update feedback trang_thai
def update_feedback(db: Session, feedback_id: int, feedback: schemas.Feedback):
    feedback_update = (
        db.query(models.GopY).filter(models.GopY.id_gop_y == feedback_id).first()
    )
    if feedback_update is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if feedback.nguoi_xu_ly is not None:
        feedback_update.nguoi_xu_ly = feedback.nguoi_xu_ly

    feedback_update.trang_thai = "Đã xử lý"
    feedback_update.thoi_gian_xu_ly = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    db.refresh(feedback_update)
    return feedback_update


# search feedback by all attributes
def search_feedback(db: Session, search: str) -> List[schemas.Feedback]:
    feedbacks = (
        db.query(
            models.GopY.id_gop_y.label("id_gop_y"),
            models.GopY.ho_ten.label("ho_ten"),
            models.GopY.email.label("email"),
            models.GopY.noi_dung.label("noi_dung"),
            models.GopY.loai_gop_y.label("loai_gop_y"),
            models.GopY.trang_thai.label("trang_thai"),
            models.GopY.thoi_gian_tao.label("thoi_gian_tao"),
            models.GopY.nguoi_xu_ly.label("nguoi_xu_ly"),
            models.GopY.thoi_gian_xu_ly.label("thoi_gian_xu_ly"),
            models.GopY.chat_bot_id.label("chat_bot_id"),
            models.ChatBot.ten_chat_bot.label("ten_chat_bot"),
        )
        .join(
            models.ChatBot,
            models.GopY.chat_bot_id == models.ChatBot.id_chat_bot,
        )
        .filter(
            models.GopY.ho_ten.like(f"%{search}%")
            | models.GopY.email.like(f"%{search}%")
            | models.GopY.noi_dung.like(f"%{search}%")
            | models.GopY.loai_gop_y.like(f"%{search}%")
            | models.GopY.trang_thai.like(f"%{search}%")
            | models.ChatBot.ten_chat_bot.like(f"%{search}%")
        )
        .all()
    )
    return feedbacks
