from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import table_models as models
from app.schemas import User as UserSchema
from datetime import datetime
from app.utils.auth import hash_password, verify_password


def get_user(db: Session, user_id: int):
    return (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id_nguoi_dung == user_id)
        .first()
    )


# Lấy danh sách tất cả users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    print("get_users")
    # Truy vấn danh sách users từ database
    users = db.query(models.NguoiDung).offset(skip).limit(limit).all()

    # Chuyển đổi SQLAlchemy objects sang Pydantic schemas
    return [UserSchema.from_orm(user) for user in users]


# Lấy thông tin user theo ID
def get_user_by_id(db: Session, idUser: str) -> models.NguoiDung:
    return (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id_nguoi_dung == idUser)
        .first()
    )


# Tạo mới một user
def create_user(db: Session, user: schemas.User, avatar_url: Optional[str] = None):
    existing_user = (
        db.query(models.NguoiDung).filter(models.NguoiDung.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    db_user = models.NguoiDung(
        ho_ten=user.username,
        ngay_sinh=user.birthday,
        anh_dai_dien=avatar_url,
        gioi_tinh=user.gender,
        chuc_vu=user.position,
        dia_chi=user.address,
        email=user.email,
        trang_thai=user.status,
        mat_khau=hashed_password,
        so_dien_thoai=user.phone,
        thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # thoi_gian_cap_nhat=None,
        nguoi_tao=user.createdBy,
        vai_tro_id=user.roleID,
        truong_id=user.schoolID,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Cập nhật thông tin user
def update_user(db: Session, idUser: int, user: schemas.User, avatar_url: str):
    db_user = (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id_nguoi_dung == idUser)
        .first()
    )

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.username is not None:
        db_user.ho_ten = user.username
    if user.email is not None:
        db_user.email = user.email
    if user.birthday is not None:
        db_user.ngay_sinh = user.birthday
    if user.gender is not None:
        db_user.gioi_tinh = user.gender
    if user.position is not None:
        db_user.chuc_vu = user.position
    if user.address is not None:
        db_user.dia_chi = user.address
    if user.phone is not None:
        db_user.so_dien_thoai = user.phone
    if user.createdTime is not None:
        db_user.thoi_gian_tao = user.createdTime
    if user.roleID is not None:
        db_user.vai_tro_id = user.roleID
    if user.schoolID is not None:
        db_user.truong_id = user.schoolID

    if avatar_url is not None:
        db_user.anh_dai_dien = avatar_url

    db_user.thoi_gian_cap_nhat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    db.refresh(db_user)
    return db_user


# Lấy thông tin user theo username
def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.NguoiDung).filter(models.NguoiDung.ho_ten == username).first()
    )


# Lấy thông tin user theo email
def get_user_by_email(db: Session, email: str):
    user = (
        db.query(
            models.NguoiDung.id_nguoi_dung.label("idUser"),
            models.NguoiDung.ho_ten.label("username"),
            models.NguoiDung.anh_dai_dien.label("avatarUrl"),
            models.NguoiDung.email.label("email"),
            models.NguoiDung.mat_khau.label("password"),
            models.NguoiDung.chuc_vu.label("position"),
            models.NguoiDung.trang_thai.label("status"),
            models.NguoiDung.truong_id.label("schoolID"),
            models.NguoiDung.vai_tro_id.label("roleID"),
            models.VaiTro.ten_vai_tro.label("roleName"),
        )
        .join(models.VaiTro, models.NguoiDung.vai_tro_id == models.VaiTro.id_vai_tro)
        .filter(models.NguoiDung.email == email)
        .first()
    )

    if user is None:
        return None

    return user


# Xóa user theo ID
def delete_user(db: Session, user_id: int):
    db_user = (
        db.query(models.NguoiDung)
        .filter(models.NguoiDung.id_nguoi_dung == user_id)
        .first()
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


# Lấy danh sách users theo trường ID
def get_users_by_schoolId(db: Session, schoolId: int):
    return (
        db.query(models.NguoiDung).filter(models.NguoiDung.truong_id == schoolId).all()
    )


# Tìm kiếm theo bất kỳ trường nào
def search_user(db: Session, search: str):
    return (
        db.query(models.NguoiDung)
        .filter(
            models.NguoiDung.ho_ten.like(f"%{search}%")
            | models.NguoiDung.email.like(f"%{search}%")
            | models.NguoiDung.so_dien_thoai.like(f"%{search}%")
        )
        .all()
    )


# đặt lại mật khẩu
def reset_password(db: Session, idUser: str, new_password: str):
    user = get_user_by_id(db, idUser)
    if user is None:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    user.mat_khau = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


# Change password
def change_password(db: Session, idUser: int, old_password: str, new_password: str):
    user = get_user_by_id(db, idUser)
    if user is None:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    if not verify_password(old_password, user.mat_khau):
        raise HTTPException(status_code=401, detail="Mật khẩu cũ không chính xác")

    user.mat_khau = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user
