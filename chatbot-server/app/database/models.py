# # models.py
# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Boolean,
#     LargeBinary,
#     ForeignKey,
#     DateTime,
#     Index,
#     Text,
# )
# from app.database.database import Base
# from datetime import datetime

# # class Log(Base):
# #     __tablename__ = "logs"

# #     id = Column(Integer, primary_key=True, index=True)
# #     user_id = Column(Integer, ForeignKey("nguoi_dung.id_nguoi_dung"))
# #     action = Column(String(50), index=True)
# #     details = Column(String(255))
# #     timestamp = Column(DateTime, default=datetime.utcnow)


# class VaiTro(Base):
#     __tablename__ = "vai_tro"

#     id_vai_tro = Column(Integer, primary_key=True, index=True)
#     ten_vai_tro = Column(String(255), index=True)
#     mo_ta = Column(String(255), index=True)


# class User(Base):
#     __tablename__ = "nguoi_dung"

#     id_nguoi_dung = Column(Integer, primary_key=True, index=True)
#     ho_ten = Column(String(255), index=True)
#     ngay_sinh = Column(String(255), index=True)
#     gioi_tinh = Column(String(255), index=True)
#     chuc_vu = Column(String(255), index=True)
#     dia_chi = Column(String(255), index=True)
#     email = Column(String(255), unique=True, index=True)
#     mat_khau = Column(String(255), index=True)
#     so_dien_thoai = Column(String(255), index=True)
#     thoi_gian_tao = Column(String(255), index=True)
#     nguoi_tao = Column(String(255), index=True)
#     vai_tro_id = Column(Integer, ForeignKey("vai_tro.id_vai_tro"), index=True)


# class Truong(Base):
#     __tablename__ = "truong"

#     id_truong = Column(Integer, primary_key=True, index=True)
#     ten_truong = Column(String(255), index=True)
#     ma_truong = Column(String(255), index=True)
#     dia_chi = Column(String(255), index=True)
#     so_dien_thoai = Column(String(255), index=True)
#     email = Column(String(255), index=True)
#     website = Column(String(255), index=True)
#     nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id_nguoi_dung"), index=True)
#     chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"), index=True)
#     thoi_gian_tao = Column(String(255), index=True)


# class TinNhan(Base):
#     __tablename__ = "tin_nhan"

#     id_tin_nhan = Column(Integer, primary_key=True, index=True)
#     noi_dung = Column(String(255), index=True)
#     nguoi_gui = Column(String(255), index=True)
#     thoi_gian_gui = Column(String(255), index=True)
#     luong_id = Column(Integer, ForeignKey("luong.id_luong"), index=True)


# class CauHoiNguoiDung(Base):
#     __tablename__ = "cau_hoi_nguoi_dung"

#     id_cau_hoi = Column(Integer, primary_key=True, index=True)
#     ho_ten = Column(String(255), index=True)
#     email = Column(String(255), index=True)
#     cau_hoi = Column(String(255), index=True)
#     cau_tra_loi = Column(String(255), index=True)
#     thoi_gian_tao = Column(String(255), index=True)
#     nguoi_tra_loi = Column(String(255), index=True)
#     thoi_gian_tra_loi = Column(String(255), index=True)
#     trang_thai = Column(Boolean, index=True)
#     chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"), index=True)


# class GopY(Base):
#     __tablename__ = "gop_y"

#     id_gop_y = Column(Integer, primary_key=True, index=True)
#     ho_ten = Column(String(255), index=True)
#     email = Column(String(255), index=True)
#     noi_dung = Column(String(255), index=True)
#     loai_gop_y = Column(String(255), index=True)
#     ghi_chu = Column(String(255), index=True)
#     thoi_gian_tao = Column(String(255), index=True)
#     trang_thai = Column(Boolean, index=True)
#     chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"), index=True)


# class TaiLieu(Base):
#     __tablename__ = "tai_lieu"

#     id_tai_lieu = Column(Integer, primary_key=True, index=True)
#     ten_tai_lieu = Column(String(255), index=True)
#     loai_tai_lieu = Column(String(255), index=True)
#     mo_ta = Column(String(255), index=True)
#     pinecone_id = Column(String(255), index=True)
#     thoi_gian_tao = Column(String(255), index=True)
#     them_boi = Column(String(255), index=True)


# class ChatBot(Base):
#     __tablename__ = "chat_bot"

#     id_chat_bot = Column(Integer, primary_key=True, index=True)
#     ten_chat_bot = Column(String(255), index=True)
#     mo_ta = Column(String(255), index=True)
#     trang_thai = Column(String(255), index=True)
#     # cau_hoi_id = Column(
#     #     Integer, ForeignKey("cau_hoi_nguoi_dung.id_cau_hoi"), index=True
#     # )
#     # gop_y_id = Column(Integer, ForeignKey("gop_y.id_gop_y"), index=True)


# class DuLieuChatBot(Base):
#     __tablename__ = "tai_lieu_chat_bot"

#     id_tai_lieu_chat_bot = Column(Integer, primary_key=True, index=True)
#     tai_lieu_id = Column(Integer, ForeignKey("tai_lieu.id_tai_lieu"), index=True)
#     chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"), index=True)


# class Luong(Base):
#     __tablename__ = "luong"

#     id_luong = Column(Integer, primary_key=True, index=True)
#     chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"), index=True)


# # class Link(Base):
# #     __tablename__ = "link"

# #     id_link = Column(Integer, primary_key=True, index=True)
# #     link = Column(String(255), index=True)
# #     thoi_gian_tao = Column(String(255), index=True)
# #     nguoi_tao = Column(String(255), index=True)

# # class TaiLieu(Base):
# #     __tablename__ = "tai_lieu"

# #     id_tai_lieu = Column(Integer, primary_key=True, index=True)
# #     ten_tai_lieu = Column(String(255), index=True)
# #     loai_tai_lieu = Column(String(255), index=True)
# #     kich_thuoc = Column(String(255), index=True)
# #     du_lieu = Column(LargeBinary, nullable=False)

# # class CauHoi(Base):
# #     __tablename__ = "cau_hoi"

# #     id_cau_hoi = Column(Integer, primary_key=True, index=True)
# #     cau_hoi = Column(String(255), index=True)
# #     cau_tra_loi = Column(String(255), index=True)
# #     thoi_gian_tao = Column(String(255), index=True)
# #     nguoi_tao = Column(String(255), index=True)

# # class VanBan(Base):
# #     __tablename__ = "van_ban"

# #     id_van_ban = Column(Integer, primary_key=True, index=True)
# #     noi_dung = Column(String(255), index=True)
# #     thoi_gian_tao = Column(String(255), index=True)
# #     nguoi_tao = Column(String(255), index=True)
