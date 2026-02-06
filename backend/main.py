from fastapi import FastAPI
from backend.app.api.question_routes import router
from backend.app.api.question_routes import router as question_router

app = FastAPI(
    title="Intelligent Question Generation System using NLP and LLMs"
)

app.include_router(router)
