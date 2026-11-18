# Library.io — Intelligent Library Management & AI Book Recommendation System

> **A modern, full-stack digital library platform featuring hybrid machine-learning book recommendations, Elasticsearch-powered typo-tolerant search, real-time circulation tracking, role-based governance, and containerized deployment.**

---

## 🎓 Academic & Industry Overview

### 1. Problem Statement
Traditional university library management systems often suffer from clunky, outdated user interfaces, rigid catalog searches that fail upon the slightest spelling typo, absence of intelligent personalized book discovery, and manual paperwork for circulation, renewals, and overdue penalty tracking.

### 2. The Solution
**Library.io** transforms institutional library operations into a modern digital platform. It combines:
- A responsive, high-performance **React 18 Single Page Application (SPA)** with tailored portals for Students, Librarians, and Administrators.
- A secure **Django REST Framework** backend with PostgreSQL persistence and stateless JWT token rotation.
- An **AI Recommendation Engine** utilizing TF-IDF cosine similarity and collaborative user-item correlation to provide personalized reading suggestions.
- An **Elasticsearch 8.x search cluster** with edge n-gram live autocomplete and fuzzy matching, backed by an automated zero-downtime PostgreSQL ORM fallback engine.

### 3. Innovation & Key Differentiators
- **Hybrid AI Discovery ($0.6 \times \text{Content} + 0.4 \times \text{Collaborative}$)**: Combines catalog natural language metadata with peer reading correlation, automatically transitioning new students from cold-start popularity picks to personalized recommendations.
- **Typo-Tolerant Search with ORM Fallback**: Delivers relevant search results even with misspelled queries (e.g. *"pyhton"* $\to$ *Python*), while remaining fully operational via database fallback if Elasticsearch is offline.
- **Real-Time Circulation & Fine Automation**: Automates 14-day lending windows, fine calculation ($1.00/day), 7-day loan extensions, and desk check-ins.
- **Dual-Portal Role Architecture**: Distinct workflows for Students (Dashboard, Catalog, Reading Analytics, Loans) and Staff (Inventory CRUD, Circulation Desk, Overdue Settlement, Institutional Telemetry).

---

## 🏗 System Architecture

```
                                  ┌───────────────────────────────┐
                                  │      Client Web Browser       │
                                  └──────────────┬────────────────┘
                                                 │ HTTP / HTTPS (Port 80)
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │     Nginx Gateway Router      │
                                  └──────┬─────────────────┬──────┘
                                         │                 │
                    / (Frontend SPA)     │                 │ /api/* (REST API Calls)
                                         ▼                 ▼
              ┌────────────────────────────┐    ┌────────────────────────────┐
              │      library-frontend      │    │       library-backend      │
              │   (React 18 + Vite + Nginx)│    │   (Django 5 + Gunicorn)    │
              └────────────────────────────┘    └──────┬───────────────┬─────┘
                                                       │               │
                                          PostgreSQL   │               │ Elasticsearch
                                          Port 5432    ▼               ▼ Port 9200
                                      ┌────────────────────┐ ┌────────────────────┐
                                      │  library-postgres  │ │library-elasticsearch│
                                      │  (PostgreSQL 16)   │ │  (Elasticsearch 8) │
                                      └────────────────────┘ └────────────────────┘
```

---

## 🛠 Tech Stack

| Domain | Technologies & Libraries |
| :--- | :--- |
| **Frontend** | React 18, Vite 5, Tailwind CSS, Lucide Icons, Chart.js, React-Chartjs-2, Axios |
| **Backend** | Python 3.12/3.13, Django 5.x, Django REST Framework, Gunicorn WSGI |
| **Database** | PostgreSQL 16 (Authoritative datastore with SQLite support for local dev) |
| **Search Engine**| Elasticsearch 8.x / 9.x, Edge N-Gram Analyzers, Fuzzy Query Builders |
| **AI / Machine Learning** | `scikit-learn` (TF-IDF Vectorizer, Cosine Similarity), `numpy`, `pandas` |
| **Authentication** | `djangorestframework-simplejwt` (Stateless JWT with auto-refresh interceptor) |
| **DevOps & Containers** | Docker, Docker Compose, Multi-stage builds, Nginx Reverse Proxy Gateway |

