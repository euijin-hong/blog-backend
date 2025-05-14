import app.schema.blog as blog_schema
import app.model.model as model

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result

from datetime import datetime

async def create_blog_post(db: AsyncSession, blog_post: blog_schema.CreateBlogPost) -> model.Post:
    new_post = model.Post(**blog_post.model_dump())
    db.add(new_post)
    await db.commit()
    return new_post

async def get_all_posts(db: AsyncSession) -> list[blog_schema.BlogPostSummary]:
    query = (
        select(model.Post).options(selectinload(model.Post.author_user))
    )
    result: Result = await db.execute(query)
    posts = result.scalars().all()
    
    if posts is None:
        raise HTTPException(status_code=404, detail="There is no blog post")
    
    return [blog_schema.BlogPostSummary(
        id = post.post_id,
        title = post.title,
        author = post.author_user.name,
        created_at = post.updated_at
    ) for post in posts]

async def get_post(post_id: int, 
                   db: AsyncSession) -> blog_schema.BlogPostSummary:
    query = (
        select(model.Post).where(model.Post.post_id == post_id).options(selectinload(model.Post.author_user))
    )
    result: Result = await db.execute(query)
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="Cannot find the post")
    
    return post

async def update_post(post_id: int, 
                      post_update: blog_schema.UpdateBlogPost, 
                      db: AsyncSession) -> model.Post:
    query = (
        select(model.Post)
        .where(model.Post.post_id == post_id)
        .options(selectinload(model.Post.author_user))
    )
    result: Result = await db.execute(query)
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="Cannot find the post")
    
    update_dict = {
        key: value
        for key, value in post_update.model_dump().items()
        if value is not None
    }

    for key, value in update_dict.items():
        setattr(post, key, value)
    post.updated_at = datetime.utcnow()

    return post

async def delete_post(post_id: int,
                      db: AsyncSession):
    result: Result = await db.execute(
         select(model.Post).where(model.Post.post_id == post_id)
    )
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=404, detail="Cannot find the post")
    
    await db.delete(post)
    await db.commit()

    return True