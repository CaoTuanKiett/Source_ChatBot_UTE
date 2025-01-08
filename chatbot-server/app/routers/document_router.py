from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import urllib
from app import schemas
from typing import List, Optional
from app.database.database import SessionLocal
from app.models import document_model
import uuid
from app.gemini_api.genai_model import embed_text
import os
from datetime import datetime
from app.utils.config_link import crawl_data
from app.utils.file_processing import process_file, split_text_into_chunks
from app.utils.config_pinecone import get_pinecone
from app.config import settings

MAX_CHUNK_SIZE = settings.MAX_CHUNK_SIZE
OVERLAP_SIZE = settings.OVERLAP_SIZE

# Create a new router
router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all documents
@router.get("/documents/", response_model=List[schemas.Document])
def get_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    listDocument = document_model.get_documents(db, skip=skip, limit=limit)
    if not listDocument:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    return listDocument


# # Upload multiple documents
# @router.post("/documents/")
# def upload_documents(
#     files: List[UploadFile],
#     folderId: int = Form(...),
#     description: str = Form(...),
#     createdBy: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files provided")

#     print("folderId", folderId)
#     uploaded_documents = []
#     temp_dir = "temp"
#     os.makedirs(temp_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

#     namespace = str(folderId)

#     for file in files:
#         temp_file_path = os.path.join(temp_dir, str(uuid.uuid4()))
#         try:
#             # Trích xuất nội dung file
#             chunks = process_file(file, temp_file_path)

#             # # Tạo vector từ nội dung và lưu vào Pinecone
#             # vector = embed_text(text)
#             # vector_id = str(uuid.uuid4())

#             # Kết nối Pinecone
#             index = get_pinecone()
#             # Tạo vector và lưu vào Pinecone
#             for chunk in chunks:
#                 vector = embed_text(chunk)
#                 vector_id = str(uuid.uuid4())

#                 index.upsert(
#                     [(vector_id, vector, {"text": chunk, "filename": file.filename})],
#                     namespace=namespace,
#                 )

#             # Tạo đối tượng tài liệu
#             document = schemas.Document(
#                 ten_tai_lieu=file.filename,
#                 loai_tai_lieu=file.content_type,
#                 mo_ta=description,
#                 pinecone_id="vector_id",  ###
#                 thu_muc_id=folderId,
#                 thoi_gian_tao=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
#                 them_boi=createdBy,
#             )

#             # Upload tài liệu vào database
#             document_model_new = document_model.upload_document(db, document)
#             uploaded_documents.append(document_model_new)
#         except Exception as e:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Error processing file {file.filename}: {str(e)}",
#             )
#         finally:
#             # Xóa file tạm nếu tồn tại
#             if os.path.exists(temp_file_path):
#                 os.remove(temp_file_path)

#     return {
#         "message": "Files uploaded successfully",
#         "listDocumentId": uploaded_documents,
#     }


