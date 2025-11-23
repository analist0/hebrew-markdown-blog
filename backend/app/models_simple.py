"""Simplified models for SQLite"""
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(20), default="author")
    created_at = Column(DateTime, server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    author_id = Column(Integer)
    status = Column(String(20), default="draft")  # draft, published
    published_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    views = Column(Integer, default=0)
    reading_time = Column(Integer, default=0)

print("✅ Simple models loaded")
