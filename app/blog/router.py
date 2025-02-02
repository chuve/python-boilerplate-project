from uuid import UUID

from fastapi import APIRouter, HTTPException

from .repository import create_blog_post, get_blog_post
from .views import BlogPostCreate, BlogPostResponse

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)


@router.post("/post")
async def create_post(blog_post: BlogPostCreate) -> BlogPostResponse:
    created_post = await create_blog_post(blog_post)
    return created_post


# @router.get("/posts")
# async def get_posts() -> list[BlogPost]:
#     blog_posts = await BlogPost.all()
#     return blog_posts


@router.get("/posts/{uuid}")
async def get_post(uuid: UUID) -> BlogPostResponse:
    blog_post = await get_blog_post(uuid)
    if blog_post:
        return blog_post
    else:
        raise HTTPException(status_code=404, detail="BlogPost doesn't exist")