@router.post("/documents/")
async def upload_documents(
    files: Optional[List[UploadFile]] = Form(None),  # Optional files
    texts: Optional[List[str]] = Form(None),  # Nhận mảng text
    links: Optional[List[str]] = Form(None),  # Link
    folderId: int = Form(...),
    description: str = Form(...),
    createdBy: str = Form(...),
    dataType: int = Form(...),
    db: Session = Depends(get_db),
):
    if not files and not texts and not links:
        raise HTTPException(status_code=400, detail="No content provided")

    uploaded_documents = []
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    namespace = str(folderId)

    # 1. Xử lý file upload
    if files:
        for file in files:
            temp_file_path = os.path.join(temp_dir, str(uuid.uuid4()))
            try:
                [chunks, content] = process_file(file, temp_file_path)
                index = get_pinecone()
                for chunk in chunks:
                    # print("chunk", chunk)
                    vector = embed_text(chunk)
                    vector_id = str(uuid.uuid4())

                    index.upsert(
                        [
                            (
                                vector_id,
                                vector,
                                {"text": chunk, "filename": file.filename},
                            )
                        ],
                        namespace=namespace,
                    )

                # print("file", file)
                # content = await file.read()
                # print("content", content)
                # if not content:
                #     raise HTTPException(status_code=400, detail="File is empty")

                document = schemas.Document(
                    ten_tai_lieu=file.filename,
                    loai_tai_lieu=file.content_type,
                    noi_dung=content,
                    mo_ta=description,
                    pinecone_id=vector_id,
                    thu_muc_id=folderId,
                    kieu_tai_lieu=dataType,
                    thoi_gian_tao=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    them_boi=createdBy,
                )

                document_model_new = document_model.upload_document(db, document)
                uploaded_documents.append(document_model_new)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

    # 2. Xử lý mảng text input
    if texts:
        index = get_pinecone()
        for text in texts:
            try:
                vector = embed_text(text)  # Embed từng đoạn văn bản
                vector_id = str(uuid.uuid4())

                title = text[:100]

                index.upsert(
                    [(vector_id, vector, {"text": text, "filename": title})],
                    namespace=namespace,
                )

                document = schemas.Document(
                    ten_tai_lieu=title,
                    loai_tai_lieu="text/plain",
                    noi_dung=text,
                    mo_ta=description,
                    pinecone_id=vector_id,
                    thu_muc_id=folderId,
                    kieu_tai_lieu=dataType,
                    thoi_gian_tao=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    them_boi=createdBy,
                )

                document_model_new = document_model.upload_document(db, document)
                uploaded_documents.append(document_model_new)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error processing text: {str(e)}"
                )

    # 3. Xử lý link input
    if links:
        index = get_pinecone()
        for link in links:
            try:
                dataLinks = await crawl_data(link)

                listData = split_text_into_chunks(
                    dataLinks, MAX_CHUNK_SIZE, OVERLAP_SIZE
                )

                for dataLink in listData:
                    vector = embed_text(dataLink)  # Embed từng đoạn văn bản
                    vector_id = str(uuid.uuid4())

                    index.upsert(
                        [(vector_id, vector, {"text": dataLink, "filename": link})],
                        namespace=namespace,
                    )

                descriptionText = dataLinks[:500]

                document = schemas.Document(
                    ten_tai_lieu=link,
                    loai_tai_lieu="text/plain",
                    noi_dung=dataLinks,
                    mo_ta=descriptionText,
                    pinecone_id=vector_id,
                    thu_muc_id=folderId,
                    kieu_tai_lieu=dataType,
                    thoi_gian_tao=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    them_boi=createdBy,
                )

                document_model_new = document_model.upload_document(db, document)
                uploaded_documents.append(document_model_new)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error processing link: {str(e)}"
                )
    return {
        "message": "Content uploaded successfully",
        "listDocumentId": uploaded_documents,
    }


# Get a document by ID
@router.get("/document/{document_id}", response_model=schemas.Document2)
def get_document_by_id(document_id: int, db: Session = Depends(get_db)):
    document = document_model.get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    return document


# Get a document by folder ID
@router.get("/documents/{folderId}/{typeFile}", response_model=List[schemas.Document2])
def get_documents_by_folder_id(
    folderId: int, typeFile: int, db: Session = Depends(get_db)
):
    documents = document_model.get_documents_by_folder_id(db, folderId, typeFile)

    return documents


