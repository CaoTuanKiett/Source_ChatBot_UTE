import sys
import os

# Thêm đường dẫn tới thư mục gốc của dự án
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import SessionLocal
from app.database.table_models import (
    VaiTro,
    NguoiDung,
    # Truong,
    # TinNhan,
    # CauHoiNguoiDung,
    # GopY,
    # TaiLieu,
    # ChatBot,
    # DuLieuChatBot,
    # Luong,
)


# Hàm khởi tạo dữ liệu mẫu
def init_db():
    # Tạo phiên làm việc với cơ sở dữ liệu
    db = SessionLocal()

    # Tạo dữ liệu mẫu cho bảng VaiTro
    vai_tro = [
        VaiTro(ten_vai_tro="Quản trị viên", mo_ta="Quản trị viên của trường"),
        VaiTro(
            ten_vai_tro="Cán bộ quản lý tuyển sinh",
            mo_ta="Cán bộ quản lý tuyển sinh chịu trách nhiệm về việc quản lý tuyển sinh (Trả lời câu hỏi, hỗ trợ tuyển sinh, Xử lý góp ý) và Cập nhật tài liệu",
        ),
        VaiTro(
            ten_vai_tro="Cán bộ quản lý tài liệu",
            mo_ta="Cán bộ quản lý tài liệu chịu trách nhiệm về việc quản lý tài liệu",
        ),
        VaiTro(
            ten_vai_tro="Quản trị viên hệ thống",
            mo_ta="Quản trị viên của hệ thông",
        ),
    ]

    # Tạo dữ liệu mẫu cho bảng User
    users = [
        NguoiDung(
            ho_ten="admin",
            ngay_sinh="1990-01-01",
            gioi_tinh="Nam",
            chuc_vu="admin",
            dia_chi="Hà Nội",
            email="admin@gmail.com",
            mat_khau="123456",
            so_dien_thoai="123456789",
            thoi_gian_tao="2024-01-01",
            nguoi_tao="admin",
            vai_tro_id=1,
        )
    ]

    # # Tạo dữ liệu mẫu cho bảng TinNhan
    # tin_nhans = [
    #     TinNhan(noi_dung="Tin nhắn 1", thoi_gian_gui="2024-01-01 08:00:00", nguoi_gui_id=1),
    #     TinNhan(noi_dung="Tin nhắn 2", thoi_gian_gui="2024-01-02 09:00:00", nguoi_gui_id=2),
    #     TinNhan(noi_dung="Tin nhắn 3", thoi_gian_gui="2024-01-03 10:00:00", nguoi_gui_id=3),
    #     TinNhan(noi_dung="Tin nhắn 4", thoi_gian_gui="2024-01-04 11:00:00", nguoi_gui_id=4),
    #     TinNhan(noi_dung="Tin nhắn 5", thoi_gian_gui="2024-01-05 12:00:00", nguoi_gui_id=5)
    # ]

    # Tạo dữ liệu mẫu cho bảng ChatBot
    # chat_bots = [
    #     ChatBot(
    #         ten_chat_bot="ChatBot 1",
    #         mo_ta="Hỗ trợ sinh viên",
    #         # thu_muc_id=1,
    #         # truong_id=1,
    #         trang_thai="Active",
    #         ngay_tao="2024-01-01",
    #         ngay_cap_nhat="2024-01-01",
    #         nguoi_tao="admin",
    #         nguoi_cap_nhat="admin",
    #     ),
    #     ChatBot(
    #         ten_chat_bot="ChatBot 2",
    #         mo_ta="Hỗ trợ giảng viên",
    #         # thu_muc_id=2,
    #         # truong_id=2,
    #         trang_thai="Active",
    #         ngay_tao="2024-01-01",
    #         ngay_cap_nhat="2024-01-01",
    #         nguoi_tao="admin",
    #         nguoi_cap_nhat="admin",
    #     ),
    #     ChatBot(
    #         ten_chat_bot="ChatBot 3",
    #         mo_ta="Hỗ trợ cán bộ",
    #         # thu_muc_id=3,
    #         # truong_id=3,
    #         trang_thai="Active",
    #         ngay_tao="2024-01-01",
    #         # ngay_cap_nhat="2024-01-01",
    #         nguoi_tao="admin",
    #         # nguoi_cap_nhat="admin",
    #     ),
    # ]

    # # Tạo dữ liệu mẫu cho bảng NguoiGui
    # nguoi_guis = [
    #     NguoiGui(nguoi_gui="Nguyen Van A"),
    #     NguoiGui(nguoi_gui="Tran Thi B"),
    #     NguoiGui(nguoi_gui="Le Minh C"),
    #     NguoiGui(nguoi_gui="Pham Thi D"),
    #     NguoiGui(nguoi_gui="Vu Thi E")
    # ]

    # # Tạo dữ liệu mẫu cho bảng CauHoiNguoiDung
    # cau_hoi_nguoi_dungs = [
    #     CauHoiNguoiDung(ho_ten="Nguyen Van A", noi_dung="Câu hỏi 1", email="nguyenvana@example.com", trang_thai=True, thoi_gian_gui="2024-01-01"),
    #     CauHoiNguoiDung(ho_ten="Tran Thi B", noi_dung="Câu hỏi 2", email="tranthib@example.com", trang_thai=False, thoi_gian_gui="2024-01-02"),
    #     CauHoiNguoiDung(ho_ten="Le Minh C", noi_dung="Câu hỏi 3", email="leminhc@example.com", trang_thai=True, thoi_gian_gui="2024-01-03"),
    #     CauHoiNguoiDung(ho_ten="Pham Thi D", noi_dung="Câu hỏi 4", email="phamthid@example.com", trang_thai=False, thoi_gian_gui="2024-01-04"),
    #     CauHoiNguoiDung(ho_ten="Vu Thi E", noi_dung="Câu hỏi 5", email="vuthie@example.com", trang_thai=True, thoi_gian_gui="2024-01-05")
    # ]

    # # Tạo dữ liệu mẫu cho bảng GopY
    # gop_ys = [
    #     GopY(ho_ten="Nguyen Van A", noi_dung="Góp ý 1", email="nguyenvana@example.com", thoi_gian_gui="2024-01-01"),
    #     GopY(ho_ten="Tran Thi B", noi_dung="Góp ý 2", email="tranthib@example.com", thoi_gian_gui="2024-01-02"),
    #     GopY(ho_ten="Le Minh C", noi_dung="Góp ý 3", email="leminhc@example.com", thoi_gian_gui="2024-01-03"),
    #     GopY(ho_ten="Pham Thi D", noi_dung="Góp ý 4", email="phamthid@example.com", thoi_gian_gui="2024-01-04"),
    #     GopY(ho_ten="Vu Thi E", noi_dung="Góp ý 5", email="vuthie@example.com", thoi_gian_gui="2024-01-05")
    # ]

    # # Tạo dữ liệu mẫu cho bảng Truong
    # truong_list = [
    #     Truong(
    #         ten_truong="Trường Đại học Công nghệ Thông tin",
    #         ma_truong="UDN-IT",
    #         dia_chi="123 Đại lộ Công Nghệ, Đà Nẵng",
    #         so_dien_thoai="0236-1234567",
    #         email="contact@udn.edu.vn",
    #         website="https://www.udn.edu.vn",
    #         nguoi_dung_id=1,
    #         chat_bot_id=1,
    #         thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     ),
    #     Truong(
    #         ten_truong="Trường Đại học Bách Khoa Hà Nội",
    #         ma_truong="HUST",
    #         dia_chi="1 Đại Cồ Việt, Hà Nội",
    #         so_dien_thoai="024-38695131",
    #         email="contact@hust.edu.vn",
    #         website="https://www.hust.edu.vn",
    #         nguoi_dung_id=1,
    #         chat_bot_id=1,
    #         thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     ),
    #     Truong(
    #         ten_truong="Trường Đại học Kinh tế Quốc dân",
    #         ma_truong="NEU",
    #         dia_chi="207 Giải Phóng, Hà Nội",
    #         so_dien_thoai="024-37548620",
    #         email="contact@neu.edu.vn",
    #         website="https://www.neu.edu.vn",
    #         nguoi_dung_id=1,
    #         chat_bot_id=1,
    #         thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     ),
    #     Truong(
    #         ten_truong="Trường Đại học Sư phạm Hà Nội",
    #         ma_truong="HUPT",
    #         dia_chi="136 Xuân Thủy, Hà Nội",
    #         so_dien_thoai="024-37548596",
    #         email="contact@hup.edu.vn",
    #         website="https://www.hup.edu.vn",
    #         nguoi_dung_id=1,
    #         chat_bot_id=1,
    #         thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     ),
    #     Truong(
    #         ten_truong="Trường Đại học Ngoại thương",
    #         ma_truong="FTU",
    #         dia_chi="91 Chùa Láng, Hà Nội",
    #         so_dien_thoai="024-37541517",
    #         email="contact@ftu.edu.vn",
    #         website="https://www.ftu.edu.vn",
    #         nguoi_dung_id=1,
    #         chat_bot_id=1,
    #         thoi_gian_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     ),
    # ]

    # Lặp qua và thêm dữ liệu vào cơ sở dữ liệu
    # db.add_all(vai_tro + quyens + users + nguoi_guis + tin_nhans + chat_bots + cau_hoi_nguoi_dungs + gop_ys)
    db.add_all(vai_tro)
    # db.add_all(chat_bots)
    # db.add_all(users)
    db.flush()
    db.commit()

    print("Dữ liệu mẫu đã được thêm thành công!")

    # Đóng kết nối
    db.close()


# Gọi hàm init_db để khởi tạo dữ liệu
if __name__ == "__main__":
    init_db()
