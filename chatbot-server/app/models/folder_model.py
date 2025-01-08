from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import table_models as models
from datetime import datetime
from sqlalchemy.exc import IntegrityError


# Lấy danh sách thư mục
def get_folders(db: Session):
    folders = db.query(models.ThuMuc).all()

    # Convert SQLAlchemy objects to Pydantic schemas
    folders_dict = []
    for folder in folders:
        folder_dict = folder.__dict__.copy()
        # folder_dict["ngay_tao"] = folder.ngay_tao.strftime("%Y-%m-%d %H:%M:%S")
        folders_dict.append(schemas.Folder2(**folder_dict))

    return folders_dict


# Lấy thông tin thư mục theo id
def get_folder_by_id(db: Session, id_folder: int):
    folder = (
        db.query(models.ThuMuc).filter(models.ThuMuc.id_thu_muc == id_folder).first()
    )

    # Convert SQLAlchemy objects to Pydantic schemas
    folder_dict = folder.__dict__.copy()
    # folder_dict["ngay_tao"] = folder.ngay_tao.strftime("%Y-%m-%d %H:%M:%S")

    return schemas.Folder(**folder_dict)


# Thêm thư mục
def create_folder(db: Session, folder: schemas.Folder):
    new_folder = models.ThuMuc(
        ten_thu_muc=folder.folderName,
        mo_ta=folder.description,
        ngay_tao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    return new_folder


# Cập nhật thông tin thư mục
def update_folder(db: Session, id_folder: int, folder: schemas.Folder):
    folder_update = (
        db.query(models.ThuMuc).filter(models.ThuMuc.id_thu_muc == id_folder).first()
    )

    if folder_update is None:
        raise HTTPException(status_code=404, detail="Folder not found")

    if folder.folderName:
        folder_update.ten_thu_muc = folder.folderName
    if folder.description:
        folder_update.mo_ta = folder.description

    db.commit()
    db.refresh(folder_update)
    return folder_update


# Xóa thư mục
# def delete_folder(db: Session, id_folder: int):
#     folder_delete = (
#         db.query(models.ThuMuc).filter(models.ThuMuc.id_thu_muc == id_folder).first()
#     )
#     if folder_delete is None:
#         raise HTTPException(status_code=404, detail="Folder not found")
#     db.delete(folder_delete)
#     db.commit()
#     return folder_delete


def delete_folder(db: Session, id_folder: int):
    # Tìm thư mục cần xóa
    folder_delete = (
        db.query(models.ThuMuc).filter(models.ThuMuc.id_thu_muc == id_folder).first()
    )
    if folder_delete is None:
        raise HTTPException(status_code=404, detail="Thư mục không tồn tại")

    # Kiểm tra xem thư mục có đang được sử dụng hay không
    related_data = (
        db.query(models.ChatBot).filter(models.ChatBot.thu_muc_id == id_folder).first()
    )
    if related_data:
        raise HTTPException(
            status_code=400, detail="Thư mục đang được sử dụng, không thể xóa"
        )

    # Xóa thư mục nếu không bị ràng buộc
    try:
        db.delete(folder_delete)
        db.commit()
    except IntegrityError as e:
        # Bắt lỗi nếu có ràng buộc khác chưa xử lý
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Không thể xóa thư mục do ràng buộc khóa ngoại"
        )

    return folder_delete


# Lấy tất cả thư mục và tài liệu trong thư mục
def get_folders_and_documents(db: Session):
    folders = db.query(models.ThuMuc).all()
    folders_dict = []
    for folder in folders:
        folder_dict = folder.__dict__.copy()
        documents = (
            db.query(models.TaiLieu)
            .filter(models.TaiLieu.thu_muc_id == folder.id_thu_muc)
            .all()
        )
        documents_dict = []
        for document in documents:
            document_dict = document.__dict__.copy()

            if "noi_dung" in document_dict:
                del document_dict["noi_dung"]

            document_dict["thoi_gian_tao"] = document.thoi_gian_tao.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            documents_dict.append(schemas.Document2(**document_dict))
        folder_dict["documents"] = documents_dict

        folders_dict.append(schemas.FolderAndDocuments(**folder_dict))
    return folders_dict


# Search document by all fields
def search_document_by_all_fields(db: Session, search: str):
    folders = db.query(models.ThuMuc).all()
    folders_dict = []
    for folder in folders:
        folder_dict = folder.__dict__.copy()
        documents = (
            db.query(models.TaiLieu)
            .filter(models.TaiLieu.thu_muc_id == folder.id_thu_muc)
            .filter(
                models.TaiLieu.ten_tai_lieu.like(f"%{search}%")
                | models.TaiLieu.mo_ta.like(f"%{search}%")
                | models.TaiLieu.thoi_gian_tao.like(f"%{search}%")
                | models.TaiLieu.them_boi.like(f"%{search}%")
                | models.TaiLieu.loai_tai_lieu.like(f"%{search}%")
            )
            .all()
        )
        documents_dict = []
        for document in documents:
            document_dict = document.__dict__.copy()
            document_dict["thoi_gian_tao"] = document.thoi_gian_tao.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            documents_dict.append(schemas.Document2(**document_dict))
        folder_dict["documents"] = documents_dict

        folders_dict.append(schemas.FolderAndDocuments(**folder_dict))

    return folders_dict
