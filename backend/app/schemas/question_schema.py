from pydantic import BaseModel
from typing import Optional, List, Literal, Union


# ---------------- MCQ ----------------
class MCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    image_url: Optional[str] = None


# ---------------- DESCRIPTIVE ----------------
class DescriptiveQuestion(BaseModel):
    question: str
    model_answer: str
    key_points: List[str]
    expected_keywords: List[str]
    image_url: Optional[str] = None


# ---------------- REQUEST ----------------
class QuestionRequest(BaseModel):
    topic: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[List[str]] = None

    # ✅ FIX: make optional with default
    num_questions: Optional[int] = 10

    difficulty: Optional[str] = "medium"
    question_type: Literal["descriptive", "mcq"] = "descriptive"
    include_images: Optional[bool] = False


# ---------------- RESPONSE ----------------
class QuestionResponse(BaseModel):
    questions: List[Union[MCQ, DescriptiveQuestion]]