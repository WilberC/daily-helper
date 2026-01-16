# Daily Helper - Backend 🧠

The backend for Daily Helper is built with **Django 6.0** and uses **Strawberry GraphQL** for a modern, type-safe API. This backend provides a robust foundation for product comparison, user management, and future daily helper functionalities.

## 🛠️ Tech Stack

- **Framework**: [Django 6.0](https://www.djangoproject.com/)
- **API**: [Strawberry GraphQL](https://strawberry.rocks/) (with [strawberry-graphql-django](https://strawberry-graphql.github.io/strawberry-graphql-django/))
- **Database**: SQLite (default for development) / PostgreSQL (recommended for production)
- **Authentication**: Session-based authentication with CORS support
- **Image Handling**: Pillow
- **Environment Management**: python-dotenv / `mise`

## 📂 Project Structure

```
backend/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings with environment-based config
│   ├── schema.py          # Root GraphQL schema (aggregates all app schemas)
│   └── urls.py            # URL routing
├── users/                 # User management app
│   ├── models.py          # Custom User model extending Django's AbstractUser
│   ├── schema.py          # GraphQL mutations (login, register, logout) and queries (me)
│   └── types.py           # GraphQL type definitions for User
├── products/              # Product catalog app
│   ├── models.py          # Category, UnitOfMeasure, Presentation, Brand, Product, ProductVariant, ProductEquivalent
│   ├── schema.py          # GraphQL queries for products
│   ├── types.py           # GraphQL type definitions
│   └── management/        # Custom management commands
│       └── commands/
│           ├── seed.py              # Master seeder
│           ├── seed_products.py    # Products & categories seeder
│           └── seed_brands.py      # Brands seeder
├── comparator/            # Price comparison app (in development)
│   └── schema.py          # Future comparison logic
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🎯 Core Apps

### `users` - User Management & Authentication

Handles user authentication and management with GraphQL API.

**Features:**

- Session-based authentication
- User registration (admin-only in frontend)
- Login/logout mutations
- Current user query (`me`)
- Staff and admin role support

**Key Models:**

- `User`: Custom user model with `isStaff` flag for role-based access

**GraphQL Operations:**

- `login(username, password)`: Authenticate user and create session
- `register(input)`: Create new user (requires authentication)
- `logout()`: Destroy session
- `me`: Get current authenticated user

### `products` - Product Catalog

Manages the product catalog with support for variants and equivalencies.

**Key Models:**

- `Category`: Product categories with color coding
- `UnitOfMeasure`: Units like kg, L, units
- `Presentation`: Package types (bottle, box, can, etc.)
- `Brand`: Product brands
- `Product`: Base product template
- `ProductVariant`: Specific product variations (e.g., Coca-Cola 500ml vs 1L)
- `ProductEquivalent`: Defines price comparison relationships

**Features:**

- Hierarchical product organization
- Support for product variations
- Price comparison logic foundation

### `comparator` - Price Comparison (In Development)

Future home for price comparison logic and analysis features.

### `config` - Project Configuration

Central configuration and schema aggregation for the entire project.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip or mise for package management

### 1. Installation

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure environment variables in `.env`:

**Development Configuration:**

```env
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Session Configuration
SESSION_COOKIE_AGE=86400
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=False

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173
FRONTEND_URL=http://localhost:5173

# Database (SQLite)
DATABASE_URL=sqlite:///db.sqlite3
```

**Production Configuration:**

```env
DEBUG=False
SECRET_KEY=<generate-new-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Session Configuration
SESSION_COOKIE_AGE=86400
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=True

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://yourdomain.com
FRONTEND_URL=https://yourdomain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

> **Security**: Generate a new `SECRET_KEY` for production:
>
> ```bash
> python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
> ```

See [.env.example](.env.example) for all available configuration options.

### 3. Database Setup

Run migrations to create database tables:

```bash
python manage.py migrate
```

### 4. Seed Initial Data

The backend includes a custom seeding system to prepopulate your database.

**Run all seeders:**

```bash
python manage.py seed
```

**Or run specific seeders:**

```bash
python manage.py seed_products  # Categories, units, presentations, products
python manage.py seed_brands    # Brand registry
```

### 5. Create Superuser (Optional)

Create an admin user for Django admin panel:

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

**Access Points:**

- GraphQL Playground: `http://127.0.0.1:8000/graphql/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## 📡 GraphQL API

The GraphQL schema is centrally defined in `config/schema.py` and aggregates sub-schemas from different apps.

### Authentication Operations

#### Login

```graphql
mutation Login($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    success
    message
    user {
      id
      username
      email
      firstName
      lastName
      isStaff
    }
  }
}
```

#### Register (Admin Only)

```graphql
mutation Register($input: RegisterInput!) {
  register(input: $input) {
    success
    message
    user {
      id
      username
      email
      isStaff
    }
  }
}
```

#### Logout

```graphql
mutation Logout {
  logout {
    success
    message
  }
}
```

#### Current User

```graphql
query Me {
  me {
    id
    username
    email
    firstName
    lastName
    isStaff
  }
}
```

### Product Queries

#### Get Categories

```graphql
query {
  categories {
    id
    name
    color
  }
}
```

#### Get Products

```graphql
query {
  products {
    id
    name
    category {
      name
      color
    }
  }
}
```

## 🧪 Management Commands

Custom Django management commands for database seeding and maintenance:

| Command         | Description                                                       |
| --------------- | ----------------------------------------------------------------- |
| `seed`          | Runs all registered seeding commands in sequence                  |
| `seed_products` | Populates categories, units, presentations, and product templates |
| `seed_brands`   | Populates the brand registry                                      |

## 🔒 Authentication & Security

The backend uses Django's session-based authentication with the following features:

- **Session Management**: Configurable session duration (default: 24 hours)
- **CORS Support**: Configured for cross-origin requests from frontend
- **Secure Cookies**: HTTPS-only cookies in production
- **CSRF Protection**: Built-in Django CSRF protection
- **Role-Based Access**: Staff and admin role support via `isStaff` flag

**Authentication Flow:**

1. User logs in via GraphQL mutation
2. Django creates session and sets session cookie
3. Frontend includes cookie in subsequent requests
4. Backend validates session on each request
5. User logs out to destroy session

## 🧩 Adding New Modules

The architecture is designed to easily accommodate new modules:

1. **Create a new Django app:**

   ```bash
   python manage.py startapp your_app_name
   ```

2. **Add the app to `INSTALLED_APPS` in `config/settings.py`:**

   ```python
   INSTALLED_APPS = [
       # ...
       'your_app_name',
   ]
   ```

3. **Define your models in `your_app_name/models.py`**

4. **Create GraphQL schema in `your_app_name/schema.py`:**

   ```python
   import strawberry

   @strawberry.type
   class Query:
       # Your queries here
       pass

   @strawberry.type
   class Mutation:
       # Your mutations here
       pass
   ```

5. **Integrate with root schema in `config/schema.py`:**

   ```python
   from your_app_name.schema import Query as YourQuery, Mutation as YourMutation

   @strawberry.type
   class Query(ProductsQuery, UsersQuery, YourQuery):
       pass
   ```

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test users
python manage.py test products
```

## 📝 Dependencies

Key dependencies (see `requirements.txt` for full list):

- `Django==6.0` - Web framework
- `strawberry-graphql==0.288.2` - GraphQL server
- `strawberry-graphql-django==0.73.0` - Django integration for Strawberry
- `django-cors-headers==4.9.0` - CORS support
- `python-dotenv==1.2.1` - Environment variable management
- `pillow==12.1.0` - Image handling

## 🔧 Troubleshooting

### CORS Issues

If frontend can't connect to backend:

- Verify `CORS_ALLOWED_ORIGINS` in `.env` includes frontend URL
- Check that django-cors-headers is installed and configured
- Ensure `corsheaders.middleware.CorsMiddleware` is in `MIDDLEWARE`

### Session Cookie Issues

If authentication doesn't persist:

- Check `SESSION_COOKIE_SAMESITE` setting (use `Lax` for development)
- Verify `SESSION_COOKIE_SECURE` is `False` for HTTP (development)
- Ensure frontend sends cookies with `credentials: 'include'`

### Database Issues

If migrations fail:

- Delete `db.sqlite3` and `*/migrations/*` files (except `__init__.py`)
- Re-run `python manage.py makemigrations` and `python manage.py migrate`

### GraphQL Playground Not Loading

- Ensure DEBUG=True in development
- Check that Strawberry is properly installed
- Verify URL configuration in `config/urls.py`

## 📄 License

This project is part of the Daily Helper system.
