from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.decision import router as decision_router

app = FastAPI(title="Thinking AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(decision_router, prefix="/decision")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def serve_ui():
    return FileResponse("app/static/index.html")
