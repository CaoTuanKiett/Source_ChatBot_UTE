from PyPDF2 import PdfReader
from fastapi import HTTPException, UploadFile
import pandas as pd
from docx import Document
from app.config import settings

MAX_CHUNK_SIZE = settings.MAX_CHUNK_SIZE
OVERLAP_SIZE = settings.OVERLAP_SIZE


# Hàm trích xuất văn bản từ file Word
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


# Hàm trích xuất văn bản từ file PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])


# Hàm trích xuất dữ liệu từ file CSV
def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()


# Hàm trích xuất dữ liệu từ file Excel
def extract_text_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_string()


# Hàm xử lý file upload
def process_file(file: UploadFile, temp_file_path: str):
    # Lưu file tạm thời
    content = file.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")

    with open(temp_file_path, "wb") as f:
        # print(f"Nội dung file (first 100 bytes): {content[:100]}")
        f.write(content)

    # Trích xuất nội dung theo loại file
    if file.filename.endswith(".docx"):
        text = extract_text_from_docx(temp_file_path)
    elif file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(temp_file_path)
    elif file.filename.endswith(".csv"):
        text = extract_text_from_csv(temp_file_path)
    elif file.filename.endswith(".xlsx"):
        text = extract_text_from_excel(temp_file_path)
    elif file.filename.endswith(".txt"):
        text = content.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ")

    # Chia nhỏ nội dung thành các đoạn (chunk)
    chunks = split_text_into_chunks(text, MAX_CHUNK_SIZE, OVERLAP_SIZE)

    return chunks, content  # Trả về danh sách các đoạn


# def split_text_into_chunks(text, max_chunk_size):
#     words = text.split()
#     chunks = []

#     for i in range(0, len(words), max_chunk_size):
#         chunk = " ".join(words[i : i + max_chunk_size])
#         chunks.append(chunk)

#     return chunks


def split_text_into_chunks(text, max_chunk_size, overlap_size):
    words = text.split()  # Tách đoạn văn thành danh sách các từ
    chunks = []  # Danh sách để lưu các đoạn văn nhỏ
    i = 0  # Chỉ số bắt đầu của đoạn đầu tiên

    while i < len(words):
        # Tính chỉ số kết thúc đoạn hiện tại
        end = i + max_chunk_size
        chunk = " ".join(words[i:end])  # Lấy đoạn từ i đến end
        chunks.append(chunk)

        # Cập nhật chỉ số bắt đầu của đoạn tiếp theo (có overlap)
        i += max_chunk_size - overlap_size

    return chunks
