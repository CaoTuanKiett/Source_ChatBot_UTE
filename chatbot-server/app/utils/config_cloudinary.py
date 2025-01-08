import os
import shutil
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from fastapi import HTTPException

from app.config import settings

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,  # Thay bằng Cloud Name của bạn
    api_key=settings.CLOUDINARY_API_KEY,  # Thay bằng API Key của bạn
    api_secret=settings.CLOUDINARY_API_SECRET,  # Thay bằng API Secret của bạn
)

print(cloudinary.config().api_secret)


def upload_to_cloudinary(file):
    """
    Upload file lên Cloudinary.
    """
    print("upload_to_cloudinary", file)
    try:
        result = upload(file, folder="chatbot")  # Lưu vào thư mục "chatbots/avatars"
        return result.get("secure_url")  # Trả về URL an toàn của ảnh
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None


def handle_logic_cover_image(file):
    avatar_url = None
    # Nếu có file được upload
    if file:
        if file.content_type not in [
            "image/jpeg",
            "image/png",
            "image/jpg",
            "image/gif",
        ]:
            raise HTTPException(
                status_code=400, detail="Invalid file type. Only JPEG or PNG allowed."
            )

        # Lưu tạm file vào máy
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Upload ảnh lên Cloudinary
        avatar_url = upload_to_cloudinary(temp_file_path)

        # Xóa file tạm sau khi upload
        os.remove(temp_file_path)

        if not avatar_url:
            raise HTTPException(
                status_code=500, detail="Failed to upload avatar to Cloudinary"
            )
    return avatar_url
