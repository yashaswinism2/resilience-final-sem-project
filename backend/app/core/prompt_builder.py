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
        base_context += f"\nCONTENT:\n{content[:1500]}"  # ✅ limit size
    if keywords:
        base_context += f"\nFOCUS KEYWORDS: {', '.join(keywords)}"

    # 🔥 GLOBAL RULES (VERY IMPORTANT)
    strict_rules = """
IMPORTANT RULES:
- Return ONLY a valid JSON array
- Do NOT include ``` or markdown
- Do NOT include explanation or text outside JSON
- Ensure JSON is COMPLETE and NOT truncated
- Ensure commas and brackets are correct
"""

    # ================= DESCRIPTIVE =================
    if question_type == "descriptive":
        return f"""
You are an experienced university examiner.

Generate EXACTLY {num_questions} {difficulty}-level DESCRIPTIVE questions.

{base_context}

For EACH question:
- model_answer must be SHORT (2–3 lines only)
- key_points must be 4–5 items
- expected_keywords must be 5–6 words

{strict_rules}

OUTPUT FORMAT:
[
  {{
    "question": "string",
    "model_answer": "string",
    "key_points": ["string"],
    "expected_keywords": ["string"]
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
- Options MUST NOT be prefixed (no A/B/C/D)
- EXACTLY ONE correct answer
- Keep questions SHORT

{strict_rules}

OUTPUT FORMAT:
[
  {{
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "correct_answer": "string"
  }}
]
"""