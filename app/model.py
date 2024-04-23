from pydantic import BaseModel


class VectorMatched(BaseModel):
    id: str
    embedding: list[float]

class ListMatched(BaseModel):
    items: list[VectorMatched]