from uuid import UUID

from pydantic import BaseModel


class Pagination(BaseModel):
    total_items: int
    page_number: int
    page_size: int
    total_pages: int


class BlogPostCreate(BaseModel):
    title: str
    summary: str


class BlogPostResponse(BaseModel):
    id: UUID
    title: str
    summary: str

    class Config:
        from_attributes = True


class BlogPostsResponse(BaseModel):
    items: list[BlogPostResponse]
    pagination: Pagination
