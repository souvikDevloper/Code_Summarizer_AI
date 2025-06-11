# backend/api.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.summarize import summarize, review

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/api/summarise")
async def summarise_route(req: TextRequest):
    class Dummy: ...
    args = Dummy()
    args.bullets = 3
    args.style = "concise"
    args.model = "deepseek-chat"
    args.max_tokens = 512

    result = summarize(req.text, args)
    return {"result": result}

@app.post("/api/review")
async def review_route(req: TextRequest):
    class Dummy: ...
    args = Dummy()
    args.comments = 5
    args.depth = "brief"
    args.model = "deepseek-chat"
    args.max_tokens = 512

    result = review(req.text, args)
    return {"result": result}

@app.post("/api/upload")
async def upload_patch(file: UploadFile = File(...)):
    content = await file.read()
    try:
        diff = content.decode("utf-8")
    except UnicodeDecodeError:
        diff = content.decode("utf-8", errors="replace")
    return {"diff": diff}
