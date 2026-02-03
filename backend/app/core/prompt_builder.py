def build_question_prompt(topic: str, num_questions: int, difficulty: str) -> str:
    return f"""
Generate exactly {num_questions} {difficulty} level questions
on the topic below.

Topic:
{topic}

Rules:
- Do NOT include answers
- Do NOT add explanations
- One question per line
"""
