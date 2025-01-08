from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import UploadFile


class User(BaseModel):
    idUser: Optional[int] = Field(alias="id_nguoi_dung", default=None)
    username: Optional[str] = Field(alias="ho_ten", default=None)
    avatarUrl: Optional[str] = Field(alias="anh_dai_dien", default=None)
    email: Optional[str] = None
    password: Optional[str] = Field(alias="mat_khau", default=None)
    birthday: Optional[str] = Field(alias="ngay_sinh", default=None)
    gender: Optional[str] = Field(alias="gioi_tinh", default=None)
    position: Optional[str] = Field(alias="chuc_vu", default=None)
    status: Optional[int] = Field(alias="trang_thai", default=None)
    address: Optional[str] = Field(alias="dia_chi", default=None)
    phone: Optional[int] = Field(alias="so_dien_thoai", default=None)
    createdTime: Optional[str] = Field(alias="thoi_gian_tao", default=None)
    createdBy: Optional[str] = Field(alias="nguoi_tao", default=None)
    updatedTime: Optional[str] = Field(alias="thoi_gian_cap_nhat", default=None)
    roleID: Optional[int] = Field(alias="vai_tro_id", default=None)
    schoolID: Optional[int] = Field(alias="truong_id", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class User2(BaseModel):
    id_nguoi_dung: Optional[int] = Field(alias="idUser", default=None)
    ho_ten: Optional[str] = Field(alias="username", default=None)
    anh_dai_dien: Optional[str] = Field(alias="avatarUrl", default=None)
    email: Optional[str] = None
    mat_khau: Optional[str] = Field(alias="password", default=None)
    ngay_sinh: Optional[str] = Field(alias="birthday", default=None)
    gioi_tinh: Optional[str] = Field(alias="birthday", default=None)
    chuc_vu: Optional[str] = Field(alias="position", default=None)
    trang_thai: Optional[int] = Field(alias="status", default=1)
    dia_chi: Optional[str] = Field(alias="address", default=None)
    so_dien_thoai: Optional[int] = Field(alias="phone", default=None)
    thoi_gian_tao: Optional[str] = Field(alias="createdTime", default=None)
    nguoi_tao: Optional[str] = Field(alias="createdBy", default=None)
    thoi_gian_cap_nhat: Optional[str] = Field(alias="updatedTime", default=None)
    vai_tro_id: Optional[int] = Field(alias="roleID", default=None)
    truong_id: Optional[int] = Field(alias="schoolID", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class UserResponse(BaseModel):
    message: str
    user: User2

    class Config:
        orm_mode = True
        from_attributes = True


class Role(BaseModel):
    idRole: Optional[int] = Field(alias="id_vai_tro", default=None)
    roleName: Optional[str] = Field(alias="ten_vai_tro", default=None)
    description: Optional[str] = Field(alias="mo_ta", default=None)
    createdTime: Optional[str] = Field(alias="thoi_gian_tao", default=None)
    updatedTime: Optional[str] = Field(alias="thoi_gian_cap_nhat", default=None)
    createdBy: Optional[str] = Field(alias="nguoi_tao", default=None)
    updatedBy: Optional[str] = Field(alias="nguoi_cap_nhat", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class Role2(BaseModel):
    id_vai_tro: Optional[int] = Field(alias="idRole", default=None)
    ten_vai_tro: Optional[str] = Field(alias="roleName", default=None)
    mo_ta: Optional[str] = Field(alias="description", default=None)
    thoi_gian_tao: Optional[str] = Field(alias="createdTime", default=None)
    thoi_gian_cap_nhat: Optional[str] = Field(alias="updatedTime", default=None)
    nguoi_tao: Optional[str] = Field(alias="createdBy", default=None)
    nguoi_cap_nhat: Optional[str] = Field(alias="updatedBy", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class RoleResponse(BaseModel):
    idRole: int
    message: str

    class Config:
        orm_mode = True
        from_attributes = True


class RoleWithUsersResponse(BaseModel):
    role: Role2
    users: List[User2]

    class Config:
        orm_mode = True
        from_attributes = True


class School(BaseModel):
    idSchool: Optional[int] = Field(alias="id_truong", default=None)
    schoolName: Optional[str] = Field(alias="ten_truong", default=None)
    schoolCode: Optional[str] = Field(alias="ma_truong", default=None)
    description: Optional[str] = Field(alias="mo_ta", default=None)
    avatarUrl: Optional[str] = Field(alias="anh_dai_dien", default=None)
    dateEstablished: Optional[str] = Field(alias="ngay_thanh_lap", default=None)
    address: Optional[str] = Field(alias="dia_chi", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    phone: Optional[int] = Field(alias="so_dien_thoai", default=None)
    website: Optional[str] = Field(alias="website", default=None)
    createdTime: Optional[str] = Field(alias="thoi_gian_tao", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class School2(BaseModel):
    id_truong: Optional[int] = Field(alias="idSchool", default=None)
    ten_truong: Optional[str] = Field(alias="schoolName", default=None)
    ma_truong: Optional[str] = Field(alias="schoolCode", default=None)
    mo_ta: Optional[str] = Field(alias="description", default=None)
    anh_dai_dien: Optional[str] = Field(alias="avatarUrl", default=None)
    ngay_thanh_lap: Optional[str] = Field(alias="dateEstablished", default=None)
    dia_chi: Optional[str] = Field(alias="address", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    so_dien_thoai: Optional[int] = Field(alias="phone", default=None)
    website: Optional[str] = Field(alias="website", default=None)
    thoi_gian_tao: Optional[str] = Field(alias="createdTime", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class SchoolResponse(BaseModel):
    schoolId: int
    schoolName: str
    message: str

    class Config:
        orm_mode = True
        from_attributes = True


# Model tin nhắn người dùng
class Message(BaseModel):
    idMessage: Optional[int] = Field(alias="id_tin_nhan", default=None)
    content: Optional[str] = Field(alias="noi_dung", default=None)
    sender: Optional[str] = Field(alias="nguoi_gui", default=None)
    sentTime: Optional[str] = Field(alias="thoi_gian_gui", default=None)
    threadId: Optional[int] = Field(alias="luong_id", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class TinNhan(BaseModel):
    idMessage: Optional[int] = Field(alias="id_tin_nhan", default=None)
    content: Optional[str] = Field(alias="noi_dung", default=None)
    sender: Optional[str] = Field(alias="nguoi_gui", default=None)
    sentTime: Optional[str] = Field(alias="thoi_gian_gui", default=None)
    threadId: Optional[int] = Field(alias="luong_id", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


# Model resquest tin nhắn
class MessageRequest(BaseModel):
    content: str
    sender: str
    threadId: int
    chatbotId: int

    class Config:
        orm_mode = True
        from_attributes = True


# class UserQuestion(BaseModel):
#     idQuestion: Optional[int] = Field(alias="id_cau_hoi")
#     fullName: Optional[str] = Field(alias="ho_ten")
#     question: Optional[str] = Field(alias="cau_hoi")
#     answer: Optional[str] = Field(alias="cau_tra_loi")
#     email: Optional[str] = Field(alias="email")
#     status: Optional[str] = Field(alias="trang_thai")
#     sentTime: Optional[str] = Field(alias="thoi_gian_tao")
#     answeredBy: Optional[str] = Field(alias="nguoi_tra_loi")
#     answeredTime: Optional[str] = Field(alias="thoi_gian_xu_ly")
#     chatBotID: Optional[int] = Field(alias="chat_bot_id")
#     chatbotName: Optional[str] = Field(alias="ten_chat_bot")

#     class Config:
#         orm_mode = True
#         from_attributes = True
#         populate_by_name = True


class UserQuestion2(BaseModel):
    id_cau_hoi: Optional[int] = Field(alias="idQuestion", default=None)
    ho_ten: Optional[str] = Field(alias="fullName", default=None)
    cau_hoi: Optional[str] = Field(alias="question", default=None)
    cau_tra_loi: Optional[str] = Field(alias="answer", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    trang_thai: Optional[str] = Field(alias="status", default=None)
    thoi_gian_tao: Optional[str] = Field(alias="sentTime", default=None)
    nguoi_tra_loi: Optional[str] = Field(alias="answeredBy", default=None)
    thoi_gian_xu_ly: Optional[str] = Field(alias="answeredTime", default=None)
    chat_bot_id: Optional[int] = Field(alias="chatBotID", default=None)
    ten_chat_bot: Optional[str] = Field(alias="chatbotName", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class UserQuestionResponse(BaseModel):
    idQuestion: int
    message: str

    class Config:
        orm_mode = True
        from_attributes = True


class Feedback(BaseModel):
    id_gop_y: Optional[int] = Field(alias="idFeedback", default=None)
    ho_ten: Optional[str] = Field(alias="fullName", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    noi_dung: Optional[str] = Field(alias="content", default=None)
    loai_gop_y: Optional[str] = Field(alias="feedbackType", default=None)
    trang_thai: Optional[str] = Field(alias="status", default=None)
    thoi_gian_tao: Optional[str] = Field(alias="createdTime", default=None)
    nguoi_xu_ly: Optional[str] = Field(alias="processedBy", default=None)
    thoi_gian_xu_ly: Optional[str] = Field(alias="processedTime", default=None)
    chat_bot_id: Optional[int] = Field(alias="chatBotID", default=None)
    ten_chat_bot: Optional[str] = Field(alias="chatbotName", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class ChatBot(BaseModel):
    idChatBot: Optional[int] = Field(alias="id_chat_bot", default=None)
    chatBotName: Optional[str] = Field(alias="ten_chat_bot", default=None)
    description: Optional[str] = Field(alias="mo_ta", default=None)
    folderId: Optional[int] = Field(alias="thu_muc_id", default=None)
    schoolId: Optional[int] = Field(alias="truong_id", default=None)
    token: Optional[str] = Field(alias="token", default=None)
    avatarUrl: Optional[str] = Field(alias="anh_dai_dien", default=None)
    status: Optional[int] = Field(alias="trang_thai", default=None)
    createdTime: Optional[str] = Field(alias="ngay_tao", default=None)
    updatedTime: Optional[str] = Field(alias="ngay_cap_nhat", default=None)
    createdBy: Optional[str] = Field(alias="them_boi", default=None)
    updateBy: Optional[str] = Field(alias="nguoi_cap_nhat", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class ChatBot2(BaseModel):
    id_chat_bot: Optional[int] = Field(alias="idChatBot", default=None)
    ten_chat_bot: Optional[str] = Field(alias="chatBotName", default=None)
    mo_ta: Optional[str] = Field(alias="description", default=None)
    thu_muc_id: Optional[int] = Field(alias="folderId", default=None)
    truong_id: Optional[int] = Field(alias="schoolId", default=None)
    token: Optional[str] = Field(alias="token", default=None)
    anh_dai_dien: Optional[str] = Field(alias="avatarUrl", default=None)
    trang_thai: Optional[int] = Field(alias="status", default=None)
    ngay_tao: Optional[str] = Field(alias="createdTime", default=None)
    ngay_cap_nhat: Optional[str] = Field(alias="updatedTime", default=None)
    them_boi: Optional[str] = Field(alias="createdBy", default=None)
    nguoi_cap_nhat: Optional[str] = Field(alias="updateBy", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class SearchData(BaseModel):
    searchValue: str
    schoolId: int

    class Config:
        orm_mode = True
        from_attributes = True


class Document(BaseModel):
    idDocument: Optional[int] = Field(alias="id_tai_lieu", default=None)
    documentName: Optional[str] = Field(alias="ten_tai_lieu", default=None)
    documentType: Optional[str] = Field(alias="loai_tai_lieu", default=None)
    dataType: Optional[int] = Field(alias="kieu_tai_lieu", default=None)
    content: Optional[bytes] = Field(alias="noi_dung", default=None)
    description: Optional[str] = Field(alias="mo_ta", default=None)
    pineconeID: Optional[str] = Field(alias="pinecone_id", default=None)
    folderId: Optional[int] = Field(alias="thu_muc_id", default=None)
    createdTime: Optional[str] = Field(alias="thoi_gian_tao", default=None)
    createdBy: Optional[str] = Field(alias="them_boi", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class Document2(BaseModel):
    id_tai_lieu: Optional[int] = Field(alias="idDocument", default=None)
    ten_tai_lieu: Optional[str] = Field(alias="documentName", default=None)
    loai_tai_lieu: Optional[str] = Field(alias="documentType", default=None)
    kieu_tai_lieu: Optional[int] = Field(alias="dataType", default=None)
    noi_dung: Optional[bytes] = Field(alias="content", default=None)
    mo_ta: Optional[str] = Field(alias="description", default=None)
    pinecone_id: Optional[str] = Field(alias="pineconeID", default=None)
    thu_muc_id: Optional[int] = Field(alias="folderId", default=None)
    thoi_gian_tao: Optional[str] = Field(alias="createdTime", default=None)
    them_boi: Optional[str] = Field(alias="createdBy", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class ResponseDocument(BaseModel):
    documentId: int
    pineconeId: str
    message: str

    class Config:
        orm_mode = True
        from_attributes = True


class RequestDocument(BaseModel):
    file: UploadFile
    folderId: int

    class Config:
        orm_mode = True
        from_attributes = True


class ChatBotData(BaseModel):
    idChatBotData: int = Field(alias="id_chat_bot_data")
    dataID: int = Field(alias="id_du_lieu")
    chatBotID: int = Field(alias="id_chat_bot")

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class Thread(BaseModel):
    idThread: int = Field(alias="id_luong")
    chatBotDataID: int = Field(alias="chat_bot_id")
    messageID: int = Field(alias="tin_nhan_id")

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class Config:
    orm_mode = True


class QuestionRequest(BaseModel):
    question: str
    document: str
    historyMessages: List[Message]

    class Config:
        orm_mode = True
        from_attributes = True


class GenerateResponse(BaseModel):
    answer: str

    class Config:
        orm_mode = True
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class LuongCreate(BaseModel):
    chat_bot_id: int = Field(alias="chatbotId")

    class Config:
        populate_by_name = True


class Luong(BaseModel):
    idLuong: Optional[int] = Field(alias="id_luong", default=None)
    chatbotId: Optional[int] = Field(alias="chat_bot_id", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class Folder(BaseModel):
    idFolder: Optional[int] = Field(alias="id_thu_muc", default=None)
    folderName: Optional[str] = Field(alias="ten_thu_muc", default=None)
    description: Optional[str] = Field(alias="mo_ta", default=None)
    createdTime: Optional[str] = Field(alias="ngay_tao", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class Folder2(BaseModel):
    id_thu_muc: Optional[int] = Field(alias="idFolder", default=None)
    ten_thu_muc: Optional[str] = Field(alias="folderName", default=None)
    mo_ta: Optional[str] = Field(alias="description", default=None)
    ngay_tao: Optional[str] = Field(alias="createdTime", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class FolderResponse(BaseModel):
    idFolder: int
    folderName: str
    description: Optional[str] = None
    message: str

    class Config:
        orm_mode = True
        from_attributes = True


class FolderAndDocuments(BaseModel):
    id_thu_muc: Optional[int] = Field(alias="idFolder", default=None)
    ten_thu_muc: Optional[str] = Field(alias="folderName", default=None)
    mo_ta: Optional[str] = Field(alias="description", default=None)
    ngay_tao: Optional[str] = Field(alias="createdTime", default=None)
    documents: List[Document2]

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True


class ResetPasswordRequest(BaseModel):
    new_password: str

    class Config:
        orm_mode = True
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    class Config:
        orm_mode = True
        from_attributes = True
