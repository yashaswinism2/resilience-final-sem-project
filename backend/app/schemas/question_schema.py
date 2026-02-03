from pydantic import BaseModel

class QuestionRequest(BaseModel):
    topic: str
    num_questions: int
    difficulty: str = "medium"

class QuestionResponse(BaseModel):
    questions: list[str]
