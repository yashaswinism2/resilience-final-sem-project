from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# from backend.app.api.question_routes import router as question_router
from app.api.question_routes import router as question_router
import os

# -------------------------------------------------
# Create FastAPI App
# -------------------------------------------------

app = FastAPI(
    title="Intelligent Question Generation System using NLP and LLMs"
)

# -------------------------------------------------
# Enable CORS (Required for Vercel frontend)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for learning; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Include API routes
# -------------------------------------------------

app.include_router(question_router)

# -------------------------------------------------
# Serve React Frontend (Production Build)
# -------------------------------------------------

frontend_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "frontend",
    "dist"
)
frontend_path = os.path.abspath(frontend_path)

if os.path.exists(frontend_path):

    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(frontend_path, "assets")),
        name="assets"
    )

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        file_path = os.path.join(frontend_path, full_path)

        if os.path.exists(file_path):
            return FileResponse(file_path)

        return FileResponse(os.path.join(frontend_path, "index.html"))