# Daily Helper 🛠️

A comprehensive personal assistant application for managing daily tasks, product comparisons, and more.

## 🚀 Project Overview

Daily Helper consists of two main components:
- **Backend**: A robust Django-based API providing GraphQL endpoints for data management.
- **Frontend**: A modern Vue 3 application for a seamless user experience.

## 🏗️ Project Structure

```text
.
├── backend/       # Django 6.0 + GraphQL (Strawberry)
├── frontend/      # Vue 3 + Vite + Pinia
└── mise.toml      # Environment/tooling configuration
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.12+ (managed via `mise` or manually)
- Node.js 20+

### Backend Setup
1. Navigate to `backend/`.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run migrations: `python manage.py migrate`.
5. Seed initial data: `python manage.py seed`.
6. Start the server: `python manage.py runserver`.

### Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Start development server: `npm run dev`.

---

## 📝 Roadmap
- [x] Backend core models and seeding system.
- [ ] GraphQL API expansion.
- [ ] Frontend development (In progress).
- [ ] Product comparison logic implementation.
