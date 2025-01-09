Mở Terminal và chạy các câu lệnh sau để cập nhật danh sách gói và cài đặt Nginx:
sudo apt update
sudo apt install nginx

mysql -h 127.0.0.1 -P 3306 -u root

docker exec -it 510d019573e4 bash

docker logs sourcecode-backend-1

    # command: >
    #   sh -c "
    #   sleep 10 &&
    #   python -m app.database.create_tables &&
    #   python -m app.database.init_database &&
    #   uvicorn app.main:app --host 0.0.0.0 --port 8000
    #   "

docker tag 61c2f9653cd5 tuankiet777/sourcecode-frontend:v2.0
docker push tuankiet777/sourcecode-frontend:v2.0

### Câu lệnh trên Ubuntu

# pull image

sudo docker pull tuankiet777/mysql:1.0.0
sudo docker pull tuankiet777/sourcecode-frontend:1.0.0
sudo docker pull tuankiet777/sourcecode-backend:1.0.2

# chạy image:

sudo docker run --name database -d -p 3307:3306 tuankiet777/mysql:1.0.0

sudo docker run --name frontend-container -d -p 3000:80 tuankiet777/sourcecode-frontend:1.0.0

sudo docker run --name backend-container -d -p 8000:8000 tuankiet777/sourcecode-backend:1.0.2

# xem log:

sudo docker logs frontend-container
sudo docker logs backend-container
sudo docker logs database

# stop container id

sudo docker stop 3eba6feda8af

# xóa container id

sudo docker rm 3eba6feda8af

# xóa image

sudo docker rmi tuankiet777/sourcecode-backend:1.0.1

## Câu lệnh dưới máy local win

# tag name update version

docker tag sourcecode-backend tuankiet777/sourcecode-backend:1.0.2

# push image lên docker

docker push tuankiet777/sourcecode-backend:1.0.2

# xóa image cũ version

docker rmi tuankiet777/sourcecode-backend:1.0.1

# chạy docker down

docker compose down

# chạt file docker compose

docker-compose up --build -d

## Cài đặt git

sudo apt update
sudo apt install git
git --version
git clone https://github.com/CaoTuanKiett/Source_ChatBot_UTE.git

## Câu lệnh trong ubuntu

đnag đứng thư mục nào: pwd
lietj kê danh sách file: ls
tạo một thư mục mới: mkdir .env
xóa thư mục rm -r .env
lưu thoát ctrl + X ==> Y ==> Enter

#### START

## Setup docker

# Add Docker's official GPG key:

sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:

echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
 $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
 sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

tải docker compose
sudo apt-get update

sudo apt install docker-compose
docker-compose --version

## Cài đặt git

sudo apt update
sudo apt install git
git --version
git clone https://github.com/CaoTuanKiett/Source_ChatBot_UTE.git

# thêm file .env vào chatbot-server

## Config Port trên AWS

- http: 80
- https: 433

## config DNS tên miền chatbotute.io.vn trên mắt bão

chatbotute.io.vn

## Cấp quyền đọc cho toàn bộ nội dung thư mục

sudo chmod -R 755 /etc/letsencrypt
sudo chmod -R 644 /etc/letsencrypt/live/chatbotute.io.vn/\*

# Kiểm tra nội dung thư mục

ls -l /etc/letsencrypt/live/chatbotute.io.vn/

## Câu lệnh docker

sudo docker-compose down

sudo docker-compose up --build -d

sudo docker-compose ps

## câu lệnh NGINX

sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d chatbotute.io.vn -d www.chatbotute.io.vn

## Câu lệnh stop kiểm tra cổng 80 nginx

sudo lsof -i :80

sudo systemctl stop nginx
