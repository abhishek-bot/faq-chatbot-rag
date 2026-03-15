from pydantic import BaseModel

class Feedback(BaseModel):
    question: str
    answer: str
    action: str   # "accept", "edit", "reject"