# Daily Helper 🛠️

A comprehensive personal assistant application for managing daily tasks, product comparisons, and user management. Built with modern web technologies, featuring a Django GraphQL backend and a Vue 3 frontend with a beautiful dark mode interface.

## 🚀 Project Overview

Daily Helper is a full-stack web application designed to streamline daily management tasks. The system is architected for scalability and maintainability, with a modular backend structure that makes adding new features straightforward without affecting the core architecture.

**Key Capabilities:**

- 🔐 Secure user authentication and role-based access control
- 📊 Product catalog management with variant support
- 🔍 Product comparison foundation (in development)
- 👥 User management with admin interface
- 🌙 Modern dark mode UI with excellent accessibility

## 🏗️ Architecture

Daily Helper consists of two main components:

### Backend - Django GraphQL API

- **Framework**: Django 6.0
- **API Layer**: Strawberry GraphQL
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: Session-based with CORS support

**Apps:**

- `users` - Authentication & user management
- `products` - Product catalog with variants
- `comparator` - Price comparison (in development)
- `config` - Project configuration & schema aggregation

### Frontend - Vue 3 SPA

- **Framework**: Vue 3 with Composition API & TypeScript
- **UI Library**: PrimeVue 4.x (Aura preset)
- **Styling**: Tailwind CSS with custom dark theme
- **State**: Pinia
- **GraphQL Client**: urql
- **Build Tool**: Vite 7

## 📊 Project Structure

```
daily-helper/
├── backend/               # Django GraphQL API
│   ├── config/           # Project settings & root schema
│   ├── users/            # User management & authentication
│   ├── products/         # Product catalog
│   ├── comparator/       # Comparison logic (in development)
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md         # Backend-specific documentation
│
├── frontend/             # Vue 3 SPA
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── views/        # Page-level components
│   │   ├── stores/       # Pinia stores
│   │   ├── router/       # Vue Router configuration
│   │   ├── composables/  # Reusable composition functions
│   │   └── graphql/      # GraphQL operations
│   ├── .agent/workflows/ # Development guidelines
│   ├── package.json
│   └── README.md         # Frontend-specific documentation
│
├── mise.toml             # Environment/tooling configuration
└── README.md             # This file
```

## ✨ Features

### Current Features

- ✅ **User Authentication**: Session-based login/logout with role-based access
- ✅ **User Management**: Admin interface for creating staff and admin users
- ✅ **Product Catalog**: Hierarchical product organization with variants
- ✅ **Dark Mode UI**: Exclusive dark theme with custom color palette
- ✅ **GraphQL API**: Type-safe API with Strawberry GraphQL
- ✅ **Responsive Design**: Mobile, tablet, and desktop support
- ✅ **Accessibility**: WCAG 2.1 AA compliant

### In Development

- 🚧 **Product Comparison**: Advanced price comparison logic
- 🚧 **Daily Tasks**: Task management features
- 🚧 **Additional Modules**: Easily extensible architecture

## 🛠️ Quick Start

### Prerequisites

- **Python**: 3.12+ (managed via `mise` or manually)
- **Node.js**: ^20.19.0 || >=22.12.0
- **Bun**: Latest version (or npm)

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment:

```bash
cp .env.example .env
# Edit .env with your configuration (defaults work for development)
```

Run migrations and seed data:

```bash
python manage.py migrate
python manage.py seed
```

Start the development server:

```bash
python manage.py runserver
```

**Backend is now running at:** `http://localhost:8000`

📖 **For detailed backend documentation, see:** [backend/README.md](backend/README.md)

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
bun install  # or: npm install
```

Start the development server:

```bash
bun run dev  # or: npm run dev
```

**Frontend is now running at:** `http://localhost:5173`

📖 **For detailed frontend documentation, see:** [frontend/README.md](frontend/README.md)

### 3. Access the Application

1. Open your browser to `http://localhost:5173`
2. Login with credentials created during backend seeding or create a superuser:
   ```bash
   cd backend
   python manage.py createsuperuser
   ```

## 🔒 Authentication

The application uses session-based authentication:

