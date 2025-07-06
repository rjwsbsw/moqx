from typing import List
from pydantic import BaseModel

class OptionOut(BaseModel):
    id: int
    text: str
    correct: bool
    
    class Config:
        from_attributes = True
class QuestionOut(BaseModel):
    id: int
    text: str
    options: List[OptionOut]

    class Config:
        from_attributes = True
class QuizOut(BaseModel):
    id: int
    title: str
    questions: List[QuestionOut]

    class Config:
        from_attributes = True
