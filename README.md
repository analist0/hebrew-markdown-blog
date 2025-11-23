# 🇮🇱 Hebrew Markdown Blog - בלוג Markdown מתקדם

![Bold Magazine Design](https://img.shields.io/badge/Design-Bold%20Magazine-ec4899)
![Next.js 15](https://img.shields.io/badge/Next.js-15-black)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178c6)

פלטפורמת בלוג מתקדמת עם Markdown, CMS מלא, דירוגים, תגובות, אנליטיקס ותמיכה מלאה בעברית RTL.

## ✨ תכונות

### 📝 ניהול תוכן
- ✅ עורך Markdown מתקדם (Tiptap WYSIWYG)
- ✅ תמיכה מלאה ב-MDX (Markdown + React components)
- ✅ ניהול מדיה (תמונות, וידאו)
- ✅ קטגוריות ותגיות
- ✅ Draft/Published status
- ✅ SEO מתקדם (meta tags, sitemap)

### 🎨 עיצוב
- ✅ Bold Magazine - עיצוב נועז וצבעוני
- ✅ Responsive מושלם (Mobile-First)
- ✅ תמיכה מלאה ב-RTL (עברית)
- ✅ Dark mode
- ✅ אנימציות חלקות (Framer Motion)

### 💬 אינטראקציה
- ✅ מערכת תגובות מלאה (+ replies)
- ✅ דירוגים 5 כוכבים
- ✅ שיתוף ברשתות חברתיות
- ✅ Related posts

### 📊 אנליטיקס
- ✅ מעקב צפיות
- ✅ זמן קריאה
- ✅ מאמרים פופולריים
- ✅ מקורות טראפיק

### 🔐 אבטחה
- ✅ JWT Authentication
- ✅ Password hashing (bcrypt)
- ✅ Role-based access (admin/author)
- ✅ Input validation (Zod + Pydantic)

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** - App Router, TypeScript
- **TailwindCSS 4** - Styling
- **Tiptap 2** - Rich text editor
- **Framer Motion** - Animations
- **Tanstack Query** - Data fetching
- **Zustand** - State management

### Backend
- **FastAPI** - Python API framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Alembic** - Migrations

### Deployment (100% FREE)
- **Vercel** - Frontend
- **Railway/Render** - Backend
- **Supabase/Neon** - PostgreSQL

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 16+

### 1. Clone Repository
```bash
git clone <repo-url>
cd hebrew-markdown-blog
```

### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000
API Docs: http://localhost:8000/api/docs

### 3. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local
# Edit with your API URL

# Start development server
npm run dev
```

Frontend will run on: http://localhost:3000

## 📁 Project Structure

```
hebrew-markdown-blog/
├── frontend/                 # Next.js App
│   ├── app/
│   │   ├── (public)/        # Public routes
│   │   │   ├── page.tsx    # Homepage
│   │   │   └── blog/
│   │   │       ├── page.tsx           # Blog listing
│   │   │       └── [slug]/page.tsx    # Post page
│   │   └── (admin)/         # Admin CMS
│   │       ├── dashboard/
│   │       ├── posts/
│   │       ├── media/
│   │       └── analytics/
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── backend/                 # FastAPI App
│   ├── app/
│   │   ├── main.py         # Main app + all endpoints
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── crud.py         # CRUD operations
│   │   ├── auth.py         # Authentication
│   │   └── database.py     # Database connection
│   ├── alembic/            # Migrations
│   └── requirements.txt
│
└── README.md
```

## 🎨 Design Options

העיצוב הנוכחי: **Bold Magazine**

לצפייה בעיצובים:
- [Option 1: Modern Minimal](https://0x0.st/KVl-.html)
- [Option 2: Bold Magazine](https://0x0.st/KVlX.html) ⭐ (נבחר)
- [Option 3: Classic Elegant](https://0x0.st/KVl8.html)

## 📖 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Posts (CRUD)
- `GET /api/posts` - List posts (with filters)
- `GET /api/posts/{slug}` - Get post
- `POST /api/posts` - Create post (auth)
- `PUT /api/posts/{id}` - Update post (auth)
- `DELETE /api/posts/{id}` - Delete post (auth)

### Comments (CRUD)
- `GET /api/posts/{id}/comments` - Get comments
- `POST /api/posts/{id}/comments` - Create comment
- `PUT /api/comments/{id}` - Update status (admin)
- `DELETE /api/comments/{id}` - Delete (admin)

### Ratings
- `POST /api/posts/{id}/rate` - Rate post
- `GET /api/posts/{id}/rating` - Get average rating

### Categories & Tags (CRUD)
- `GET /api/categories` - List categories
- `POST /api/categories` - Create (admin)
- `PUT /api/categories/{id}` - Update (admin)
- `DELETE /api/categories/{id}` - Delete (admin)

### Media (CRUD)
- `GET /api/media` - List media
- `POST /api/media/upload` - Upload (auth)
- `DELETE /api/media/{id}` - Delete (auth)

### Analytics
- `POST /api/analytics/view` - Track view
- `GET /api/analytics/posts/{id}` - Post analytics
- `GET /api/analytics/dashboard` - Dashboard stats (admin)

### Search
- `GET /api/search?q=query` - Full-text search

## 🌍 Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel
```

### Railway (Backend)
```bash
cd backend
railway login
railway init
railway up
```

### Environment Variables

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/blog
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📝 Features Roadmap

- [x] Full CRUD for Posts
- [x] Comments system
- [x] Rating system
- [x] Admin CMS
- [x] Analytics
- [x] Responsive design
- [ ] Email notifications
- [ ] Social auth (Google, GitHub)
- [ ] Advanced search (Elasticsearch)
- [ ] Newsletter integration
- [ ] Export to PDF

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📄 License

MIT License - see LICENSE file

## 👨‍💻 Author

Built with 🤖 Claude Code - Full-Stack Builder

---

**🚀 Ready to start blogging!**

For questions: Open an issue on GitHub
