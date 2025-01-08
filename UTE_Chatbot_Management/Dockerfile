# Sử dụng Node.js để build ứng dụng Vue 3
FROM node:18-alpine AS build

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file package.json và package-lock.json để cài đặt dependencies
COPY package*.json ./

# Cài đặt dependencies
RUN npm install && npm cache clean --force

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# COPY .env /app/.env

# Build ứng dụng
RUN npm run build-only

# Sử dụng Nginx để chạy ứng dụng Vue
FROM nginx:alpine

# Copy các file build vào thư mục Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy file cấu hình Nginx vào container
COPY nginx.conf /etc/nginx/nginx.conf

# Cấu hình cổng Nginx
EXPOSE 80

# Chạy Nginx
CMD ["nginx", "-g", "daemon off;"]
