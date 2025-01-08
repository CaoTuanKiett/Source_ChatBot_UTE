from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.database import table_models as models
from app.schemas import Document
# from datetime import datetime


# Get all documents
def get_documents(db: Session, skip: int = 0, limit: int = 100):
    print("get_documents")
    # Query all documents from database
    documents = db.query(models.TaiLieu).offset(skip).limit(limit).all()

    # Convert SQLAlchemy objects to Pydantic schemas
    documents_dict = []
    for document in documents:
        document_dict = document.__dict__.copy()
        document_dict["thoi_gian_tao"] = document.thoi_gian_tao.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        documents_dict.append(Document(**document_dict))

    return documents_dict


# # Upload a document
def upload_document(db: Session, document: schemas.Document):
    print("upload_document")
    # Create a new document object
    new_document = models.TaiLieu(
        ten_tai_lieu=document.documentName,
        mo_ta=document.description,
        loai_tai_lieu=document.documentType,
        noi_dung=document.content,
        kieu_tai_lieu=document.dataType,
        pinecone_id=document.pineconeID,
        thu_muc_id=document.folderId,
        thoi_gian_tao=document.createdTime,
        them_boi=document.createdBy,
    )

    # Add the new document to the database
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document.id_tai_lieu


# # Get a document by ID
def get_document_by_id(db: Session, document_id: int):
    print("get_document_by_id")
    # Query the document by ID
    document = (
        db.query(models.TaiLieu)
        .filter(models.TaiLieu.id_tai_lieu == document_id)
        .first()
    )

    # If the document is not found, raise an HTTPException
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    # Convert SQLAlchemy object to Pydantic schema
    document_dict = document.__dict__.copy()
    document_dict["thoi_gian_tao"] = document.thoi_gian_tao.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return Document(**document_dict)


# # Delete a document by ID
def delete_document_by_id(db: Session, document_id: int):
    print("delete_document_by_id")
    # Query the document by ID
    document = (
        db.query(models.TaiLieu)
        .filter(models.TaiLieu.id_tai_lieu == document_id)
        .first()
    )

    # If the document is not found, raise an HTTPException
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    # Delete the document from the database
    db.delete(document)
    db.commit()
    return document


# Get Documents by Folder ID
def get_documents_by_folder_id(db: Session, folder_id: int, typeFile: int):
    print("get_documents_by_folder_id")
    # Query all documents by folder ID
    documents = (
        db.query(models.TaiLieu)
        .filter(models.TaiLieu.thu_muc_id == folder_id)
        .filter(models.TaiLieu.kieu_tai_lieu == typeFile)
        .all()
    )

    # Convert SQLAlchemy objects to Pydantic schemas
    documents_dict = []
    for document in documents:
        document_dict = document.__dict__.copy()

        # # Loại bỏ các trường không phải UTF-8
        # for key, value in document_dict.items():
        #     if isinstance(value, bytes):  # Xử lý dữ liệu nhị phân
        #         document_dict[key] = value.decode("utf-8", errors="ignore")

        if "noi_dung" in document_dict:
            del document_dict["noi_dung"]

        document_dict["thoi_gian_tao"] = document.thoi_gian_tao.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        # Thêm vào danh sách
        try:
            documents_dict.append(schemas.Document2(**document_dict))
        except Exception as e:
            print(f"Error serializing document: {document_dict}")
            raise e

    return documents_dict


# Update a document
def update_document(db: Session, document_id: int, document: schemas.Document):
    print("update_document")
    # Query the document by ID
    document_update = (
        db.query(models.TaiLieu)
        .filter(models.TaiLieu.id_tai_lieu == document_id)
        .first()
    )

    # If the document is not found, raise an HTTPException
    if not document_update:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    # Update the document
    if document.documentName:
        document_update.ten_tai_lieu = document.documentName
    if document.description:
        document_update.mo_ta = document.description
    if document.documentType:
        document_update.loai_tai_lieu = document.documentType
    if document.dataType:
        document_update.kieu_tai_lieu = document.dataType
    if document.pineconeID:
        document_update.pinecone_id = document.pineconeID
    if document.folderId:
        document_update.thu_muc_id = document.folderId
    if document.createdTime:
        document_update.thoi_gian_tao = document.createdTime
    if document.createdBy:
        document_update.them_boi = document.createdBy

    db.commit()
    db.refresh(document_update)
    return document_update
