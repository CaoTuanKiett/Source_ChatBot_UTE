import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from app.config import settings

# Khóa bí mật cho JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Mã hóa mật khẩu
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# Kiểm tra mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# Tạo JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Giải mã JWT
def decode_access_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token hết hạn")
    except jwt.InvalidTokenError:
        raise Exception("Token không hợp lệ")


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Kiểm tra quyền người dùng (ví dụ: chỉ cho phép Admin cập nhật)
def check_admin_permission(role_id: int = Depends(verify_access_token)):
    if role_id != 1:  # Giả sử roleID=1 là Admin
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update user",
        )


# Tạo token cho chatbot
def create_chatbot_token(chatbot: dict):
    """
    Tạo token cho chatbot từ thông tin chatbot.
    """
    payload = {
        "id": chatbot["id_chat_bot"],
        "name": chatbot["ten_chat_bot"],
        "description": chatbot["mo_ta"],
        "folder_id": chatbot["thu_muc_id"],
        "school_id": chatbot["truong_id"],
        "created_at": chatbot["ngay_tao"],
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
