# # from pydantic import BaseSettings
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()


# class Settings(BaseSettings):
    
#     GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
#     GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME")
#     GEMINI_TEMPERATURE: float = os.getenv("GEMINI_TEMPERATURE", 0.7)
#     GEMINI_MAX_TOKENS: int = os.getenv("GEMINI_MAX_TOKENS", 300)
#     GEMINI_TOP_P: float = os.getenv("GEMINI_TOP_P", 0.8)
#     GEMINI_TOP_K: int = os.getenv("GEMINI_TOP_K", 50)
#     GEMINI_RESPONSE_TYPE: str = os.getenv("GEMINI_RESPONSE_TYPE", "text/plain")
#     DB_USERNAME: str = os.getenv("DB_USERNAME")
#     DB_PASSWORD: str = os.getenv("DB_PASSWORD")
#     DB_HOST: str = os.getenv("DB_HOST")
#     DB_NAME: str = os.getenv("DB_NAME")
#     DB_PORT: str = os.getenv("DB_PORT", "3306")
#     PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
#     PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT")
#     PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME")
#     OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
#     SECRET_KEY: str = os.getenv("SECRET_KEY")
#     ALGORITHM: str = os.getenv("ALGORITHM")
#     MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
#     MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
#     MAIL_FROM: str = os.getenv("MAIL_FROM")
#     MAIL_PORT: int = os.getenv("MAIL_PORT")
#     MAIL_SERVER: str = os.getenv("MAIL_SERVER")
#     MAIL_TLS: bool = os.getenv("MAIL_TLS")
#     MAIL_SSL: bool = os.getenv("MAIL_SSL")
#     CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME")
#     CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY")
#     CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET")
#     API_VERSION: str = os.getenv("API_VERSION")
#     MAX_CHUNK_SIZE: int = os.getenv("MAX_CHUNK_SIZE", 400)
#     OVERLAP_SIZE: int = os.getenv("OVERLAP_SIZE", 100)

#     class Config:
#         # Load environment variables from .env file automatically
#         env_file = ".env"
#         env_file_encoding = "utf-8"


# # Create an instance of Settings to use in the application
# settings = Settings()

   
# print(f"Settings loaded: {Settings.__fields_set__}")


from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Nạp các biến môi trường từ file .env
load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", 0.7))
    GEMINI_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", 300))
    GEMINI_TOP_P: float = float(os.getenv("GEMINI_TOP_P", 0.8))
    GEMINI_TOP_K: int = int(os.getenv("GEMINI_TOP_K", 50))
    GEMINI_RESPONSE_TYPE: str = os.getenv("GEMINI_RESPONSE_TYPE", "text/plain")
    DATABASE_URL: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    OPENAI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))  # Giá trị mặc định nếu không có
    MAIL_SERVER: str
    MAIL_TLS: bool = os.getenv("MAIL_TLS", "true").lower() == "true"
    MAIL_SSL: bool = os.getenv("MAIL_SSL", "false").lower() == "false"
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    API_VERSION: str
    MAX_CHUNK_SIZE: int = int(os.getenv("MAX_CHUNK_SIZE", 400))
    OVERLAP_SIZE: int = int(os.getenv("OVERLAP_SIZE", 100))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Tạo một instance của Settings để sử dụng trong ứng dụng
try:
    settings = Settings()
    # print(f"Settings loaded: {settings.__fields_set__}")
except Exception as e:
    print(f"Error loading settings: {e}")
