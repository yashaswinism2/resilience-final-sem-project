from pydantic import BaseModel
from typing import Optional, List, Literal


class MCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


class DescriptiveQuestion(BaseModel):
    question: str
    model_answer: str
    key_points: List[str]
    expected_keywords: List[str]


class QuestionRequest(BaseModel):
    topic: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[List[str]] = None
    num_questions: int
    difficulty: str = "medium"
    question_type: Literal["descriptive", "mcq"] = "descriptive"


class QuestionResponse(BaseModel):
    questions: List[dict]
