# 🚀 Code Summarizer AI

[![Repo Size](https://img.shields.io/github/repo-size/souvikDevloper/Code_Summarizer_AI)](https://github.com/souvikDevloper/Code_Summarizer_AI)
[![Docker Compose](https://img.shields.io/badge/docker-compose-✓-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full-stack application that summarizes and reviews git diffs using AI.  
Built with **FastAPI** (Python) on the backend, **Vite + React** on the frontend, and served via **Docker Compose**.

---

## 📖 Table of Contents

1. [Features](#-features)  
2. [Architecture](#-architecture)  
3. [Getting Started](#-getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Clone & Setup](#clone--setup)  
   - [Environment Variables](#environment-variables)  
   - [Build & Run](#build--run)  
4. [API Reference](#-api-reference)  
5. [Frontend Usage](#-frontend-usage)  
6. [Development](#-development)  
7. [Contributing](#-contributing)  
8. [License](#-license)  
9. [Contact](#-contact)  

---

## 🔥 Features

- **Summarise** a git diff in concise bullet points.  
- **Review** a git diff with AI-generated code-review comments.  
- **Upload** a local diff file and preview its contents.  
- **Interactive Swagger UI** at `/docs` for quick API testing.  
- **SPA React frontend** with Monaco diff editor & diff preview.  
- **Docker Compose** for one-command setup & teardown.  

---

## 🏗 Architecture

┌──────────────────┐ HTTP ┌──────────────────┐
│ React + Vite │ <──────────> │ Nginx Proxy │
│ Frontend │ │ (serves & routes)│
└──────────────────┘ └──────────────────┘
│ /api/*
▼
┌──────────────────┐
│ FastAPI + Uvicorn│
│ Backend │
└──────────────────┘
│
▼
External LLM APIs (DeepSeek / OpenRouter)

yaml
Copy

---

## 🛠 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)  
- A shell (Linux/macOS) or PowerShell (Windows)  
- (Optional) GitHub CLI [`gh`](https://cli.github.com/)  

---

### Clone & Setup

```bash
git clone https://github.com/souvikDevloper/Code_Summarizer_AI.git
cd Code_Summarizer_AI
Environment Variables
Create a .env file in the repo root to provide your AI API keys:

dotenv
Copy
# .env
DEEPSEEK_API_KEY=your_deepseek_key      # optional (fallback)
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions

OPENROUTER_API_KEY=your_openrouter_key  # primary chat API
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_MODEL=deepseek/deepseek-chat:free
Note: If you only have one service, you can omit the other key—fallback logic will skip missing ones.

Build & Run
From the project root:

bash
Copy
# Build both services fresh
docker compose build --no-cache

# Launch backend (8000) & frontend (5173)
docker compose up -d

# Show logs
docker compose logs -f
Backend runs at http://localhost:8000

Swagger UI at http://localhost:8000/docs

Frontend SPA at http://localhost:5173

To stop and remove containers:

bash
Copy
docker compose down
📡 API Reference
All endpoints are prefixed with /api and expect JSON payloads (except file upload).

1. Summarise Diff
css
Copy
POST /api/summarise
Content-Type: application/json

Body:
{
  "text": "<git diff text>"
}

Response:
{
  "result": "• Bullet point 1…\n• Bullet point 2…\n• Bullet point 3…"
}
2. Review Diff
css
Copy
POST /api/review
Content-Type: application/json

Body:
{
  "text": "<git diff text>"
}

Response:
{
  "result": "Comment 1…\nComment 2…\n…"
}
3. Upload Patch File
makefile
Copy
POST /api/upload
Content-Type: multipart/form-data

Form Data:
file: <.diff or .patch file>

Response:
{
  "diff": "<uploaded file contents, text>"
}
🎨 Frontend Usage
Edit or drag-and-drop your diff file onto the drop zone.

The Monaco editor shows the raw diff.

Toggle “Show diff preview” to see a split-view.

Click Summarise or Review to call the backend.

All API calls are proxied via Nginx—no CORS hassles.

🛠 Development
If you want to hack on the frontend or backend separately:

Backend
bash
Copy
# inside repo root
cd backend
pip install -r requirements.txt

# run dev server
uvicorn backend.api:app --reload --host localhost --port 8000
Frontend
bash
Copy
cd frontend
npm install
npm run dev
🤝 Contributing
Fork the repo

Create a feature branch: git checkout -b feat/your-feature

Commit your changes

Push: git push origin feat/your-feature

Open a Pull Request against main

Please follow the existing code style, add tests where appropriate, and update this README if needed.

📄 License
This project is licensed under the MIT License. See LICENSE for details.

📬 Contact
Souvik Developer • @souvikDevloper
Project Link: https://github.com/souvikDevloper/Code_Summarizer_AI
Feel free to open issues or PRs!

Happy coding & summarizing!