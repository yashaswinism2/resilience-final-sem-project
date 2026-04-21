from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.api.question_routes import router as question_router
from backend.app.api.auth_routes import router as auth_router
from backend.app.api.institute_routes import router as institute_router  # ✅ NEW

# DATABASE IMPORTS
from backend.app.db.database import Base, engine
import backend.app.models 
import os
from backend.app.api.dashboard_routes import router as dashboard_router
from backend.app.api.question_paper_routes import router as paper_router
from backend.app.models.notification_model import Notification
from backend.app.api.notification_routes import router as notification_router




# -------------------------------------------------
# Create FastAPI App
# -------------------------------------------------

app = FastAPI(
    title="Intelligent Question Generation System using NLP and LLMs"
)

# -------------------------------------------------
# CREATE DATABASE TABLES (IMPORTANT)
# -------------------------------------------------

Base.metadata.create_all(bind=engine)

# -------------------------------------------------
# CORS CONFIGURATION (IMPORTANT)
# -------------------------------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://resilience-final-sem-project.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# INCLUDE ROUTES
# -------------------------------------------------

app.include_router(auth_router)
app.include_router(question_router)
app.include_router(institute_router) 
app.include_router(dashboard_router)
app.include_router(paper_router)
app.include_router(notification_router)

# -------------------------------------------------
# SERVE REACT FRONTEND (PRODUCTION BUILD)
# -------------------------------------------------

frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
)

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