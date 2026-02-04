from pydantic import BaseModel
from typing import Optional, List

class QuestionRequest(BaseModel):
    topic: Optional[str] = None
    content : Optional[str] = None
    num_questions: int
    difficulty: str = "medium"

class QuestionResponse(BaseModel):
    questions: list[str]