---

## 🔐 Default Demo Accounts

| Role | Email | Password | Cardholder ID | Access Privileges |
|---|---|---|---|---|
| **System Admin** | `admin@library.io` | `AdminPass123!` | `LIB-ADM-001` | Full system governance, role promotion, user quotas |
| **Head Librarian** | `librarian@library.io` | `LibrarianPass123!` | `LIB-STF-001` | Inventory CRUD, Issue Desk, Overdue fines settlement |
| **Student Member** | `alex@student.io` | `StudentPass123!` | `LIB-STU-1001` | Browse catalog, borrow/renew books, AI recommendations |
| **Student Member** | `sarah@student.io` | `StudentPass123!` | `LIB-STU-1002` | Standard cardholder profile |

---

## 🚀 Quickstart & Deployment Guide

### Option 1: Docker Compose Production Deployment (Recommended)

```bash
# 1. Clone repository and prepare environment
cp .env.example .env

# 2. Build and launch all 5 containers
docker compose up -d --build

# 3. Check running service health
docker compose ps

# 4. View container logs
docker compose logs -f backend
```

Access the application in your browser:
- **Frontend Web Portal:** `http://localhost/`
- **Backend API Root:** `http://localhost/api/`
- **System Health Probe:** `http://localhost/api/health/`

---

### Option 2: Cloud Deployment on Render (Public Internet Live)

Library.io is 100% production-ready for deployment on **Render.com** (with free tier support for PostgreSQL, Django Web Service, and React Static Site).

