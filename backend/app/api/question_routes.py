from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional, List
import json

from backend.app.schemas.question_schema import QuestionRequest, QuestionResponse
from backend.app.core.prompt_builder import build_question_prompt
from backend.app.services.llm_client import generate_questions
from backend.app.utils.pdf_utils import extract_text_from_pdf
from backend.app.utils.text_chunker import chunk_text
from backend.app.utils.image_fetcher import fetch_wikipedia_image

router = APIRouter()

# -----------------------------------------
# SAFE JSON PARSER
# -----------------------------------------
def safe_json_loads(raw: str):
    if not raw or not raw.strip():
        raise ValueError("LLM returned empty response")

    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]

    # ✅ Try extracting JSON safely
    start = raw.find("[")
    end = raw.rfind("]")

    if start == -1:
        raise ValueError("No JSON array found")

    if end == -1:
        # 🔥 FIX: handle truncated JSON
        raw = raw[start:] + "]"
    else:
        raw = raw[start:end + 1]

    try:
        return json.loads(raw)
    except Exception:
        # 🔥 fallback: try fixing quotes
        raw = raw.replace("\n", " ")
        raw = raw.replace("\t", " ")
        return json.loads(raw)


# -----------------------------------------
# ATTACH IMAGE TO QUESTIONS
# -----------------------------------------
def attach_images(questions, topic=None):

    print("\n===== ATTACH IMAGE DEBUG =====")

    for q in questions:
        entity = None

        if topic:
            entity = topic
        elif "question" in q:
            entity = " ".join(q["question"].split(" ")[0:3])

        print("Trying entity:", entity)

        if entity:
            image_url = fetch_wikipedia_image(entity)

            if image_url:
                print("Image attached:", image_url)
                q["image_url"] = image_url
            else:
                print("No image found")

    print("===== ATTACH IMAGE DONE =====\n")

    return questions


# =================================================
# TEXT / CONTENT / TOPIC BASED GENERATION
# =================================================
@router.post("/generate-questions", response_model=QuestionResponse)
def generate(req: QuestionRequest):

    # ✅ SAFE DEFAULTS
    topic = req.topic or None
    content = req.content or None
    keywords = req.keywords or None

    
    num_questions = min(req.num_questions or 5, 5)  # ✅ limit to 5
    difficulty = req.difficulty or "medium"
    question_type = req.question_type or "descriptive"
    include_images = req.include_images or False

    # ✅ VALIDATION
    if not (topic or content or keywords):
        raise HTTPException(
            status_code=400,
            detail="Provide at least topic or content or keywords"
        )

    # ✅ BUILD PROMPT
    prompt = build_question_prompt(
        num_questions=num_questions,
        difficulty=difficulty,
        topic=topic,
        content=content,
        keywords=keywords,
        question_type=question_type
    )

    # ✅ CALL LLM
    raw = generate_questions(prompt)

    print("\n--- RAW LLM OUTPUT ---\n", raw, "\n---------------------\n")

    try:
        questions = safe_json_loads(raw)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse LLM output: {str(e)}"
        )

    # ✅ OPTIONAL IMAGE ATTACHMENT
    if include_images:
        questions = attach_images(questions, topic=topic)

    return {"questions": questions}


# =================================================
# PDF BASED QUESTION GENERATION
# =================================================
@router.post("/generate-questions-from-pdf", response_model=QuestionResponse)
async def generate_from_pdf(
    file: UploadFile = File(...),
    num_questions: int = 10,
    difficulty: str = "medium",
    question_type: str = "descriptive",
    include_images: bool = False
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    # ✅ Extract text
    text = extract_text_from_pdf(await file.read())

    # ✅ Chunk text
    chunks = chunk_text(text)

    questions = []

    # distribute questions across chunks
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
            continue

        if len(questions) >= num_questions:
            break

    questions = questions[:num_questions]

    # ✅ OPTIONAL IMAGE ATTACHMENT
    if include_images:
        questions = attach_images(questions)

    return {"questions": questions}