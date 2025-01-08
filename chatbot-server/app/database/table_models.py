from sqlalchemy import (
    LargeBinary,
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import date, datetime

from app.database.database import Base


class ThuMuc(Base):
    __tablename__ = "thu_muc"
    id_thu_muc = Column(Integer, primary_key=True)
    ten_thu_muc = Column(String(255))
    mo_ta = Column(Text)
    ngay_tao = Column(String(255), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class TaiLieu(Base):
    __tablename__ = "tai_lieu"
    __table_args__ = {"extend_existing": True}
    id_tai_lieu = Column(Integer, primary_key=True)
    ten_tai_lieu = Column(String(255))
    loai_tai_lieu = Column(String(100))
    noi_dung = Column(LargeBinary)
    mo_ta = Column(Text)
    kieu_tai_lieu = Column(Integer)
    pinecone_id = Column(String(255))
    thu_muc_id = Column(Integer, ForeignKey("thu_muc.id_thu_muc", ondelete="CASCADE"))
    thoi_gian_tao = Column(DateTime, default=datetime.now)
    them_boi = Column(String(255))


class Truong(Base):
    __tablename__ = "Truong"
    id_truong = Column(Integer, primary_key=True)
    ten_truong = Column(String(255))
    ma_truong = Column(String(50))
    mo_ta = Column(Text)
    anh_dai_dien = Column(String(255))
    ngay_thanh_lap = Column(String(255))
    dia_chi = Column(String(255))
    email = Column(String(255))
    so_dien_thoai = Column(Integer)
    website = Column(String(255))
    thoi_gian_tao = Column(
        String(255), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class CauHoiNguoiDung(Base):
    __tablename__ = "cau_hoi_nguoi_dung"
    __table_args__ = {"extend_existing": True}
    id_cau_hoi = Column(Integer, primary_key=True)
    ho_ten = Column(String(255))
    email = Column(String(255))
    cau_hoi = Column(Text)
    cau_tra_loi = Column(Text)
    trang_thai = Column(String(50))
    thoi_gian_tao = Column(String(100))
    nguoi_tra_loi = Column(String(255))
    thoi_gian_xu_ly = Column(String(100))
    chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"))


class ChatBot(Base):
    __tablename__ = "chat_bot"
    __table_args__ = {"extend_existing": True}
    id_chat_bot = Column(Integer, primary_key=True)
    ten_chat_bot = Column(String(255))
    mo_ta = Column(Text)
    token = Column(Text)
    avatarUrl = Column(String(255))
    thu_muc_id = Column(Integer, ForeignKey("thu_muc.id_thu_muc"), nullable=True)
    truong_id = Column(Integer, ForeignKey("Truong.id_truong"), nullable=True)
    trang_thai = Column(Integer)
    ngay_tao = Column(
        String(100), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    ngay_cap_nhat = Column(String(100))
    them_boi = Column(String(255))
    nguoi_cap_nhat = Column(String(255))


class GopY(Base):
    __tablename__ = "gop_y"
    __table_args__ = {"extend_existing": True}
    id_gop_y = Column(Integer, primary_key=True)
    chat_bot_id = Column(Integer, ForeignKey("chat_bot.id_chat_bot"))
    ho_ten = Column(String(255))
    email = Column(String(255))
    noi_dung = Column(Text)
    loai_gop_y = Column(String(100))
    trang_thai = Column(String(50))
    thoi_gian_tao = Column(String(100))
    nguoi_xu_ly = Column(String(255))
    thoi_gian_xu_ly = Column(String(100))


class Luong(Base):
    __tablename__ = "luong"
    __table_args__ = {"extend_existing": True}
    id_luong = Column(Integer, primary_key=True)
    chat_bot_id = Column(
        Integer, ForeignKey("chat_bot.id_chat_bot", ondelete="SET NULL"), nullable=True
    )


class TinNhan(Base):
    __tablename__ = "tin_nhan"
    __table_args__ = {"extend_existing": True}
    id_tin_nhan = Column(Integer, primary_key=True)
    noi_dung = Column(Text)
    nguoi_gui = Column(String(255))
    luong_id = Column(Integer, ForeignKey("luong.id_luong"))
    thoi_gian_gui = Column(DateTime, default=datetime.now)


class VaiTro(Base):
    __tablename__ = "vai_tro"
    __table_args__ = {"extend_existing": True}
    id_vai_tro = Column(Integer, primary_key=True)
    ten_vai_tro = Column(String(255))
    mo_ta = Column(Text)
    thoi_gian_tao = Column(
        String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    thoi_gian_cap_nhat = Column(String(100))
    nguoi_tao = Column(String(255))
    nguoi_cap_nhat = Column(String(255))


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"
    __table_args__ = {"extend_existing": True}
    id_nguoi_dung = Column(Integer, primary_key=True)
    ho_ten = Column(String(255))
    anh_dai_dien = Column(Text)
    ngay_sinh = Column(String(100))
    gioi_tinh = Column(String(10))
    chuc_vu = Column(String(100))
    dia_chi = Column(String(255))
    trang_thai = Column(Integer)
    email = Column(String(255))
    mat_khau = Column(String(255))
    so_dien_thoai = Column(Integer)
    thoi_gian_tao = Column(
        String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    thoi_gian_cap_nhat = Column(String(100))
    nguoi_tao = Column(String(255))
    vai_tro_id = Column(Integer, ForeignKey("vai_tro.id_vai_tro"))
    truong_id = Column(Integer, ForeignKey("Truong.id_truong"))
