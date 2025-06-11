# frontend/Dockerfile

# 1) Builder: install & build
FROM node:18-alpine AS builder
RUN apk add --no-cache python3 make g++

WORKDIR /web
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps --silent

COPY . .
RUN npm run build

# 2) Production image: Nginx
FROM nginx:alpine

# Remove default content
RUN rm -rf /usr/share/nginx/html/*

# Copy built React into place
COPY --from=builder /web/dist /usr/share/nginx/html

# Copy our custom Nginx config (will proxy /api → backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