#### Method A: One-Click Blueprint Deployment (Recommended)
1. Push this repository to **GitHub** or **GitLab**.
2. Log into [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** $\to$ **Blueprint**.
4. Connect your repository containing `render.yaml`.
5. Render will automatically provision:
   - `libraryio-postgres` (PostgreSQL Database)
   - `libraryio-backend` (Django REST API Web Service with WhiteNoise & Gunicorn)
   - `libraryio-frontend` (React + Vite Static Site with SPA rewrites)
6. Click **Apply**. Render will automatically run `./build.sh` (which installs dependencies, runs database migrations, and executes `seed_production` to populate accounts and public-domain ebooks).

#### Method B: Manual Dashboard Setup

1. **Create PostgreSQL Database (`libraryio-postgres`)**:
   - In Render Dashboard, create a new **PostgreSQL**.
   - Copy the **Internal Database URL**.

2. **Create Backend Web Service (`libraryio-backend`)**:
   - **Type**: Web Service (Python runtime).
   - **Root Directory**: `backend`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn library_core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120`
   - **Environment Variables**:
     - `DATABASE_URL`: *(Your Render PostgreSQL Connection String)*
     - `DEBUG`: `False`
     - `SECRET_KEY`: *(Generate a random 50-character string)*
     - `ALLOWED_HOSTS`: `localhost,127.0.0.1,.onrender.com`
     - `FRONTEND_URL`: `https://your-frontend-subdomain.onrender.com`
     - `CORS_ALLOW_ALL_ORIGINS`: `False`

3. **Create Frontend Static Site (`libraryio-frontend`)**:
   - **Type**: Static Site.
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_BASE_URL`: `https://your-backend-subdomain.onrender.com/api`

---

### Option 3: Local Development Setup (Host Machine)

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Apply database migrations & seed initial demo data
python manage.py migrate
python manage.py seed_production

# Start Django Development Server
python manage.py runserver 127.0.0.1:8000
```

#### 2. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 📡 API Reference Matrix

### 1. Authentication & Member Management (`/api/auth/`)
- `POST /api/auth/register/` — Cardholder self-registration (enforces `STUDENT` role)
- `POST /api/auth/login/` — Obtain JWT access & refresh tokens
- `POST /api/auth/token/refresh/` — Refresh expired access token
- `GET/PUT /api/auth/profile/` — Cardholder self-profile management
- `GET/PATCH /api/auth/members/` — *(Staff/Admin)* Member directory & borrow quota governance

### 2. Search Engine (`/api/search/`)
- `GET /api/search/books/?q=...` — Typo-tolerant search across titles, authors, categories, ISBNs
- `GET /api/search/suggestions/?q=...` — Instant live prefix autocomplete suggestions

### 3. Books, Digital Reader & Catalog (`/api/books/`)
- `GET /api/books/` — List catalog books with category & rating filters
- `GET /api/books/{id}/` — Retrieve book details & verified student reviews
- `POST /api/books/` — *(Librarian)* Add new title to inventory (supports PDF attachment)
- `PUT/DELETE /api/books/{id}/` — *(Librarian)* Edit or delete catalog title
- `GET /api/books/{id}/read/` — *(Authenticated / Active Loan / Open Access)* Stream protected digital book PDF
- `GET/POST /api/books/{id}/progress/` — Get or persist student reading page progress
- `GET /api/books/categories/` — List genre categories
- `GET /api/books/authors/` — List authors
- `POST /api/books/ratings/` — Submit 1-5 star review and rating

### 4. Circulation & Borrowing (`/api/borrowing/`)
- `POST /api/borrowing/borrow/` — Check out book (`book_id`)
- `POST /api/borrowing/transactions/{id}/return_book/` — Check in book and calculate late fine
- `POST /api/borrowing/transactions/{id}/renew/` — Extend active loan by +7 days
- `POST /api/borrowing/transactions/{id}/pay_fine/` — *(Librarian)* Settle overdue fine
- `GET /api/borrowing/my-loans/` — Active loans for logged-in user
- `GET /api/borrowing/my-history/` — Historical returned loans ledger
- `GET /api/borrowing/overdue/` — *(Librarian)* Overdue loans across entire library

### 5. AI Recommendations (`/api/recommendations/`)
- `GET /api/recommendations/personalized/` — Tailored hybrid recommendations with match percentages

### 6. Analytics Telemetry (`/api/analytics/`)
- `GET /api/analytics/student-dashboard/` — Student reading habits & category breakdown
- `GET /api/analytics/librarian-dashboard/` — *(Staff)* Stock utilization, circulation velocity, fine revenue
- `POST /api/analytics/history/` — Log telemetry interactions (`VIEW`, `READ`, `RATE`, `WISHLIST`, `SEARCH`)

---

## 📖 Digital Book Reader & Legal Compliance

Library.io includes a built-in, secure digital book reader powered by `pdfjs-dist`:
- **Supported Format**: Standard PDF files (`.pdf`, up to 50MB).
- **Access Policy**: Requires an active physical/digital loan (`BORROWED` or `OVERDUE`), an `Open Access` flag (`is_public_domain=True`), or a Librarian/Admin staff role.
- **Reading Progress**: Automatic page synchronization with resume reading dialog (*"Continue from page X?"*), zoom controls (65%–200%), and fullscreen mode.
- **Copyright & Legal Compliance**:
  > *"Only public-domain, open-access, institutionally licensed, or otherwise authorized digital content should be uploaded to Library.io. Commercial copyrighted books are strictly prohibited from distribution."*

---

## 🧪 Automated Testing & Verification

```bash
# Run backend audit test suite (25/25 checks passing)
cd backend
python audit_test_suite.py

# Run Django unit tests (11/11 tests passing)
python manage.py test

# Run frontend production build test (0 errors)
cd ../frontend
npm run build
```

---

## 🔮 Future Scope & Enhancements

1. **Physical RFID / Barcode Scanner Support**: Direct USB HID barcode scanner input integration for circulation desk check-in.
2. **Deep Neural Embeddings**: Upgrade TF-IDF text features to sentence-transformer vector embeddings (e.g. HuggingFace `all-MiniLM-L6-v2`) for semantic concept matching.
3. **Automated Email Overdue Notifications**: Celery + Redis background tasks for sending 48-hour return reminder emails to students.
4. **EPUB Format Parsing**: Extensible reader support for reflowable EPUB typography alongside fixed PDF layouts.

