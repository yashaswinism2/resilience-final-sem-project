def build_question_prompt(
    num_questions: int,
    difficulty: str,
    topic: str | None = None,
    content: str | None = None,
    keywords: list[str] | None = None
) -> str:

    # ---------------- KEYWORD MODE ----------------
    if keywords:
        keyword_list = "\n".join(f"- {k}" for k in keywords)

        return f"""
You are an expert university-level exam question setter.

Generate EXACTLY {num_questions} {difficulty}-level exam question(s)
STRICTLY based on EACH keyword below.

KEYWORDS:
{keyword_list}

RULES:
- Questions must focus ONLY on the given keyword(s)
- Do NOT mix multiple keywords in one question
- Output ONLY the questions
- Number the questions clearly (1., 2., 3., ...)
- Do NOT include answers or explanations
"""

    # ---------------- CONTENT MODE ----------------
    if content:
        return f"""
Generate exactly {num_questions} {difficulty}-level exam questions
STRICTLY based on the following content.

CONTENT:
{content}

RULES:
- Output ONLY the questions
- Number the questions clearly (1., 2., 3., ...)
- Do NOT include answers or explanations
"""

    # ---------------- TOPIC MODE ----------------
    return f"""
Generate exactly {num_questions} {difficulty}-level exam questions
on the following topic.

TOPIC:
{topic}

RULES:
- Output ONLY the questions
- Number the questions clearly (1., 2., 3., ...)
- Do NOT include answers or explanations
"""
