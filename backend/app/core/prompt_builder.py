def build_question_prompt(
    num_questions: int,
    difficulty: str,
    topic: str | None = None,
    content: str | None = None,
    keywords: list[str] | None = None,
    question_type: str = "descriptive"
) -> str:

    base_context = ""
    if topic:
        base_context += f"\nTOPIC: {topic}"
    if content:
        base_context += f"\nCONTENT:\n{content}"
    if keywords:
        base_context += f"\nFOCUS KEYWORDS: {', '.join(keywords)}"

    # ================= DESCRIPTIVE WITH MODEL ANSWERS =================
    if question_type == "descriptive":
        return f"""
You are an experienced university examiner.

Generate EXACTLY {num_questions} {difficulty}-level DESCRIPTIVE questions.

{base_context}

For EACH question, generate:
1. A concise model answer (3–4 lines)
2. 4–6 key points (bullet-style)
3. 5–8 expected keywords

Output MUST be VALID JSON ARRAY ONLY.

JSON FORMAT:
[
  {{
    "question": "...",
    "model_answer": "...",
    "key_points": ["...", "..."],
    "expected_keywords": ["...", "..."]
  }}
]
"""

    # ================= MCQ =================
    return f"""
You are an expert university exam question setter.

Generate EXACTLY {num_questions} {difficulty}-level MCQs.

{base_context}

RULES:
- Each question MUST have exactly 4 options
- Options MUST NOT be prefixed with letters
- EXACTLY ONE option must be correct
- Output MUST be VALID JSON ARRAY ONLY

JSON FORMAT:
[
  {{
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "..."
  }}
]
"""
