from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.gemini_api.genai_model import generate_response_test

from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx
from bs4 import BeautifulSoup
import logging

from app.schemas import QuestionRequest, GenerateResponse

router = APIRouter()


class Question(BaseModel):
    question: str


@router.post("/ask-gemini", response_model=GenerateResponse)
async def ask_gemini(request: Question) -> GenerateResponse:
    question = request.question
    logging.info(f"Request body: {question}")
    try:
        answer = generate_response_test(question)

        logging.info(f"generate_response_test: {answer}")
        # return {"question": question, "answer": GenerateResponse(answer=answer)}
        return GenerateResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Input model cho URL
class LinkInput(BaseModel):
    url: HttpUrl


# Endpoint để crawl dữ liệu từ link
@router.post("/crawl/")
async def crawl_link(link: LinkInput):
    try:
        # Convert HttpUrl to string
        url_str = str(link.url)

        # Gửi request để lấy nội dung HTML từ URL
        async with httpx.AsyncClient() as client:
            response = await client.get(url_str)
            response.raise_for_status()  # Kiểm tra lỗi HTTP

        # Phân tích nội dung HTML
        soup = BeautifulSoup(response.text, "lxml")

        # Trích xuất tiêu đề của trang
        title = soup.title.string if soup.title else "No title"

        # Trích xuất nội dung văn bản từ thẻ body
        body_text = (
            soup.body.get_text(separator="\n", strip=True)
            if soup.body
            else "No body content"
        )

        return {
            "url": url_str,
            "title": title,
            "content": body_text,
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