1. **Login**: Users authenticate via the frontend login page
2. **Session**: Django creates a session cookie
3. **Authorization**: Routes and operations are protected based on user roles
4. **Roles**:
   - **Admin** (`isStaff: true`): Full access, can create users
   - **Staff** (`isStaff: false`): Limited access, dashboard only

## 📡 API Documentation

The backend provides a GraphQL API accessible at `http://localhost:8000/graphql/`

**Key Operations:**

- `login(username, password)` - Authenticate user
- `register(input)` - Create new user (admin only)
- `logout()` - Destroy session
- `me` - Get current user
- `categories` - List product categories
- `products` - List products with variants

Visit the GraphQL Playground for interactive documentation and schema exploration.

## 🧩 Adding New Modules

The architecture is designed for easy extensibility. New modules can be added without affecting existing functionality:

### Backend (Django App)

1. Create new app: `python manage.py startapp module_name`
2. Add models and business logic
3. Create GraphQL schema
4. Integrate schema in `config/schema.py`
5. Run migrations

See [backend/README.md](backend/README.md#adding-new-modules) for detailed instructions.

### Frontend (Feature Module)

1. Create components in `src/components/module_name/`
2. Add views in `src/views/`
3. Define types in `src/types/`
4. Create GraphQL operations in `src/graphql/`
5. Add routes in `src/router/`

See [frontend/README.md](frontend/README.md#adding-new-features) for detailed instructions.

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
bun run test:unit     # Unit tests (Vitest)
bun run test:e2e      # E2E tests (Playwright)
```

## 📝 Development Workflow

The frontend includes comprehensive workflow guidelines in `.agent/workflows/`:

- **Code Principles**: Architecture and organization
- **Component Best Practices**: Component development patterns
- **Styling Guidelines**: Tailwind CSS and theming
- **Accessibility Guidelines**: A11y best practices
- **UI/UX Principles**: Design patterns and consistency

## 🔧 Configuration

### Environment Variables

**Backend** (`.env`):

- `DEBUG` - Debug mode (True/False)
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `CORS_ALLOWED_ORIGINS` - Allowed frontend origins
- `SESSION_*` - Session cookie settings

**Frontend** (`.env.local`):

- `VITE_API_URL` - Backend GraphQL endpoint

See `.env.example` files in respective directories for complete configuration options.

## 🐛 Troubleshooting

### CORS Issues

- Ensure `CORS_ALLOWED_ORIGINS` in backend `.env` includes frontend URL
- Verify `django-cors-headers` is installed on backend

### Session Authentication Issues

- Check `SESSION_COOKIE_SAMESITE` setting in backend
- Verify `credentials: 'include'` in frontend GraphQL client
- Ensure both services are on same domain or CORS is properly configured

### GraphQL Connection Issues

- Verify backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env.local`
- Test GraphQL endpoint directly: `http://localhost:8000/graphql/`

### Database Issues

- Delete `db.sqlite3` and re-run migrations if needed
- Run `python manage.py seed` to repopulate data

For more detailed troubleshooting, see the module-specific README files.

## 📚 Documentation

- **[Backend Documentation](backend/README.md)** - Django API, models, GraphQL operations
- **[Frontend Documentation](frontend/README.md)** - Vue components, routing, state management
- **[User Management Feature](USER_MANAGEMENT_FEATURE.md)** - Authentication system details

## 🗺️ Roadmap

- [x] Backend core models and seeding system
- [x] User authentication and management
- [x] GraphQL API with Strawberry
- [x] Frontend with Vue 3 and dark mode
- [x] Session-based authentication
- [x] User management interface
- [ ] Product comparison logic implementation
- [ ] Daily task management features
- [ ] Additional helper modules
- [ ] Production deployment guides

## 🤝 Contributing

The project is designed to easily accommodate new features and modules. The modular architecture ensures that new additions don't affect existing functionality or require changes to core commands.

## 📄 License

This project is a personal assistant application built for daily management tasks.

---

**Quick Commands:**

```bash
# Start backend
cd backend && python manage.py runserver

# Start frontend
cd frontend && bun run dev

# Run all seeders
cd backend && python manage.py seed

# Create superuser
cd backend && python manage.py createsuperuser
```
