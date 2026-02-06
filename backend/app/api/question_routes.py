from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.app.schemas.question_schema import QuestionRequest, QuestionResponse
from backend.app.core.prompt_builder import build_question_prompt
from backend.app.services.llm_client import generate_questions
from backend.app.utils.pdf_utils import extract_text_from_pdf
from backend.app.utils.text_chunker import chunk_text
import re

router = APIRouter()


# -------------------------------------------------
# Helper: distribute questions across keywords
# -------------------------------------------------
def distribute_questions(keywords: list[str], total: int) -> dict[str, int]:
    base = total // len(keywords)
    remainder = total % len(keywords)

    distribution = {}
    for i, kw in enumerate(keywords):
        distribution[kw] = base + (1 if i < remainder else 0)

    return distribution


# =================================================
# TEXT / TOPIC / CONTENT BASED
# =================================================
@router.post("/generate-questions", response_model=QuestionResponse)
def generate(req: QuestionRequest):

    if not (req.topic or req.content or req.keywords):
        raise HTTPException(
            status_code=400,
            detail="Topic, content, or keywords must be provided"
        )

    questions = []

    # -------- KEYWORD DISTRIBUTION MODE --------
    if req.keywords:
        distribution = distribute_questions(req.keywords, req.num_questions)

        for keyword, count in distribution.items():
            prompt = build_question_prompt(
                num_questions=count,
                difficulty=req.difficulty,
                topic=req.topic,
                content=req.content,
                keywords=[keyword]
            )

            raw_output = generate_questions(prompt)

            for line in raw_output.split("\n"):
                match = re.match(r"^\d+[\).\s]+(.*)", line.strip())
                if match:
                    questions.append(match.group(1).strip())

        return {"questions": questions[:req.num_questions]}

    # -------- NORMAL MODE (NO KEYWORDS) --------
    prompt = build_question_prompt(
        num_questions=req.num_questions,
        difficulty=req.difficulty,
        topic=req.topic,
        content=req.content
    )

    raw_output = generate_questions(prompt)

    for line in raw_output.split("\n"):
        match = re.match(r"^\d+[\).\s]+(.*)", line.strip())
        if match:
            questions.append(match.group(1).strip())

    return {"questions": questions[:req.num_questions]}


# =================================================
# PDF BASED
# =================================================
@router.post("/generate-questions-from-pdf", response_model=QuestionResponse)
async def generate_from_pdf(
    file: UploadFile = File(...),
    num_questions: int = 10,
    difficulty: str = "medium",
    keywords: list[str] | None = None
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found")

    questions = []

    # -------- KEYWORD DISTRIBUTION MODE --------
    if keywords:
        distribution = distribute_questions(keywords, num_questions)

        for keyword, count in distribution.items():
            prompt = build_question_prompt(
                num_questions=count,
                difficulty=difficulty,
                content=text,
                keywords=[keyword]
            )

            raw_output = generate_questions(prompt)

            for line in raw_output.split("\n"):
                match = re.match(r"^\d+[\).\s]+(.*)", line.strip())
                if match:
                    questions.append(match.group(1).strip())

        return {"questions": questions[:num_questions]}

    # -------- NORMAL PDF MODE --------
    chunks = chunk_text(text)

    for chunk in chunks:
        prompt = build_question_prompt(
            num_questions=num_questions,
            difficulty=difficulty,
            content=chunk
        )

        raw_output = generate_questions(prompt)

        for line in raw_output.split("\n"):
            match = re.match(r"^\d+[\).\s]+(.*)", line.strip())
            if match:
                questions.append(match.group(1).strip())

        if len(questions) >= num_questions:
            break

    return {"questions": questions[:num_questions]}
