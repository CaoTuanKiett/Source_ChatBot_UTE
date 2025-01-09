# Sử dụng Python base image
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies hệ thống cần thiết và xóa cache
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/* là gì

# Sao chép file yêu cầu (requirements.txt)
COPY requirements.txt ./

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# COPY .env /app/.env

# Thiết lập PYTHONPATH
# ENV PYTHONPATH=/app

# Expose port cho FastAPI
EXPOSE 8000

# Chạy ứng dụng
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]

# Chạy ứng dụng FastAPI với module đúng
# CMD ["sh", "-c", "python -m app.database.create_tables && python -m app.database.init_database && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
