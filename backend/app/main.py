"""
Hebrew Markdown Blog - FastAPI Backend
Main application file with all CRUD endpoints
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import os

from .database import engine, get_db, Base
from . import models, schemas, crud, auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hebrew Markdown Blog API",
    description="Advanced blog platform with Markdown, CMS, and analytics",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# ==================== AUTH ENDPOINTS ====================

@app.post("/api/auth/register", response_model=schemas.User, tags=["Authentication"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register new user (admin/author)"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/auth/login", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@app.get("/api/auth/me", response_model=schemas.User, tags=["Authentication"])
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """Get current logged in user"""
    return current_user

# ==================== POSTS CRUD ====================

@app.get("/api/posts", response_model=List[schemas.Post], tags=["Posts"])
def get_posts(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all posts with filtering and pagination"""
    return crud.get_posts(
        db,
        skip=skip,
        limit=limit,
        status=status,
        category=category,
        tag=tag,
        search=search
    )

@app.get("/api/posts/{slug}", response_model=schemas.PostDetail, tags=["Posts"])
def get_post(slug: str, db: Session = Depends(get_db)):
    """Get single post by slug"""
    post = crud.get_post_by_slug(db, slug=slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Increment view count
    crud.increment_post_views(db, post_id=post.id)

    return post

@app.post("/api/posts", response_model=schemas.Post, tags=["Posts"])
def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create new post (authenticated)"""
    return crud.create_post(db=db, post=post, author_id=current_user.id)

@app.put("/api/posts/{post_id}", response_model=schemas.Post, tags=["Posts"])
def update_post(
    post_id: str,
    post: schemas.PostUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Update post (authenticated)"""
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is author or admin
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.update_post(db=db, post_id=post_id, post=post)

@app.delete("/api/posts/{post_id}", tags=["Posts"])
def delete_post(
    post_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete post (authenticated)"""
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if user is author or admin
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    crud.delete_post(db=db, post_id=post_id)
    return {"message": "Post deleted successfully"}

# ==================== COMMENTS CRUD ====================

@app.get("/api/posts/{post_id}/comments", response_model=List[schemas.Comment], tags=["Comments"])
def get_post_comments(post_id: str, db: Session = Depends(get_db)):
    """Get all comments for a post"""
    return crud.get_post_comments(db, post_id=post_id)

@app.post("/api/posts/{post_id}/comments", response_model=schemas.Comment, tags=["Comments"])
def create_comment(
    post_id: str,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    """Create new comment"""
    return crud.create_comment(db=db, comment=comment, post_id=post_id)

@app.put("/api/comments/{comment_id}", response_model=schemas.Comment, tags=["Comments"])
def update_comment_status(
    comment_id: str,
    status: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Update comment status (approve/reject) - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return crud.update_comment_status(db=db, comment_id=comment_id, status=status)

@app.delete("/api/comments/{comment_id}", tags=["Comments"])
def delete_comment(
    comment_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete comment - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    crud.delete_comment(db=db, comment_id=comment_id)
    return {"message": "Comment deleted successfully"}

# ==================== RATINGS ====================

@app.post("/api/posts/{post_id}/rate", response_model=schemas.Rating, tags=["Ratings"])
def rate_post(
    post_id: str,
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db)
):
    """Rate a post (1-5 stars)"""
    return crud.create_rating(db=db, rating=rating, post_id=post_id)

@app.get("/api/posts/{post_id}/rating", tags=["Ratings"])
def get_post_rating(post_id: str, db: Session = Depends(get_db)):
    """Get average rating for post"""
    return crud.get_post_average_rating(db, post_id=post_id)

# ==================== CATEGORIES CRUD ====================

@app.get("/api/categories", response_model=List[schemas.Category], tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    return crud.get_categories(db)

@app.post("/api/categories", response_model=schemas.Category, tags=["Categories"])
def create_category(
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create new category - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return crud.create_category(db=db, category=category)

@app.put("/api/categories/{category_id}", response_model=schemas.Category, tags=["Categories"])
def update_category(
    category_id: str,
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Update category - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return crud.update_category(db=db, category_id=category_id, category=category)

@app.delete("/api/categories/{category_id}", tags=["Categories"])
def delete_category(
    category_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete category - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    crud.delete_category(db=db, category_id=category_id)
    return {"message": "Category deleted successfully"}

# ==================== TAGS CRUD ====================

@app.get("/api/tags", response_model=List[schemas.Tag], tags=["Tags"])
def get_tags(db: Session = Depends(get_db)):
    """Get all tags"""
    return crud.get_tags(db)

@app.post("/api/tags", response_model=schemas.Tag, tags=["Tags"])
def create_tag(
    tag: schemas.TagCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create new tag - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return crud.create_tag(db=db, tag=tag)

# ==================== MEDIA CRUD ====================

@app.get("/api/media", response_model=List[schemas.Media], tags=["Media"])
def get_media(
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get media library - Authenticated"""
    return crud.get_media(db, skip=skip, limit=limit)

@app.post("/api/media/upload", response_model=schemas.Media, tags=["Media"])
def upload_media(
    media: schemas.MediaCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Upload media file - Authenticated"""
    return crud.create_media(db=db, media=media, user_id=current_user.id)

@app.delete("/api/media/{media_id}", tags=["Media"])
def delete_media(
    media_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete media - Authenticated"""
    crud.delete_media(db=db, media_id=media_id)
    return {"message": "Media deleted successfully"}

# ==================== ANALYTICS ====================

@app.post("/api/analytics/view", tags=["Analytics"])
def track_page_view(
    view: schemas.PageViewCreate,
    db: Session = Depends(get_db)
):
    """Track page view"""
    return crud.create_page_view(db=db, view=view)

@app.get("/api/analytics/posts/{post_id}", tags=["Analytics"])
def get_post_analytics(
    post_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics for specific post - Authenticated"""
    return crud.get_post_analytics(db, post_id=post_id)

@app.get("/api/analytics/dashboard", tags=["Analytics"])
def get_dashboard_analytics(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall dashboard analytics - Admin only"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {
        "total_posts": crud.count_posts(db),
        "total_views": crud.count_total_views(db),
        "total_comments": crud.count_comments(db),
        "popular_posts": crud.get_popular_posts(db, limit=10),
        "recent_comments": crud.get_recent_comments(db, limit=10),
    }

# ==================== SEARCH ====================

@app.get("/api/search", response_model=List[schemas.Post], tags=["Search"])
def search_posts(
    q: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Full-text search for posts"""
    return crud.search_posts(db, query=q, skip=skip, limit=limit)

# ==================== HEALTH CHECK ====================

@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
