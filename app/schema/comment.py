from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CommentBaseModel(BaseModel):
    content: str = Field(..., min_length=1, max_length=100, description="Comment Content (1~100 characters)")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )


class CreateComment(CommentBaseModel):
    user_id: int
    post_id: int

class ReadComment(CommentBaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime | None = Field(default=None)

class UpdateComment(CommentBaseModel):
    pass