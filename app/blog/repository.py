from uuid import UUID

from tortoise.contrib.pydantic import pydantic_model_creator  # type: ignore

from .models import BlogPost
from .views import BlogPostCreate, BlogPostResponse

BlogPost_Pydantic = pydantic_model_creator(BlogPost, name="BlogPostPydantic")


async def create_blog_post(blog_post_data: BlogPostCreate) -> BlogPostResponse:
    blog_post = await BlogPost.create(**blog_post_data.model_dump())
    pydantic_model = await BlogPost_Pydantic.from_tortoise_orm(blog_post)
    return BlogPostResponse(**pydantic_model.model_dump())


async def get_blog_post(blog_post_uuid: UUID) -> BlogPostResponse | None:
    blog_post = await BlogPost.get_or_none(id=blog_post_uuid)
    if blog_post:
        pydantic_model = await BlogPost_Pydantic.from_tortoise_orm(blog_post)
        return BlogPostResponse(**pydantic_model.model_dump())
    return None


async def get_blog_posts(
    offset: int = 0, limit: int = 10
) -> tuple[list[BlogPostResponse], int]:
    blog_posts_count = await BlogPost.all().count()
    blog_posts = await BlogPost.all().offset(offset).limit(limit)
    blog_posts = [
        await BlogPost_Pydantic.from_tortoise_orm(blog_post) for blog_post in blog_posts
    ]
    blog_posts = [
        BlogPostResponse(**blog_post.model_dump()) for blog_post in blog_posts
    ]

    return (blog_posts, blog_posts_count)
