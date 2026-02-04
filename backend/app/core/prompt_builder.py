def build_question_prompt(
    num_questions: int,
    difficulty: str,
    topic: str | None = None,
    content: str | None = None
) -> str:

    if content:
        return f"""
Generate exactly {num_questions} {difficulty}-level exam questions
STRICTLY based on the following content.

Content:
{content}

IMPORTANT RULES:
- Output ONLY the questions
- Do NOT include introductions, explanations, or headings
- Do NOT say "Here are the questions"
- Number each question clearly (1., 2., 3., ...)
- Do NOT include answers
"""

    return f"""
Generate exactly {num_questions} {difficulty}-level exam questions
on the following topic.

Topic:
{topic}

IMPORTANT RULES:
- Output ONLY the questions
- Do NOT include introductions, explanations, or headings
- Do NOT say "Here are the questions"
- Number each question clearly (1., 2., 3., ...)
- Do NOT include answers
"""
