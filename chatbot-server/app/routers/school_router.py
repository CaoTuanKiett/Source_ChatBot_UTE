import json
import os
import shutil
from app import schemas
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.database.database import SessionLocal
from app.models import school_model
from app.utils.config_cloudinary import handle_logic_cover_image, upload_to_cloudinary

router = APIRouter()


# Dependency để lấy session DB cho mỗi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all schools
@router.get("/schools", response_model=List[schemas.School2])
def get_schools(db: Session = Depends(get_db)):
    return school_model.get_schools(db)


# Get school by id
@router.get("/school/{school_id}", response_model=schemas.School2)
def get_school_by_id(school_id: int, db: Session = Depends(get_db)):
    school = school_model.get_school_by_id(db, school_id)
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school


# Create a new school
@router.post("/school", response_model=schemas.SchoolResponse)
def create_school(
    # school: schemas.School,
    school: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Giải mã chuỗi JSON thành object
        chatbot_data = json.loads(school)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for school")

    # Chuyển dữ liệu sang schema ChatBot
    school_obj = schemas.School(**chatbot_data)

    # Xử lý ảnh đại diện
    avatar_url = handle_logic_cover_image(file)

    school = school_model.create_school(db, school_obj, avatar_url)
    print(school)
    return {
        "schoolId": school.idSchool,
        "schoolName": school.schoolName,
        "message": "Tạo mới trường học thành công",
    }


# Update a school
@router.put("/school/{school_id}", response_model=schemas.SchoolResponse)
def update_school(
    school_id: int,
    school: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Giải mã chuỗi JSON thành object
        chatbot_data = json.loads(school)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for school")

    # Chuyển dữ liệu sang schema ChatBot
    school_obj = schemas.School(**chatbot_data)

    # Xử lý ảnh đại diện
    avatar_url = handle_logic_cover_image(file)

    school = school_model.update_school(db, school_id, school_obj, avatar_url)
    return {
        "schoolId": school.idSchool,
        "schoolName": school.schoolName,
        "message": "Cập nhật thông tin trường học thành công",
    }


# Delete a school
@router.delete("/school/{school_id}", response_model=schemas.SchoolResponse)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    school = school_model.delete_school(db, school_id)
    return {
        "schoolId": school.idSchool,
        "schoolName": school.schoolName,
        "message": "Xóa trường học thành công",
    }
