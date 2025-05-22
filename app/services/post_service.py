# Code is not used any more. Check app/services/post_services.py
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from app.db.db import get_db

from app.schema.blog import BlogPost, ReadBlogPost, CreateBlogPost, UpdateBlogPost
from app.model.model import User, Post

from typing import List
from datetime import datetime

class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_post(self, post: CreateBlogPost, user:User) -> Post:
        new_post = Post(**post.model_dump())
        author_id = user.id
        new_post.author_id = author_id
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post
    
    async def get_all_posts(self) -> List[BlogPost]:
        query= (
            select(Post).options(selectinload(Post.author))
        )
        result: Result = await self.db.execute(query)
        posts = result.scalars().all()

        return [BlogPost(
        id = post.post_id,
        title = post.title,
        content = post.content,
        author_name = post.author.name,
        created_at = post.updated_at
    ) for post in posts]

    async def get_post(self, post_id: int) -> BlogPost:
        query = (
            select(Post).where(Post.post_id == post_id)
        )
        result: Result = await self.db.execute(query)
        post = result.scalar_one_or_none()
        
        if post is None:
            raise HTTPException(status_code=404, detail="Cannot find the post")
        
        return post
    
    async def update_post(self, 
                          post_id: int, 
                          post_update: UpdateBlogPost,
                          user: User
                         ) -> Post:
        query = (
            select(Post)
            .where(Post.post_id == post_id)
        )
        result: Result = await self.db.execute(query)
        post = result.scalar_one_or_none()

        if post is None:
            return None
        
        if post.author_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Not Authorized"
            )

        update_dict = {
            key: value
            for key, value in post_update.model_dump().items()
            if value is not None
        }

        for key, value in update_dict.items():
            setattr(post, key, value)
        post.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(post)

        return post
    
    async def delete_post(self,
                          post_id: int,
                          user: User
                          ):
        result: Result = await self.db.execute(
            select(Post).where(Post.post_id == post_id)
        )
        post = result.scalar_one_or_none()

        if post is None:
            raise HTTPException(
                status_code=404, 
                detail="Cannot find the post."
                )
        
        if post.author_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Not Authorized"
            )

        await self.db.delete(post)
        await self.db.commit()

        return True
    

async def get_post_service(db: AsyncSession = Depends(get_db)):
    return PostService(db)