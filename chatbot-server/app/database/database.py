import pymysql
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lấy thông tin cấu hình từ các biến môi trường
# Lấy thông tin cấu hình từ các biến môi trường
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_USERNAME = settings.DB_USERNAME
DB_PASSWORD = settings.DB_PASSWORD
DB_NAME = settings.DB_NAME
DATABASE_URL = settings.DATABASE_URL

# URL kết nối tới MySQL
# DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# def database_exists(connection, db_name):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s", (db_name,))
#         exists = cursor.fetchone() is not None
#         logger.info("Database '%s' exists: %s", db_name, exists)
#         return exists

def database_exists(connection, db_name):
    logger.info("Checking if database '%s' exists.", db_name)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s", (db_name,))
            exists = cursor.fetchone() is not None
            logger.info("Database '%s' exists: %s", db_name, exists)
            return exists
    except Exception as e:
        logger.error("Error checking if database '%s' exists: %s", db_name, e)
        return False

# Tạo database nếu chưa tồn tại
def create_database_if_not_exists():
    connection = None
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )
        if database_exists(connection, DB_NAME):
            print(f"Database '{DB_NAME}' đã tồn tại.")
        else:
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Database '{DB_NAME}' đã được tạo thành công.")
    except Exception as e:
        print(f"Lỗi khi tạo database: {e}")  # Log thông báo lỗi
    finally:
        if connection:
            print("Đóng kết nối tới MySQL.")
            connection.close()

create_database_if_not_exists()

logger.info(f"DATABASE_URL: {DATABASE_URL}")
# Kết nối tới database
engine = create_engine(DATABASE_URL)
# Kiểm tra kết nối
try:
    with engine.connect() as connection:
        logger.info("Successfully connected to MySQL database")
except pymysql.OperationalError as e:
    logger.error(f"Failed to connect to MySQL database: {e}")
except Exception as e:
    logger.error(f"Unexpected error occurred while connecting to the database: {e}")

# # Đảm bảo kết nối đã thực hiện thành công
# logger.info(f"Engine: {engine}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency để lấy session kết nối
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
