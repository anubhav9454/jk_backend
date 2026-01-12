<div align="center">

# 📚 Book Management Agent

**Intelligent book management system with RAG capabilities, user management, and document handling**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Quick Start](#-quick-start) • [Features](#-features) • [API Reference](#-api-reference) • [Documentation](#-documentation)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [Architecture](#-architecture)
- [Development Guide](#-development-guide)
- [Testing](#-testing)
- [Contributing](#-contributing)

---

## 🎯 Overview

Book Management Agent is a comprehensive REST API built with FastAPI that provides intelligent book management capabilities powered by RAG (Retrieval-Augmented Generation). The system enables semantic search, AI-powered summaries, user authentication, and document management with seamless integration between development and production environments.

### Key Highlights

- 🔍 **Semantic Search**: Natural language queries with vector embeddings
- 🤖 **AI Integration**: LLaMA 3 powered summaries and recommendations
- 🔐 **Secure Authentication**: JWT-based with role-based access control
- 📦 **Flexible Storage**: Local development or AWS S3 production deployment
- 🧪 **Well Tested**: Comprehensive test suite with mock database support

---

## ✨ Features

<details>
<summary><b>📚 Book Management</b></summary>

- Complete CRUD operations for books
- Author and Genre management with foreign key relationships
- Book reviews with rating system
- AI-generated summaries using LLaMA 3
- Genre-based recommendations

</details>

<details>
<summary><b>🔍 RAG Pipeline</b></summary>

- Semantic search using natural language queries
- Vector embeddings via sentence-transformers
- Automatic indexing on book/review changes
- Cosine similarity matching for relevant results
- Manual reindexing capabilities

</details>

<details>
<summary><b>👥 User Management</b></summary>

- JWT-based authentication system
- Role-based access control (RBAC)
- Granular permissions (read/write/delete/admin)
- Admin-only user management endpoints
- Secure password hashing (SHA-256)

</details>

<details>
<summary><b>📄 Document Management</b></summary>

- File upload with size tracking
- Secure file download
- AWS S3 integration for production
- Local file handling for development
- Metadata management

</details>

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python** 3.8 or higher
- **PostgreSQL** database
- **OpenRouter API Key** (for AI features)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd jk_backend
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=book_mgmt
DB_USER=your_user
DB_PASSWORD=your_password

# AI Services
OPENROUTER_API_KEY=your_openrouter_key

# AWS S3 (Production)
USE_S3=false
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your_bucket_name
AWS_REGION=us-east-1
```

#### 4. Initialize Database

```bash
# Create database tables
python -c "from app.database import engine, Base; from app.models import *; import asyncio; asyncio.run(Base.metadata.create_all(bind=engine.sync_engine))"

# Run migrations
python migrate_author_genre.py
```

#### 5. Seed Sample Data (Optional)

```bash
python add_sample_books.py
```

#### 6. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_HOST` | PostgreSQL host | Yes | - |
| `DB_PORT` | PostgreSQL port | Yes | `5432` |
| `DB_NAME` | Database name | Yes | - |
| `DB_USER` | Database user | Yes | - |
| `DB_PASSWORD` | Database password | Yes | - |
| `OPENROUTER_API_KEY` | OpenRouter API key for AI | Yes | - |
| `USE_S3` | Enable AWS S3 storage | No | `false` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Conditional | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Conditional | - |
| `S3_BUCKET_NAME` | S3 bucket name | Conditional | - |
| `AWS_REGION` | AWS region | Conditional | `us-east-1` |

### Development vs Production

#### Development Mode (Default)

- ✅ Local file storage (metadata only)
- ✅ S3 disabled
- ✅ Minimal dependencies
- ✅ Placeholder file downloads

#### Production Mode

Enable in `.env`:

```env
USE_S3=true
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=your_bucket
```

- ✅ AWS S3 file storage
- ✅ Presigned URL downloads
- ✅ Requires `boto3` dependency

---

## 📖 API Reference

### Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
|:------:|:--------:|:-------------:|:------------|
| `POST` | `/auth/signup` | ❌ | Register a new user |
| `POST` | `/auth/login` | ❌ | User login |
| `POST` | `/auth/create-admin` | ❌ | Create admin user |
| `POST` | `/auth/logout` | ✅ | User logout |

### Book Management

| Method | Endpoint | Auth Required | Description |
|:------:|:--------:|:-------------:|:------------|
| `POST` | `/books` | ❌ | Create new book |
| `GET` | `/books` | ❌ | List all books |
| `GET` | `/books/{id}` | ❌ | Get book by ID |
| `PUT` | `/books/{id}` | ✅ | Update book |
| `DELETE` | `/books/{id}` | ✅ | Delete book |
| `POST` | `/books/{id}/generate-summary` | ❌ | Generate AI summary |
| `GET` | `/books/dropdown/authors` | ❌ | Get authors dropdown |
| `GET` | `/books/dropdown/genres` | ❌ | Get genres dropdown |

### Authors & Genres

| Method | Endpoint | Description |
|:------:|:--------:|:------------|
| `POST` | `/authors` | Create author |
| `GET` | `/authors` | List authors |
| `PUT` | `/authors/{id}` | Update author |
| `DELETE` | `/authors/{id}` | Delete author |
| `POST` | `/genres` | Create genre |
| `GET` | `/genres` | List genres |
| `PUT` | `/genres/{id}` | Update genre |
| `DELETE` | `/genres/{id}` | Delete genre |

### Reviews

| Method | Endpoint | Description |
|:------:|:--------:|:------------|
| `POST` | `/books/{id}/reviews` | Add review |
| `GET` | `/books/{id}/reviews` | Get reviews |
| `GET` | `/books/{id}/summary` | Get review summary |

### Search & RAG

| Method | Endpoint | Description |
|:------:|:--------:|:------------|
| `GET/POST` | `/search` | Semantic search |
| `POST` | `/reindex-all` | Reindex all books |
| `POST` | `/books/{id}/reindex` | Reindex specific book |
| `GET` | `/debug/embeddings` | Debug embeddings |

### User Management (Admin Only)

| Method | Endpoint | Description |
|:------:|:--------:|:------------|
| `POST` | `/admin/users/` | Create user |
| `GET` | `/admin/users/` | List users |
| `PUT` | `/admin/users/{id}` | Update user |
| `DELETE` | `/admin/users/{id}` | Delete user |
| `GET` | `/admin/users/roles` | List roles |
| `POST` | `/admin/users/roles` | Create role |

### Documents

| Method | Endpoint | Auth Required | Description |
|:------:|:--------:|:-------------:|:------------|
| `POST` | `/documents/upload` | ❌ | Upload document |
| `GET` | `/documents/` | ❌ | List documents |
| `GET` | `/documents/{id}/download` | ❌ | Download document |
| `DELETE` | `/documents/{id}` | ✅ | Delete document |

### Other Endpoints

| Method | Endpoint | Description |
|:------:|:--------:|:------------|
| `GET` | `/recommendations` | Get recommendations |
| `POST` | `/generate-summary` | Generate summary |

> 📘 **Interactive API Documentation**: Visit `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc) when the server is running.

---

## 💾 Database Schema

### Entity Models

```
Authors
├── id (Primary Key)
└── name (Unique)

Genres
├── id (Primary Key)
└── name (Unique)

Books
├── id (Primary Key)
├── title
├── author_id (Foreign Key → Authors)
├── genre_id (Foreign Key → Genres)
├── year_published
└── summary

Reviews
├── id (Primary Key)
├── book_id (Foreign Key → Books)
├── user_id
├── review_text
└── rating

Users
├── id (Primary Key)
├── username
├── password_hash
├── is_active
└── created_at

Roles
├── id (Primary Key)
├── name
├── can_read
├── can_write
├── can_delete
└── is_admin
```

### Relationships

- **Books → Authors**: Many-to-One
- **Books → Genres**: Many-to-One
- **Books → Reviews**: One-to-Many
- **Users → Roles**: Many-to-Many

---

## 🏗️ Architecture

### Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with SHA-256 hashing
- **Vector Search**: sentence-transformers (all-MiniLM-L6-v2)
- **Similarity**: scikit-learn cosine similarity
- **AI**: OpenRouter API (LLaMA 3)
- **Storage**: Local filesystem / AWS S3

### System Components

#### RAG Pipeline

```
Book Content → Embeddings → Vector Store → Similarity Search → Results
     ↓              ↓             ↓              ↓
  Indexing    Transformers   In-Memory      Cosine Match
```

- **Embeddings**: sentence-transformers model
- **Vector Store**: In-memory with scikit-learn
- **Indexing**: Automatic on create/update/review
- **Search**: Semantic similarity matching

#### Authentication Flow

```
User → Login → JWT Token → Protected Endpoints → Role Check → Access
```

- **Tokens**: Stateless JWT authentication
- **Roles**: Granular permissions system
- **Security**: SHA-256 password hashing

---

## 💻 Development Guide

### Project Structure

```
jk_backend/
├── app/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core configuration and security
│   ├── db/            # Database session and health
│   ├── models/        # SQLAlchemy models
│   ├── repositories/  # Data access layer
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── main.py        # Application entry point
├── tests/             # Test suite
└── requirements.txt   # Dependencies
```

### Usage Examples

#### Create Author and Genre

```bash
# Create author
curl -X POST "http://localhost:8000/authors" \
  -H "Content-Type: application/json" \
  -d '{"name": "J.K. Rowling"}'

# Create genre
curl -X POST "http://localhost:8000/genres" \
  -H "Content-Type: application/json" \
  -d '{"name": "Fantasy"}'
```

#### Create Book

```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter",
    "author_id": 1,
    "genre_id": 1,
    "year_published": 1997
  }'
```

#### Update Book

```bash
curl -X PUT "http://localhost:8000/books/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "author_id": 2,
    "genre_id": 3
  }'
```

---

## 🧪 Testing

### Run Test Suite

```bash
# Using test runner script
python run_tests.py

# Or with pytest directly
pytest tests/ -v
```

### Test Coverage

- ✅ Unit tests for all endpoints
- ✅ Mock database support
- ✅ Authentication testing
- ✅ CRUD operation validation
- ✅ Search functionality tests

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add tests** for your new features
4. **Run** the test suite to ensure everything passes
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Development Guidelines

- Write tests for all new features
- Follow PEP 8 style guidelines
- Update documentation for API changes
- Ensure backward compatibility when possible

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for intelligent book management**

[Report Bug](https://github.com/your-repo/issues) • [Request Feature](https://github.com/your-repo/issues) • [Documentation](http://localhost:8000/docs)

</div>
