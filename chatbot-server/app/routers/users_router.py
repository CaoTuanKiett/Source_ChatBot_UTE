import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from app.database.database import SessionLocal
from app.models import user_model
from app.utils.config_cloudinary import handle_logic_cover_image, upload_to_cloudinary

router = APIRouter()


# Dependency để lấy session DB cho mỗi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## Get all users
@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    listUsers = user_model.get_users(db, skip=skip, limit=limit)
    # print("listUsers", listUsers)
    # if not listUsers:
    #     raise HTTPException(status_code=404, detail="User not found")
    return listUsers


## Get user by ID
@router.get("/user/{user_id}", response_model=schemas.User2)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_model.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # return db_user
    return schemas.User2.model_validate(db_user)


## Update user
@router.put("/user/{user_id}", response_model=schemas.User2)
def update_user(
    user_id: int,
    user: str = Form(...),
    fileAvt: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Giải mã chuỗi JSON thành object
        user_data = json.loads(user)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for user")

    # Chuyển dữ liệu sang schema User
    user_obj = schemas.User(**user_data)

    # Xử lý ảnh đại diện
    avatar_url = handle_logic_cover_image(fileAvt)

    db_user = user_model.update_user(db, user_id, user_obj, avatar_url)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Create user
@router.post("/user/", response_model=schemas.UserResponse)
def create_user(
    # user: schemas.User,
    user: str = Form(...),
    fileAvt: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Giải mã chuỗi JSON thành object
        user_data = json.loads(user)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for user")

    # Chuyển dữ liệu sang schema User
    user_obj = schemas.User(**user_data)
    print("user_obj", user_obj)

    # Xử lý ảnh đại diện
    avatar_url = handle_logic_cover_image(fileAvt)

    try:
        created_user = user_model.create_user(
            db=db, user=user_obj, avatar_url=avatar_url
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Unable to create user: " + str(e),
        )

    return schemas.UserResponse(message="User created successfully!", user=created_user)


# @router.post("/user/")
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     result = user_model.create_user(db=db, user=user)
#     return {"message": "User created successfully", "user": result}


## Delete user
@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_model.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": db_user.id_nguoi_dung, "message": "User deleted successfully"}


# Lấy danh sách users theo trường ID
@router.get("/users/school/{schoolId}", response_model=List[schemas.User2])
def get_users_by_schoolId(schoolId: int, db: Session = Depends(get_db)):
    listUsers = user_model.get_users_by_schoolId(db, schoolId)

    return listUsers


# Tìm kiếm theo bất kỳ trường nào
@router.get("/users/search/{search}", response_model=List[schemas.User2])
def search_user(search: str, db: Session = Depends(get_db)):
    listUsers = user_model.search_user(db, search)

    return listUsers


# đặt lại mật khẩu
@router.post("/user/reset-password/{idUser}", response_model=schemas.UserResponse)
def reset_password(
    idUser: str, request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)
):
    user = user_model.reset_password(db, idUser, request.new_password)
    return schemas.UserResponse(message="Password reset successfully!", user=user)


# Change password
@router.post("/user/change-password/{idUser}", response_model=schemas.UserResponse)
def change_password(
    idUser: int, request: schemas.ChangePasswordRequest, db: Session = Depends(get_db)
):
    user = user_model.change_password(
        db, idUser, request.old_password, request.new_password
    )
    return schemas.UserResponse(message="Password changed successfully!", user=user)
