import app.schema.blog as blog_schema
import app.model.model as model

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result

async def create_blog_post(db: AsyncSession, blog_post: blog_schema.CreateBlogPost) -> model.Post:
    new_post = model.Post(**blog_post.model_dump())
    db.add(new_post)
    await db.commit()
    return new_post

async def get_all_blog_posts(db: AsyncSession) -> list[blog_schema.BlogPostSummary]:
    result: Result = await db.execute(
        select(model.Post).options(selectinload(model.Post.author_user))
    )
    posts = result.scalars().all()
    return [blog_schema.BlogPostSummary(
        id = post.post_id,
        title = post.title,
        author = post.author_user.name,
        created_at = post.updated_at
    ) for post in posts]