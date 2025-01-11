import google.generativeai as genai
import os
from app.config import settings
from app.utils.prompt_base import PROMPT_BASE
from app.schemas import QuestionRequest, GenerateResponse
import logging

GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME
GEMINI_TEMPERATURE = settings.GEMINI_TEMPERATURE
GEMINI_MAX_TOKENS = settings.GEMINI_MAX_TOKENS
GEMINI_TOP_P = settings.GEMINI_TOP_P
GEMINI_TOP_K = settings.GEMINI_TOP_K
GEMINI_RESPONSE_TYPE = settings.GEMINI_RESPONSE_TYPE
# PROMPT_BASE = settings.PROMPT_BASE

# Khởi tạo mô hình
os.environ["API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=os.environ["API_KEY"])

# Create the model
generation_config = {
    "temperature": GEMINI_TEMPERATURE,  # Tăng tính logic, giảm sự ngẫu nhiên
    "top_p": GEMINI_TOP_P,  # Giảm tập trung vào từ ít xác suất
    "top_k": GEMINI_TOP_K,  # Mở rộng số lượng từ khả thi
    "max_output_tokens": GEMINI_MAX_TOKENS,  # Giới hạn độ dài câu trả lời
    "response_mime_type": GEMINI_RESPONSE_TYPE,  # Trả về văn bản đơn thuần
}

modelAI = genai.GenerativeModel(GEMINI_MODEL_NAME, generation_config=generation_config)

# genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Hàm nhúng văn bản thành vector
# def embed_text(text):
#     embedding = genai.embed_text(model=modelAI, input=text)
#     return embedding["embedding"]  # Trả về vector nhúng

# def embed_text_OpenAI(text):
#     openai.api_key = settings.OPENAI_API_KEY
#     response = openai.Embedding.create(
#         model="text-embedding-ada-002",  # Chọn model thích hợp
#         input=text,
#     )
#     print(f"Response: {response}")
#     return response["embedding"]


def embed_text(text):
    try:
        # Log the input text being embedded (ensure it's not too large to log)
        logging.debug(
            f"Embedding the following text: {text[:100]}..."
        )  # Log a snippet for brevity

        # Gọi API để nhúng văn bản
        embedding = genai.embed_content(model="models/text-embedding-004", content=text)
        # print(f"Embedding: {embedding}")

        # Kiểm tra xem response có chứa key "embedding" và dữ liệu hợp lệ
        if "embedding" not in embedding:
            raise ValueError("Response không chứa 'embedding' key.")

        if not isinstance(embedding["embedding"], list):
            raise ValueError("Embedding không phải là danh sách.")

        return embedding["embedding"]  # Trả về vector nhúng

    except ValueError as ve:
        logging.error(f"Value error in embedding text: {str(ve)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in embedding text: {str(e)}")
        raise ValueError(f"Error in embedding text: {str(e)}")


def generate_response(question: QuestionRequest):
    prompt = f"Hãy trả lời Câu hỏi: {question.question}, dựa trên Tài Liệu: {question.document}, và Lịch sử tin nhắn: {question.historyMessages}. Quy tắc: {PROMPT_BASE}"
    # print(f"Prompt: {prompt}")
    try:
        # Gọi phương thức generate để tạo câu trả lời
        response = modelAI.generate_content(prompt)
        # logging.info(f"generate_response: {response.text}")
        return response.text
    except Exception as e:
        # Xử lý lỗi nếu có
        raise Exception(f"Error generating response: {str(e)}")


# Chỉnh sửa câu hỏi sau cho ngắn gọn và dễ hiểu
# def preprocess_with_gemini(question, listMessages):
#     prompt = f"Bạn là một chatbot hỗ trợ tuyển sinh của Trường Đại học Sư phạm Kỹ thuật - Đại học Đà Nẵng. Nhiệm vụ của bạn là viết lại các câu hỏi của người dùng để trở nên rõ ràng, dễ hiểu và đầy đủ nhất. Đảm bảo rằng câu hỏi không bị mất ý nghĩa ban đầu, nhưng được bổ sung thông tin cần thiết đúng ngữ cảnh để giúp hệ thống tìm kiếm trả về kết quả chính xác nhất. Hãy viết lại câu hỏi dưới dạng câu hoàn chỉnh, tự nhiên và chuyên nghiệp. Câu hỏi của người dùng là: {question}. Hãy viết lại câu hỏi trên dựa trên lịch sử cuộc hội thoại {listMessages}. Lưu ý: Đừng thay đổi ý nghĩa của câu hỏi, kết quả trả về là 1 câu hỏi."
#     response = modelAI.generate_content(prompt)

#     return response.text

def preprocess_with_gemini(question, listMessages):
    # Tách prompt ra thành một phần riêng
    prompt = (
        "Bạn là một sinh viên đang tìm hiểu thông tin về Trường Đại học Sư phạm Kỹ thuật - Đại học Đà Nẵng. "
        "Hiện tại, bạn đang sử dụng chatbot hỗ trợ tuyển sinh của Trường để đặt câu hỏi và nhận thông tin tư vấn. "
        "Nhiệm vụ của bạn là viết lại các câu hỏi mà người dùng đã nhập sao cho rõ ràng, dễ hiểu và đầy đủ nhất. "
        "Đảm bảo rằng: "
        "- Câu hỏi không bị thay đổi ý nghĩa ban đầu. "
        "- Nội dung được bổ sung các thông tin cần thiết phù hợp với ngữ cảnh cuộc hội thoại. "
        "- Văn phong được viết dưới dạng câu hoàn chỉnh, tự nhiên và mang tính chuyên nghiệp. "
        "Điều này giúp hệ thống tìm kiếm của chatbot trả về kết quả chính xác và hữu ích nhất. "
        "Lưu ý: "
         "- Nếu câu hỏi của người dùng có các nghĩa là chào hỏi, cảm ơn, không có thêm câu hỏi, hoặc muốn để lại góp ý thì giữ nguyên câu hỏi và không cần viết lại câu hỏi, trả ra câu hỏi không chỉnh sửa"
        "\n\n"
        f"Dưới đây là câu hỏi mà người dùng vừa nhập: {question}\n"
        f"Lịch sử cuộc hội thoại trước đó: {listMessages}\n"
        "\n"
        "Dựa trên câu hỏi và lịch sử hội thoại, hãy viết lại câu hỏi sao cho đáp ứng các tiêu chí trên."
    )
    
    try:
        # Gửi prompt đến model AI để nhận phản hồi
        response = modelAI.generate_content(prompt)
        return response.text
    except Exception as e:
        # Xử lý lỗi và thông báo vấn đề
        print(f"Lỗi trong quá trình xử lý với Gemini: {e}")
        return "Đã xảy ra lỗi khi xử lý câu hỏi. Vui lòng thử lại."


def generate_response_test(question: QuestionRequest):
    # logging.info(f"generate_response: {question}")
    try:
        # Gọi phương thức generate để tạo câu trả lời
        response = modelAI.generate_content(question)
        logging.info(f"generate_response: {response.text}")
        return response.text
    except Exception as e:
        # Xử lý lỗi nếu có
        raise Exception(f"Error generating response: {str(e)}")


## Test search document by question + prompt >> gemini api
# # API tìm kiếm
# @app.get("/search/")
async def search(query: str):
    # Chuyển từ khóa thành vector nhúng
    query_vector = embed_text(query)

    # Tìm kiếm trong Pinecone
    result = index.query(query_vector, top_k=5, include_metadata=True)

    # Tổng hợp nội dung từ Pinecone
    search_results = [
        f"- {match['metadata']['filename']}: {match['metadata']['text']}"
        for match in result["matches"]
    ]
    combined_results = "\n".join(search_results)

    # Gửi đến Gemini để xử lý
    prompt = f"""
    Tôi đang tìm kiếm thông tin với từ khóa: "{query}".
    Đây là các kết quả tìm kiếm từ tài liệu:
    {combined_results}

    Vui lòng tóm tắt và đưa ra câu trả lời ngắn gọn, đầy đủ nhất.
    """
    gemini_response = genai.generate_text(
        model="gemini-1.5-flash", prompt=prompt, max_output_tokens=200
    )

    return {
        "query": query,
        "gemini_answer": gemini_response["candidates"][0]["output"],
        "pinecone_results": search_results,
    }


# # Hàm nhúng văn bản thành vector
# def embed_text(text):
#     # Tích hợp mô hình nhúng tại đây
#     return [0.0] * 1536  # Thay bằng vector thực tế từ mô hình nhúng
