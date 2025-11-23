"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    role: str
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Post Schemas
class PostBase(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str]
    content: str
    featured_image: Optional[str]
    status: str = "draft"

class PostCreate(PostBase):
    content_mdx: str
    reading_time: Optional[int]

class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    excerpt: Optional[str]
    status: Optional[str]
    featured_image: Optional[str]

class Post(PostBase):
    id: UUID
    author_id: UUID
    views_count: int
    created_at: datetime
    published_at: Optional[datetime]

    class Config:
        from_attributes = True

class PostDetail(Post):
    author: User
    categories: List['Category']
    tags: List['Tag']

# Comment Schemas
class CommentCreate(BaseModel):
    author_name: str
    author_email: EmailStr
    content: str
    parent_id: Optional[UUID]

class Comment(BaseModel):
    id: UUID
    post_id: UUID
    author_name: str
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Rating Schema
class RatingCreate(BaseModel):
    user_ip: str
    rating: int

    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class Rating(BaseModel):
    id: UUID
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True

# Category Schema
class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str]

class Category(CategoryCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Tag Schema
class TagCreate(BaseModel):
    name: str
    slug: str

class Tag(TagCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Media Schema
class MediaCreate(BaseModel):
    filename: str
    url: str
    cloudinary_id: Optional[str]
    mime_type: Optional[str]
    size_bytes: Optional[int]
    width: Optional[int]
    height: Optional[int]

class Media(MediaCreate):
    id: UUID
    uploaded_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Analytics Schema
class PageViewCreate(BaseModel):
    post_id: UUID
    visitor_ip: Optional[str]
    user_agent: Optional[str]
    referrer: Optional[str]
