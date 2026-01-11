# Daily Helper - Frontend

A modern Vue 3 frontend application for the Daily Helper system, featuring user authentication and management with a sleek dark mode interface.

## 🚀 Tech Stack

- **Framework**: Vue 3 with TypeScript
- **UI Library**: PrimeVue 4.x
- **Styling**: Tailwind CSS (Dark Mode Only)
- **State Management**: Pinia
- **GraphQL Client**: urql
- **Form Validation**: vee-validate + yup
- **Routing**: Vue Router
- **Build Tool**: Vite
- **Package Manager**: Bun

## ✨ Features

- 🔐 **Authentication System**: Secure login/logout with session-based authentication
- 👥 **User Management**: Admin interface for creating staff and admin users
- 🌙 **Dark Mode**: Exclusive dark theme with custom color palette
- 📱 **Responsive Design**: Fully responsive across mobile, tablet, and desktop
- 🎨 **Modern UI**: Built with PrimeVue components
- 🔒 **Route Guards**: Protected routes based on authentication and role
- ✅ **Form Validation**: Client-side validation with helpful error messages

## 📋 Prerequisites

- **Node.js**: ^20.19.0 || >=22.12.0
- **Bun**: Latest version
- **Backend API**: Django GraphQL backend running on `http://localhost:8000`

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
bun install
```

### 2. Environment Configuration

The application uses environment variables for configuration. The default development configuration is:

```env
VITE_API_URL=http://localhost:8000/graphql/
```

To customize, create a `.env.local` file:

```bash
cp .env.development .env.local
# Edit .env.local with your configuration
```

### 3. Start Development Server

```bash
bun run dev
```

The application will be available at `http://localhost:5173`

## 🏗️ Project Structure

```
src/
├── assets/
│   └── styles/
│       └── main.css          # Global styles and Tailwind config
├── components/
│   └── users/
│       └── CreateUserForm.vue # Reusable user creation form
├── config/
│   └── api.ts                # GraphQL client configuration
├── graphql/
│   └── auth.graphql.ts       # Authentication GraphQL operations
├── router/
│   └── index.ts              # Vue Router with auth guards
├── stores/
│   └── auth.ts               # Pinia authentication store
├── types/
│   └── user.ts               # TypeScript type definitions
├── views/
│   ├── LoginView.vue         # Login page
│   ├── DashboardView.vue     # Main dashboard
│   └── UserManagementView.vue # User management (admin only)
├── App.vue                   # Root component
└── main.ts                   # Application entry point
```

## 🔑 Authentication Flow

1. **Login**: Users authenticate via the `/login` route
2. **Session**: Backend creates a session cookie
3. **Protected Routes**: Router guards check authentication status
4. **Role-Based Access**: Admin-only routes require `isStaff` flag
5. **Logout**: Destroys session and redirects to login

## 👤 User Roles

### Administrator (`isStaff: true`)
- Full system access
- Can create new admin and staff users
- Access to user management interface

### Staff (`isStaff: false`)
- Limited access
- Cannot create new users
- Dashboard access only

## 🎨 Styling

The application uses a custom dark theme with Tailwind CSS:

### Color Palette
- **Background**: `#0f172a` (dark-bg)
- **Surface**: `#1e293b` (dark-surface)
- **Border**: `#334155` (dark-border)
- **Text**: `#f1f5f9` (dark-text)
- **Text Secondary**: `#94a3b8` (dark-text-secondary)

### PrimeVue Theme
- Preset: Aura
- Dark mode selector: `.dark` class
- Custom component styling in component `<style>` blocks

## 📝 Available Scripts

```bash
# Development
bun run dev              # Start dev server

# Build
bun run build            # Type-check and build for production
bun run build-only       # Build without type-checking

# Testing
bun run test:unit        # Run unit tests
bun run test:e2e         # Run end-to-end tests

# Code Quality
bun run lint             # Run all linters
bun run lint:oxlint      # Run oxlint
bun run lint:eslint      # Run ESLint
bun run format           # Format code with Prettier

# Preview
bun run preview          # Preview production build
```

## 🔌 Backend Integration

The frontend communicates with the Django GraphQL backend via urql. The client is configured with:

- **Credentials**: `include` (for session cookies)
- **Endpoint**: Configured via `VITE_API_URL`
- **Operations**: Login, Register, Logout, Me query

### GraphQL Operations

#### Login
```graphql
mutation Login($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    success
    message
    user { ... }
  }
}
```

#### Register (Admin Only)
```graphql
mutation Register($input: RegisterInput!) {
  register(input: $input) {
    success
    message
    user { ... }
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
  me { ... }
}
```

## 🚦 Getting Started

1. **Start the backend**: Ensure Django backend is running on port 8000
2. **Install dependencies**: `bun install`
3. **Start frontend**: `bun run dev`
4. **Login**: Navigate to `http://localhost:5173/login`
5. **Default credentials**: Use credentials created in backend

## 🐛 Troubleshooting

### CORS Issues
Ensure Django backend has CORS configured to allow requests from `http://localhost:5173`

### Session Cookies Not Working
- Check `SESSION_COOKIE_SAMESITE` in Django settings
- Verify `credentials: 'include'` in urql client config
- Ensure backend and frontend are on same domain or CORS is properly configured

### GraphQL Errors
- Verify backend is running on correct port
- Check `VITE_API_URL` environment variable
- Inspect network tab for detailed error messages

## 📄 License

This project is part of the Daily Helper system.
