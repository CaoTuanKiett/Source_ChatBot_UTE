from pinecone import Pinecone
from app.config import settings
from fastapi import HTTPException

PINECONE_API_KEY = settings.PINECONE_API_KEY
PINECONE_ENVIRONMENT = settings.PINECONE_ENVIRONMENT
PINECONE_INDEX_NAME = settings.PINECONE_INDEX_NAME


def get_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    print(f"PINECONE_INDEX_NAME: {PINECONE_INDEX_NAME}")

    index_name = PINECONE_INDEX_NAME
    # print(f"Existing indexes: {pc.list_indexes()}")
    print(f"Connecting to index '{index_name}'")
    index = pc.Index(index_name)

    # Lấy index từ đối tượng Pinecone
    if index_name in pc.list_indexes().names():
        print(f"Index '{index_name}' đã tồn tại. Kết nối tới index.")
        index = pc.Index(index_name)  # Sử dụng đúng phương thức để truy cập index
    else:
        raise HTTPException(
            status_code=404, detail=f"Index '{index_name}' không tồn tại."
        )

    # # Embed your data
    # vector = pc.inference.embed(
    #     model="multilingual-e5-large",
    #     inputs=["The quick brown fox jumps over the lazy dog."],
    #     parameters={"input_type": "passage", "truncate": "END"},
    # )

    # print(f"Vector: {vector}")

    return index
