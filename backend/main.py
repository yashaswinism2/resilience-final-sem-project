from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.question_routes import router as question_router

app = FastAPI(
    title="Intelligent Question Generation System using NLP and LLMs"
)

# -------------------------------------------------
# CORS Configuration (REQUIRED for React)
# -------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Include Routes
# -------------------------------------------------
app.include_router(question_router)
