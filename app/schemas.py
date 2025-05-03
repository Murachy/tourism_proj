from typing import List, Optional
from pydantic import BaseModel

class PhotoSchema(BaseModel):
    filename: str

    class Config:
        orm_mode = True

class MarkerCreate(BaseModel):
    latitude: float
    longitude: float
    comment: Optional[str] = None

class CommentSchema(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str


class MarkerResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    comment: Optional[str]
    photos: List[PhotoSchema] = []
    comments: List[CommentSchema] = []

    class Config:
        orm_mode = True


