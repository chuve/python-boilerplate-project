from uuid import UUID

from pydantic import BaseModel


class BlogPostCreate(BaseModel):
    title: str
    summary: str


class BlogPostResponse(BaseModel):
    id: UUID
    title: str
    summary: str

    class Config:
        from_attributes = True
