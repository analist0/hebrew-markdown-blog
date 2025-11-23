"""Simple blog API for demo"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Hebrew Markdown Blog API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    id: int
    title: str
    content: str
    slug: str
    created_at: datetime = datetime.now()

# Sample data
posts_db = [
    {
        "id": 1,
        "title": "ברוכים הבאים לבלוג שלי",
        "slug": "welcome-to-my-blog",
        "content": "# שלום עולם!\n\nזה הפוסט הראשון שלי בבלוג Markdown בעברית.",
        "excerpt": "פוסט ראשון בבלוג",
        "views": 42,
        "created_at": "2025-11-23T10:00:00"
    },
    {
        "id": 2,
        "title": "איך לבנות בלוג עם FastAPI",
        "slug": "build-blog-with-fastapi",
        "content": "# FastAPI מדהים\n\nבואו נלמד איך לבנות API מהיר.",
        "excerpt": "מדריך FastAPI",
        "views": 156,
        "created_at": "2025-11-23T11:00:00"
    },
    {
        "id": 3,
        "title": "Next.js + FastAPI = ❤️",
        "slug": "nextjs-fastapi-love",
        "content": "# Full-Stack מושלם\n\nשילוב מנצח של טכנולוגיות.",
        "excerpt": "שילוב טכנולוגיות",
        "views": 289,
        "created_at": "2025-11-23T12:00:00"
    }
]

@app.get("/")
def root():
    return {
        "message": "🇮🇱 Hebrew Markdown Blog API",
        "version": "1.0.0",
        "status": "✅ Running",
        "endpoints": {
            "posts": "/api/posts",
            "post": "/api/posts/{id}",
            "docs": "/docs"
        }
    }

@app.get("/api/posts")
def get_posts(skip: int = 0, limit: int = 10):
    return {
        "total": len(posts_db),
        "posts": posts_db[skip:skip+limit]
    }

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return {"error": "Post not found"}
    return post

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Hebrew Markdown Blog API...")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🌐 Frontend should run on: http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
