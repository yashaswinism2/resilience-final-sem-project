from pydantic import BaseModel
from typing import Optional, List

class QuestionRequest(BaseModel):
    topic: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[List[str]] = None
    num_questions: int
    difficulty: str = "medium"

class QuestionResponse(BaseModel):
    questions: list[str]
