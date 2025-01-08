from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import table_models as models
from datetime import datetime


# Get all schools
def get_schools(db: Session):
    return db.query(models.Truong).all()


# Get school by id
def get_school_by_id(db: Session, school_id: int):
    return db.query(models.Truong).filter(models.Truong.id_truong == school_id).first()


# Create a new school
def create_school(
    db: Session, school: schemas.School, avatar_url: Optional[str] = None
):
    print("create_school", school, avatar_url)
    new_school = models.Truong(
        ten_truong=school.schoolName,
        ma_truong=school.schoolCode,
        mo_ta=school.description,
        anh_dai_dien=avatar_url,
        ngay_thanh_lap=school.dateEstablished,
        dia_chi=school.address,
        email=school.email,
        so_dien_thoai=school.phone,
        website=school.website,
        thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    return schemas.School(**new_school.__dict__)


# Update a school
def update_school(
    db: Session,
    school_id: int,
    school: schemas.School,
    avatar_url: Optional[str] = None,
):
    print("update_school", school.schoolName)
    school_to_update = (
        db.query(models.Truong).filter(models.Truong.id_truong == school_id).first()
    )
    if school_to_update is None:
        raise HTTPException(status_code=404, detail="School not found")

    if school.schoolName is not None:
        school_to_update.ten_truong = school.schoolName
    if school.schoolCode is not None:
        school_to_update.ma_truong = school.schoolCode
    if school.description is not None:
        school_to_update.mo_ta = school.description
    if school.dateEstablished is not None:
        school_to_update.ngay_thanh_lap = school.dateEstablished
    if school.address is not None:
        school_to_update.dia_chi = school.address
    if school.email is not None:
        school_to_update.email = school.email
    if school.phone is not None:
        school_to_update.so_dien_thoai = school.phone
    if school.website is not None:
        school_to_update.website = school.website

    if avatar_url is not None:
        school_to_update.anh_dai_dien = avatar_url

    db.commit()
    db.refresh(school_to_update)
    return schemas.School(**school_to_update.__dict__)


# Delete a school
def delete_school(db: Session, school_id: int):
    school_to_delete = (
        db.query(models.Truong).filter(models.Truong.id_truong == school_id).first()
    )
    if school_to_delete is None:
        raise HTTPException(status_code=404, detail="School not found")
    db.delete(school_to_delete)
    db.commit()
    return schemas.School(**school_to_delete.__dict__)
