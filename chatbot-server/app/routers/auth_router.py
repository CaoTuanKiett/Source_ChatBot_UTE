import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from app.config import settings
from app.database.database import SessionLocal
from app.models import user_model
from sqlalchemy.orm import Session
from app.schemas import LoginRequest
from app.utils.auth import create_access_token, create_refresh_token, verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RefreshTokenRequest(BaseModel):
    refreshToken: str


@router.post("/refresh-token")
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
        data = {
            "idUser": payload.get("idUser"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "avatarUrl": payload.get("avatarUrl"),
            "position": payload.get("position"),
            "roleID": payload.get("roleID"),
            "roleName": payload.get("roleName"),
            "schoolID": payload.get("schoolID"),
            "status": payload.get("status"),
        }

        if not data:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Tạo Access Token mới
        new_access_token = create_access_token(data=data)
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# Login
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    print("request", request)
    user = user_model.get_user_by_email(db, request.email)
    print("user", user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    data = {
        "idUser": user.idUser,
        "username": user.username,
        "avatarUrl": user.avatarUrl,
        "email": user.email,
        "position": user.position,
        "roleID": user.roleID,
        "roleName": user.roleName,
        "schoolID": user.schoolID,
        "status": user.status,
    }

    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)
    return {"access_token": access_token, "refreshToken": refresh_token}


# Logout
@router.post("/logout")
def logout():
    return {"message": "Logout successfully!"}
