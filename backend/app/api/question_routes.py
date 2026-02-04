from fastapi import APIRouter, HTTPException
from backend.app.schemas.question_schema import QuestionRequest, QuestionResponse
from backend.app.core.prompt_builder import build_question_prompt
from backend.app.services.llm_client import generate_questions
import re

router = APIRouter()


@router.post("/generate-questions", response_model=QuestionResponse)
def generate(req: QuestionRequest):

    # ---------------- VALIDATION ----------------
    if not req.topic and not req.content:
        raise HTTPException(
            status_code=400,
            detail="Either topic or content must be provided"
        )

    # ---------------- PROMPT BUILDING ----------------
    prompt = build_question_prompt(
        num_questions=req.num_questions,
        difficulty=req.difficulty,
        topic=req.topic,
        content=req.content
    )

    # ---------------- LLM CALL ----------------
    raw_output = generate_questions(prompt)

    # ---------------- POST-PROCESSING ----------------
    questions = []

    for line in raw_output.split("\n"):
        line = line.strip()

        # Match numbered questions like:
        # "1. Question"
        # "2) Question"
        # "3 Question"
        match = re.match(r"^\d+[\).\s]+(.*)", line)
        if match:
            question_text = match.group(1).strip()
            if question_text:
                questions.append(question_text)

    # Ensure exact number of questions
    questions = questions[:req.num_questions]

    # ---------------- FINAL RESPONSE ----------------
    return {"questions": questions}
