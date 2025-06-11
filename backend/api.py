# api.py  – thin REST wrapper around summarize.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.summarize import summarize, review   # your existing functions

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)                                          # :contentReference[oaicite:5]{index=5}

@app.post("/api/summarise")
async def summarise_route(text: str):
    class Dummy: pass
    args = Dummy(); args.bullets = 3; args.style = "concise"; args.model="deepseek-chat"; args.max_tokens=512
    return {"result": summarize(text, args)}

@app.post("/api/review")
async def review_route(text: str):
    class Dummy: pass
    args = Dummy(); args.comments = 5; args.depth = "brief"; args.model="deepseek-chat"; args.max_tokens=512
    return {"result": review(text, args)}

@app.post("/api/upload")
async def upload_patch(file: UploadFile = File(...)):      # :contentReference[oaicite:6]{index=6}
    diff = (await file.read()).decode()
    return {"diff": diff}
