from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .repository import create_blog_post, get_blog_post, get_blog_posts
from .views import BlogPostCreate, BlogPostResponse, BlogPostsResponse, Pagination

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)


class PaginationQueryParams(BaseModel):
    page_size: int = 10
    page_number: int = 0


@router.post("/posts")
async def create_post(blog_post: BlogPostCreate) -> BlogPostResponse:
    created_post = await create_blog_post(blog_post)
    return created_post


@router.get("/posts")
async def get_posts(
    pagination: Annotated[PaginationQueryParams, Depends(PaginationQueryParams)],
) -> BlogPostsResponse:
    blog_posts, blog_posts_count = await get_blog_posts(
        offset=pagination.page_number * pagination.page_size, limit=pagination.page_size
    )
    total_pages = int(round(blog_posts_count / pagination.page_size, 0))

    if total_pages - 1 < pagination.page_number:
        raise HTTPException(status_code=404, detail="Page doesn't exist")

    return BlogPostsResponse(
        items=blog_posts,
        pagination=Pagination(
            total_items=blog_posts_count,
            total_pages=total_pages,
            page_number=pagination.page_number,
            page_size=pagination.page_size,
        ),
    )


@router.get("/posts/{uuid}")
async def get_post(uuid: UUID) -> BlogPostResponse:
    blog_post = await get_blog_post(uuid)
    if blog_post:
        return blog_post
    else:
        raise HTTPException(status_code=404, detail="BlogPost doesn't exist")
