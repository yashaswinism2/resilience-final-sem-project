from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.app.schemas.question_schema import QuestionRequest, QuestionResponse
from backend.app.core.prompt_builder import build_question_prompt
from backend.app.services.llm_client import generate_questions
from backend.app.utils.pdf_utils import extract_text_from_pdf
from backend.app.utils.text_chunker import chunk_text
import json

router = APIRouter()


def safe_json_loads(raw: str):
    if not raw or not raw.strip():
        raise ValueError("LLM returned empty response")

    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]

    start = raw.find("[")
    end = raw.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("No JSON array found in LLM response")

    return json.loads(raw[start:end + 1])


# =================================================
# TEXT / CONTENT / TOPIC
# =================================================
@router.post("/generate-questions", response_model=QuestionResponse)
def generate(req: QuestionRequest):

    if not (req.topic or req.content or req.keywords):
        raise HTTPException(400, "Input required")

    prompt = build_question_prompt(
        num_questions=req.num_questions,
        difficulty=req.difficulty,
        topic=req.topic,
        content=req.content,
        keywords=req.keywords,
        question_type=req.question_type
    )

    raw = generate_questions(prompt)
    print("\n--- RAW LLM OUTPUT ---\n", raw, "\n---------------------\n")

    try:
        questions = safe_json_loads(raw)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse LLM output: {str(e)}"
        )

    return {"questions": questions}


# PDF
@router.post("/generate-questions-from-pdf", response_model=QuestionResponse)
async def generate_from_pdf(
    file: UploadFile = File(...),
    num_questions: int = 10,
    difficulty: str = "medium",
    question_type: str = "descriptive"
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    text = extract_text_from_pdf(await file.read())
    print("pdf chunks", text)
    chunks = chunk_text(text)

    questions = []
    per_chunk = max(1, num_questions // len(chunks))

    for chunk in chunks:
        prompt = build_question_prompt(
            num_questions=per_chunk,
            difficulty=difficulty,
            content=chunk,
            question_type=question_type
        )

        raw = generate_questions(prompt)
        print("\n--- RAW LLM OUTPUT ---\n", raw, "\n---------------------\n")

        try:
            parsed = safe_json_loads(raw)
            questions.extend(parsed)
        except Exception:
            continue  # skip bad chunk output safely

        if len(questions) >= num_questions:
            break

    return {"questions": questions[:num_questions]}
