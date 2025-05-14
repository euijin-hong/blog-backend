from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class BlogBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )

class BlogPostSummary(BlogBaseModel):
    id: int
    title: str
    author_id: int
    created_at: datetime | None = Field(default=None)

class ReadBlogPost(BlogBaseModel):
    author_id: int
    title: str
    content: str
    created_at: datetime | None = Field(default=None)

class CreateBlogPost(BlogBaseModel):
    title: str = Field(..., min_length=3, max_length=250, description="Title of the blog post(max 250 char)")
    content: str = Field(..., min_length=5, max_length=5000, description="Content of the blos post(max 5000 char)")

class UpdateBlogPost(BlogBaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=250)
    content: str | None = Field(default=None, min_length=5, max_length=5000)

