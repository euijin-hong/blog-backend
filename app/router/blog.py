from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.blog as blog_schema
import app.crud.blog as blog_crud
import app.model.model as model
from app.db.db import get_db

router = APIRouter(
     prefix="/blog"
)


@router.get("/", response_model=list[blog_schema.BlogPostSummary])
async def get_blog(db: AsyncSession = Depends(get_db)):
    return await blog_crud.get_all_blog_posts(db)
    

@router.get("/{blog_id}", response_model=blog_schema.ReadBlogPost)
async def get_one_blog(blog_id: int):
    return {"id": blog_id,
            "title": "blog title",
            "content": "content",
            "author": "EJ Hong",
            "created_at": None}

@router.post("/create", response_model=blog_schema.ReadBlogPost, status_code=status.HTTP_201_CREATED)
async def create_blog_post(blog_post: blog_schema.CreateBlogPost, db: AsyncSession=Depends(get_db)):
    new_post = await blog_crud.create_blog_post(db, blog_post) 
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.patch("/update", response_model=blog_schema.UpdateBlogPost)
async def update_blog_post():
    return {"title": None, 
            "content": "content"}

