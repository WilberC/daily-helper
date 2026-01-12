# Daily Helper - Backend 🧠

The backend for Daily Helper is built with **Django 6.0** and uses **Strawberry GraphQL** for a modern, type-safe API.

## 🛠️ Tech Stack

- **Framework**: [Django 6.0](https://www.djangoproject.com/)
- **API**: [Strawberry GraphQL](https://strawberry.rocks/) (with [strawberry-graphql-django](https://strawberry-graphql.github.io/strawberry-graphql-django/))
- **Database**: SQLite (default for development)
- **Image Handling**: Pillow
- **Environment Management**: `requirements.txt` / `mise`

## 📂 Key Components

- **`products` App**: Manages the core product catalog.
  - **Models**: `Category`, `UnitOfMeasure`, `Presentation`, `Brand`, `Product`, `ProductVariant`, `ProductEquivalent`.
  - **Logic**: Handles product variations (e.g., San Luis 500ml vs 1L) and defines equivalencies for price comparisons.
- **`comparator` App**: (In Development) Focuses on price comparison logic and analysis.
- **`config`**: Project-wide settings and master GraphQL schema.

## 🚀 Getting Started

### 1. Installation
Ensure you have a virtual environment active:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure it for your environment:

```bash
cp .env.example .env
```

Edit `.env` with your configuration. Key settings:

**Development (default values):**
- `DEBUG=True`
- `SESSION_COOKIE_SAMESITE=None` (required for cross-origin requests)
- `SESSION_COOKIE_SECURE=False` (HTTP is fine for local development)
- `CORS_ALLOWED_ORIGINS=http://localhost:5173`

**Production:**
- `DEBUG=False`
- `SESSION_COOKIE_SAMESITE=Lax` (more secure for same-origin)
- `SESSION_COOKIE_SECURE=True` (requires HTTPS)
- `CORS_ALLOWED_ORIGINS=https://yourdomain.com`
- Generate a new `SECRET_KEY`:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

See `.env.example` for all available configuration options.

### 3. Database Setup
```bash
python manage.py migrate
```

### 4. Seeding Data
The backend includes a custom seeding system to prepopulate your database with essential reference data and sample products.

Run the master seed command:
```bash
python manage.py seed
```

Or run specific seeders:
```bash
python manage.py seed_products
python manage.py seed_brands
```

### 5. Running the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/graphql/` to access the GraphQL Playground.

## 📡 API Overview

The GraphQL schema is centrally defined in `config/schema.py`. It aggregates sub-schemas from different apps.

### Example Query (Categories)
```graphql
query {
  categories {
    id
    name
    color
  }
}
```

## 🧪 Management Commands

- `seed`: Runs all registered seeding commands in order.
- `seed_products`: Populates categories, units, presentations, and product templates.
- `seed_brands`: Populates the brand registry.
