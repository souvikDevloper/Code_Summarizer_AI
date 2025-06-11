# 1) Builder stage: use Node to install & build
FROM node:18-alpine AS builder

# Install native build tools (needed by some npm packages)
RUN apk add --no-cache python3 make g++

WORKDIR /web

# 1️⃣ Copy package files and install via npm install
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps --silent

# 2️⃣ Bring in the source and build
COPY . .
RUN npm run build

# 2) Production stage: serve via nginx
FROM nginx:alpine

# Clear default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy our built files
COPY --from=builder /web/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
