from fastapi import APIRouter
from backend.app.schemas.question_schema import QuestionRequest, QuestionResponse
from backend.app.core.prompt_builder import build_question_prompt
from backend.app.services.llm_client import generate_questions

router = APIRouter()

@router.post("/generate-questions", response_model=QuestionResponse)
def generate(req: QuestionRequest):
    prompt = build_question_prompt(
        req.topic,
        req.num_questions,
        req.difficulty
    )

    raw_output = generate_questions(prompt)

    questions = [
        q.strip()
        for q in raw_output.split("\n")
        if q.strip()
    ]

    return {"questions": questions[:req.num_questions]}
