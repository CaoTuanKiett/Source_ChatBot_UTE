import sys
import os

# Thêm đường dẫn tới thư mục gốc của dự án
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import engine, Base
# from app.database.models import (
#     VaiTro,
#     User,
#     Truong,
#     TinNhan,
#     CauHoiNguoiDung,
#     GopY,
#     TaiLieu,
#     ChatBot,
#     DuLieuChatBot,
#     Luong,
# )

from app.database.table_models import (
    ThuMuc,
    TaiLieu,
    Truong,
    ChatBot,
    CauHoiNguoiDung,
    GopY,
    Luong,
    TinNhan,
    VaiTro,
    NguoiDung,
)


# Tạo các bảng
def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Các bảng đã được tạo thành công!")