# Delete a document by ID
@router.delete("/document/{document_id}", response_model=schemas.ResponseDocument)
def delete_document_by_id(document_id: int, db: Session = Depends(get_db)):
    document = document_model.get_document_by_id(db, document_id)
    print("document", document)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    # Kết nối Pinecone
    index = get_pinecone()

    # Namespace của tài liệu
    namespace = str(document.folderId)

    # Truy vấn Pinecone để lấy danh sách vector ID
    pinecone_vectors = index.query(
        vector=[0] * 768,  # Vector trống (không quan trọng giá trị)
        top_k=1000,  # Lấy tất cả các vector liên quan
        namespace=namespace,
        include_metadata=True,
        filter={"filename": {"$eq": document.documentName}},
    )

    # Xóa các vector khỏi Pinecone
    vector_ids = [match["id"] for match in pinecone_vectors["matches"]]
    if vector_ids:
        index.delete(ids=vector_ids, namespace=namespace)

    document = document_model.delete_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    return schemas.ResponseDocument(
        message="Xóa tài liệu thành công",
        documentId=document.id_tai_lieu,
        pineconeId=document.pinecone_id,
    )


@router.delete("/documents/{folderId}/{fileName}")
def delete_document(
    folderId: int,
    fileName: str,
    db: Session = Depends(get_db),
):
    try:
        # Namespace của tài liệu
        namespace = str(folderId)

        # Kết nối Pinecone
        index = get_pinecone()

        # Lấy tất cả các vector liên quan đến file từ database
        document = (
            db.query(DocumentModel)
            .filter(
                DocumentModel.ten_tai_lieu == fileName,
                DocumentModel.thu_muc_id == folderId,
            )
            .first()
        )

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Truy vấn Pinecone để lấy danh sách vector ID
        pinecone_vectors = index.query(
            vector=[0] * 1536,  # Vector trống (không quan trọng giá trị)
            top_k=1000,  # Lấy tất cả các vector liên quan
            namespace=namespace,
            include_metadata=True,
            filter={"filename": {"$eq": fileName}},
        )

        # Xóa các vector khỏi Pinecone
        vector_ids = [match["id"] for match in pinecone_vectors["matches"]]
        if vector_ids:
            index.delete(ids=vector_ids, namespace=namespace)

        # Xóa tài liệu khỏi database
        db.delete(document)
        db.commit()

        return {
            "message": f"Document '{fileName}' in folder '{folderId}' deleted successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while deleting document: {str(e)}"
        )


# Update a document
@router.put("/document/{document_id}", response_model=schemas.ResponseDocument)
def update_document(
    document_id: int, document: schemas.Document, db: Session = Depends(get_db)
):
    # Namespace của tài liệu
    namespace = str(document.folderId)

    # Kết nối Pinecone
    index = get_pinecone()

    # Truy vấn Pinecone để lấy danh sách vector ID
    pinecone_vectors = index.query(
        vector=[0] * 768,  # Vector trống (không quan trọng giá trị)
        top_k=1000,  # Lấy tất cả các vector liên quan
        namespace=namespace,
        include_metadata=True,
        filter={"filename": {"$eq": document.documentName}},
    )

    # Xóa các vector khỏi Pinecone
    vector_ids = [match["id"] for match in pinecone_vectors["matches"]]
    if vector_ids:
        index.delete(ids=vector_ids, namespace=namespace)

    document_update = document_model.update_document(db, document_id, document)
    if not document_update:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    return {
        "message": "Cập nhật tài liệu thành công",
        "documentId": document_update.id_tai_lieu,
        "pineconeId": document_update.pinecone_id,
    }


# Tải file tài liệu
@router.get("/download/document/{document_id}")
def download_document(document_id: int, db: Session = Depends(get_db)):
    db_document = document_model.get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    print("db_document", db_document.documentType)
    # Trả về file
    file_name = db_document.documentName
    file_content = db_document.content

    # Mã hóa tên file để tránh lỗi mã hóa khi có ký tự đặc biệt
    encoded_file_name = urllib.parse.quote(file_name)

    # Chuyển đổi nội dung file thành đối tượng BytesIO
    file_stream = BytesIO(file_content)

    # Trả về file dưới dạng StreamingResponse
    return StreamingResponse(
        file_stream,
        media_type=db_document.documentType,
        headers={"Content-Disposition": f"attachment; filename={encoded_file_name}"},
    )
