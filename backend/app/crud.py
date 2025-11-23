"""
CRUD operations for all database models
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from datetime import datetime
import uuid

from . import models, schemas
from .auth import get_password_hash

# ==================== USER CRUD ====================

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ==================== POST CRUD ====================

def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None
):
    query = db.query(models.Post)
    
    if status:
        query = query.filter(models.Post.status == status)
    
    if search:
        query = query.filter(
            or_(
                models.Post.title.contains(search),
                models.Post.content.contains(search)
            )
        )
    
    return query.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: str):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_post_by_slug(db: Session, slug: str):
    return db.query(models.Post).filter(models.Post.slug == slug).first()

def create_post(db: Session, post: schemas.PostCreate, author_id: str):
    db_post = models.Post(
        **post.dict(),
        author_id=author_id,
        published_at=datetime.utcnow() if post.status == "published" else None
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: str, post: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post.dict(exclude_unset=True).items():
            setattr(db_post, key, value)
        db_post.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: str):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return True

def increment_post_views(db: Session, post_id: str):
    db_post = get_post(db, post_id)
    if db_post:
        db_post.views_count += 1
        db.commit()
    return db_post

# ==================== COMMENT CRUD ====================

def get_post_comments(db: Session, post_id: str):
    return db.query(models.Comment).filter(
        models.Comment.post_id == post_id,
        models.Comment.status == "approved"
    ).order_by(models.Comment.created_at.desc()).all()

def create_comment(db: Session, comment: schemas.CommentCreate, post_id: str):
    db_comment = models.Comment(
        **comment.dict(),
        post_id=post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment_status(db: Session, comment_id: str, status: str):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db_comment.status = status
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: str):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return True

# ==================== RATING CRUD ====================

def create_rating(db: Session, rating: schemas.RatingCreate, post_id: str):
    db_rating = models.Rating(
        **rating.dict(),
        post_id=post_id
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_post_average_rating(db: Session, post_id: str):
    avg = db.query(func.avg(models.Rating.rating)).filter(
        models.Rating.post_id == post_id
    ).scalar()
    count = db.query(func.count(models.Rating.id)).filter(
        models.Rating.post_id == post_id
    ).scalar()
    return {"average": float(avg) if avg else 0, "count": count}

# ==================== CATEGORY CRUD ====================

def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: str, category: schemas.CategoryCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        for key, value in category.dict().items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: str):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return True

# ==================== TAG CRUD ====================

def get_tags(db: Session):
    return db.query(models.Tag).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# ==================== MEDIA CRUD ====================

def get_media(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Media).offset(skip).limit(limit).all()

def create_media(db: Session, media: schemas.MediaCreate, user_id: str):
    db_media = models.Media(
        **media.dict(),
        uploaded_by=user_id
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

def delete_media(db: Session, media_id: str):
    db_media = db.query(models.Media).filter(models.Media.id == media_id).first()
    if db_media:
        db.delete(db_media)
        db.commit()
    return True

# ==================== ANALYTICS CRUD ====================

def create_page_view(db: Session, view: schemas.PageViewCreate):
    db_view = models.PageView(**view.dict())
    db.add(db_view)
    db.commit()
    db.refresh(db_view)
    return db_view

def get_post_analytics(db: Session, post_id: str):
    views = db.query(func.count(models.PageView.id)).filter(
        models.PageView.post_id == post_id
    ).scalar()
    
    return {
        "total_views": views,
        "post_id": post_id
    }

def count_posts(db: Session):
    return db.query(func.count(models.Post.id)).scalar()

def count_total_views(db: Session):
    return db.query(func.sum(models.Post.views_count)).scalar() or 0

def count_comments(db: Session):
    return db.query(func.count(models.Comment.id)).scalar()

def get_popular_posts(db: Session, limit: int = 10):
    return db.query(models.Post).order_by(
        models.Post.views_count.desc()
    ).limit(limit).all()

def get_recent_comments(db: Session, limit: int = 10):
    return db.query(models.Comment).order_by(
        models.Comment.created_at.desc()
    ).limit(limit).all()

# ==================== SEARCH ====================

def search_posts(db: Session, query: str, skip: int = 0, limit: int = 20):
    return db.query(models.Post).filter(
        or_(
            models.Post.title.contains(query),
            models.Post.content.contains(query),
            models.Post.excerpt.contains(query)
        ),
        models.Post.status == "published"
    ).offset(skip).limit(limit).all()
