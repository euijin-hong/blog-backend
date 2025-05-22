from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.blog import BlogPost, ReadBlogPost, CreateBlogPost, UpdateBlogPost
from app.model.model import User
from app.services.post_service import PostService, get_post_service
from app.dependencies.auth import get_current_user

router = APIRouter(
     prefix="/blog"
)

# Get all blog posts
@router.get("/", 
            response_model=list[BlogPost],
            summary="Retreive all blog posts",
            description="This router retreives all blog posts from the DB."
            )
async def get_posts(post_service: PostService = Depends(get_post_service)):
    return await post_service.get_all_posts()
    
# Get one blog post
@router.get("/{post_id}", 
            response_model=ReadBlogPost,
            summary="Return one blog post",
            description="This return the blog post corresponding to the post_id."
            )
async def get_post(post_id: int,
                   post_service: PostService = Depends(get_post_service)):
    return await post_service.get_post(post_id)

# Create a blog post
@router.post("/create", 
             response_model=ReadBlogPost, 
             summary="Create a new blog post",
             description="This creates new blog post and save it to the DB."
             )
async def create_post(post: CreateBlogPost, 
                      post_service: PostService = Depends(get_post_service),
                      current_user: User = Depends(get_current_user)):
    new_post = await post_service.create_post(post, current_user)
    return new_post

# Update a blog post
@router.put("/{post_id}", 
            response_model=ReadBlogPost,
            summary="Update an existing blog post",
            description="This updates the existing blog post corresponding to the post_id."
            )
async def update_blog_post(post_id: int, 
                           post_update: UpdateBlogPost, 
                           post_service: PostService = Depends(get_post_service),
                           current_user: User = Depends(get_current_user)):
    updated_post = await post_service.update_post(post_id, post_update, current_user)
    return updated_post


# Delete a blog post
@router.delete("/{post_id}",
               summary="Delete a blog post",
               description="This deletes an existing blog post corresponding to the post_id."
               )
async def delete_post(post_id: int,
                      post_service: PostService = Depends(get_post_service),
                      current_user: User = Depends(get_current_user)):
    await post_service.delete_post(post_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)