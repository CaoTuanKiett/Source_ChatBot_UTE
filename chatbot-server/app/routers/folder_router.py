from app import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import SessionLocal
from app.models import folder_model

router = APIRouter()


# Dependency để lấy session DB cho mỗi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all folders
@router.get("/folders", response_model=List[schemas.Folder2])
def get_folders(db: Session = Depends(get_db)):
    return folder_model.get_folders(db)


# Get folder by id
@router.get("/folder/{id_folder}", response_model=schemas.Folder)
def get_folder_by_id(id_folder: int, db: Session = Depends(get_db)):
    folder = folder_model.get_folder_by_id(db, id_folder)
    if folder is None:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


# Create folder
@router.post("/folder", response_model=schemas.FolderResponse)
def create_folder(folder: schemas.Folder, db: Session = Depends(get_db)):
    new_folder = folder_model.create_folder(db, folder)
    return {
        "idFolder": new_folder.id_thu_muc,
        "folderName": new_folder.ten_thu_muc,
        "description": new_folder.mo_ta,
        "message": "Folder created successfully",
    }


# Update folder
@router.put("/folder/{id_folder}", response_model=schemas.FolderResponse)
def update_folder(
    id_folder: int, folder: schemas.Folder, db: Session = Depends(get_db)
):
    folder_update = folder_model.update_folder(db, id_folder, folder)
    return {
        "idFolder": folder_update.id_thu_muc,
        "folderName": folder_update.ten_thu_muc,
        "description": folder_update.mo_ta,
        "message": "Folder updated successfully",
    }


# Delete folder
@router.delete("/folder/{id_folder}", response_model=schemas.FolderResponse)
def delete_folder(id_folder: int, db: Session = Depends(get_db)):
    folder_delete = folder_model.delete_folder(db, id_folder)
    return {
        "idFolder": folder_delete.id_thu_muc,
        "folderName": folder_delete.ten_thu_muc,
        "message": "Folder deleted successfully",
    }


# Lấy tất cả thư mục và tài liệu trong thư mục
@router.get("/folders_documents", response_model=List[schemas.FolderAndDocuments])
def get_folders_and_documents(db: Session = Depends(get_db)):
    return folder_model.get_folders_and_documents(db)


# Search document by all fields
@router.get(
    "/search/folders/documents/{search}",
    response_model=List[schemas.FolderAndDocuments],
)
def search_document_by_all_fields(search: str, db: Session = Depends(get_db)):
    return folder_model.search_document_by_all_fields(db, search)
