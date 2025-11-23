"""
SQLAlchemy Database Models
Complete schema for Hebrew Markdown Blog
"""

from sqlalchemy import Column, String, Integer, Boolean, Text, String(36), ForeignKey, DateTime, Table, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .database import Base

# Many-to-Many relationship tables
post_categories = Table(
    'post_categories',
    Base.metadata,
    Column('post_id', String(36), String(36), ForeignKey('posts.id', ondelete='CASCADE')),
    Column('category_id', String(36), String(36), ForeignKey('categories.id', ondelete='CASCADE'))
)

post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', String(36), String(36), ForeignKey('posts.id', ondelete='CASCADE')),
    Column('tag_id', String(36), String(36), ForeignKey('tags.id', ondelete='CASCADE'))
)

# Models

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(Text)
    role = Column(String(20), default="author")  # admin, author
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    media = relationship("Media", back_populates="uploaded_by_user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    excerpt = Column(Text)
    content = Column(Text, nullable=False)  # Markdown content
    content_mdx = Column(Text, nullable=False)  # MDX processed content
    featured_image = Column(Text)
    status = Column(String(20), default="draft")  # draft, published
    author_id = Column(UUID(as_uuid=True), String(36), ForeignKey("users.id"))
    reading_time = Column(Integer)  # minutes
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author = relationship("User", back_populates="posts")
    categories = relationship("Category", secondary=post_categories, back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="post", cascade="all, delete-orphan")
    page_views = relationship("PageView", back_populates="post", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    posts = relationship("Post", secondary=post_categories, back_populates="categories")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    posts = relationship("Post", secondary=post_tags, back_populates="tags")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(UUID(as_uuid=True), String(36), ForeignKey("posts.id", ondelete="CASCADE"))
    parent_id = Column(UUID(as_uuid=True), String(36), ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    author_name = Column(String(100), nullable=False)
    author_email = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", cascade="all, delete-orphan")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(UUID(as_uuid=True), String(36), ForeignKey("posts.id", ondelete="CASCADE"))
    user_ip = Column(String(45), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    post = relationship("Post", back_populates="ratings")


class Media(Base):
    __tablename__ = "media"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    cloudinary_id = Column(String(255))
    mime_type = Column(String(100))
    size_bytes = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    uploaded_by = Column(UUID(as_uuid=True), String(36), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    uploaded_by_user = relationship("User", back_populates="media")


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(UUID(as_uuid=True), String(36), ForeignKey("posts.id", ondelete="CASCADE"))
    visitor_ip = Column(String(45))
    user_agent = Column(Text)
    referrer = Column(Text)
    country = Column(String(2))
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    post = relationship("Post", back_populates="page_views")


class ReadingSession(Base):
    __tablename__ = "reading_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(UUID(as_uuid=True), String(36), ForeignKey("posts.id", ondelete="CASCADE"))
    visitor_ip = Column(String(45))
    duration_seconds = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
