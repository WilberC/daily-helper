# Daily Helper - Frontend 🎨

A modern Vue 3 frontend application for the Daily Helper system, featuring user authentication and management with a sleek dark mode interface. Built with best practices in mind, following established workflow guidelines for maintainability and scalability.

## 🚀 Tech Stack

- **Framework**: Vue 3 with `<script setup>` Composition API and TypeScript
- **UI Library**: PrimeVue 4.x (Aura preset)
- **Styling**: Tailwind CSS with custom dark mode theme
- **State Management**: Pinia
- **GraphQL Client**: urql
- **Form Validation**: vee-validate + yup
- **Routing**: Vue Router 4
- **Build Tool**: Vite 7
- **Package Manager**: Bun
- **Testing**: Vitest (unit) + Playwright (e2e)
- **Code Quality**: ESLint + oxlint + Prettier

## ✨ Features

- 🔐 **Authentication System**: Secure login/logout with session-based authentication
- 👥 **User Management**: Admin interface for creating staff and admin users
- 🌙 **Dark Mode**: Exclusive dark theme with custom color palette
- 📱 **Responsive Design**: Fully responsive across mobile, tablet, and desktop
- 🎨 **Modern UI**: Built with PrimeVue components and custom styling
- 🔒 **Route Guards**: Protected routes based on authentication and role
- ✅ **Form Validation**: Client-side validation with helpful error messages
- ♿ **Accessibility**: WCAG 2.1 AA compliant with ARIA labels and keyboard navigation
- 🧩 **Composables**: Reusable logic with Vue 3 composables pattern

## 📋 Prerequisites

- **Node.js**: ^20.19.0 || >=22.12.0
- **Bun**: Latest version (recommended) or npm
- **Backend API**: Django GraphQL backend running on `http://localhost:8000`

## 🛠️ Setup Instructions

### 1. Install Dependencies

Using Bun (recommended):

```bash
bun install
```

Using npm:

```bash
npm install
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
frontend/
├── .agent/
│   └── workflows/         # Development workflows and guidelines
│       ├── accessibility-guidelines.md
│       ├── async-sync-best-practices.md
│       ├── code-principles.md
│       ├── component-best-practices.md
│       ├── styling-guidelines.md
│       └── ui-ux-principles.md
├── src/
│   ├── __tests__/         # Unit tests
│   ├── assets/
│   │   └── styles/
│   │       └── main.css   # Global styles, Tailwind config, design tokens
│   ├── components/        # Reusable components
│   │   └── users/
│   │       ├── CreateUserForm.vue
│   │       ├── ErrorText.vue
│   │       └── UserList.vue
│   ├── composables/       # Reusable composition functions
│   │   └── useFormatters.ts
│   ├── config/
│   │   └── api.ts         # GraphQL client (urql) configuration
│   ├── graphql/
│   │   └── auth.graphql.ts # Authentication GraphQL operations
│   ├── router/
│   │   └── index.ts       # Vue Router with authentication guards
│   ├── stores/
│   │   └── auth.ts        # Pinia authentication store
│   ├── types/
│   │   └── user.ts        # TypeScript type definitions
│   ├── views/             # Page-level components
│   │   ├── LoginView.vue
│   │   ├── DashboardView.vue
│   │   └── UserManagementView.vue
│   ├── App.vue            # Root component
│   └── main.ts            # Application entry point
├── e2e/                   # End-to-end tests (Playwright)
├── public/                # Static assets
├── .eslintrc.ts           # ESLint configuration
├── .oxlintrc.json         # oxlint configuration
├── .prettierrc.json       # Prettier configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── vite.config.ts         # Vite configuration
```

## 🎨 Architecture & Best Practices

This project follows established workflow guidelines for consistency and maintainability. Key principles:

### Code Organization

- **Component Structure**: Feature-based organization in subdirectories
- **Composition API**: Use `<script setup>` with TypeScript
- **Composables**: Extract reusable logic into composables
- **Type Safety**: Strong TypeScript typing throughout

### Styling

- **Tailwind CSS**: Utility-first approach with custom theme
- **Color Tokens**: Semantic color system for consistency
- **Dark Mode**: Custom dark theme with `dark-*` classes
- **Component Styles**: Scoped styles for component-specific needs

### Accessibility

- **ARIA Labels**: Descriptive labels for all interactive elements
- **Keyboard Navigation**: Full keyboard support
- **Form Validation**: Clear error messages and validation states
- **Semantic HTML**: Proper use of HTML5 semantic elements

> **Note**: For detailed guidelines, see the workflow files in `.agent/workflows/`:
>
> - `/code-principles` - Frontend architecture and code organization
> - `/component-best-practices` - Component development patterns
> - `/styling-guidelines` - Tailwind CSS and theming
> - `/accessibility-guidelines` - A11y best practices
> - `/ui-ux-principles` - UI/UX design patterns

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

## 🎨 Styling System

The application uses a custom dark theme with Tailwind CSS:

### Color Palette

```css
/* Primary Colors */
--color-primary-50: hsl(220, 70%, 95%);
--color-primary-500: hsl(220, 90%, 56%); /* Main brand color */
--color-primary-600: hsl(220, 85%, 50%);

/* Danger Colors */
--color-danger-50: hsl(0, 86%, 97%);
--color-danger-500: hsl(0, 84%, 60%); /* Error states */
--color-danger-600: hsl(0, 72%, 51%);

/* Dark Theme */
--color-dark-bg: #0f172a; /* Main background */
--color-dark-surface: #1e293b; /* Cards, panels */
--color-dark-border: #334155; /* Borders */
--color-dark-text: #f1f5f9; /* Primary text */
--color-dark-text-secondary: #94a3b8; /* Secondary text */
```

### PrimeVue Theme

- **Preset**: Aura
- **Mode**: Dark mode only (`.dark` class)
- **Customization**: Theme tokens in `main.css`

## 📝 Available Scripts

```bash
# Development
bun run dev              # Start dev server with hot reload

# Build
bun run build            # Type-check and build for production
bun run build-only       # Build without type-checking
bun run preview          # Preview production build

# Testing
bun run test:unit        # Run unit tests (Vitest)
bun run test:e2e         # Run end-to-end tests (Playwright)

# Code Quality
bun run lint             # Run all linters (oxlint + ESLint)
bun run lint:oxlint      # Run oxlint (faster linter)
bun run lint:eslint      # Run ESLint
bun run format           # Format code with Prettier

# Type Checking
bun run type-check       # TypeScript type checking
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
      firstName
      lastName
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

## 🚦 Getting Started

1. **Start the backend**: Ensure Django backend is running on port 8000
2. **Install dependencies**: `bun install`
3. **Start frontend**: `bun run dev`
4. **Login**: Navigate to `http://localhost:5173/login`
5. **Default credentials**: Use credentials created in backend via seeding or admin

## 🧩 Adding New Features

The architecture supports easy feature additions:

1. **Create a new view** in `src/views/` for page-level components
2. **Add components** in `src/components/` organized by feature
3. **Define types** in `src/types/` for TypeScript support
4. **Create GraphQL operations** in `src/graphql/`
5. **Add routes** in `src/router/index.ts`
6. **Create stores** in `src/stores/` for state management (if needed)
7. **Extract reusable logic** into composables in `src/composables/`

Follow the workflow guidelines in `.agent/workflows/` for best practices.

## 🐛 Troubleshooting

### CORS Issues

Ensure Django backend has CORS configured to allow requests from `http://localhost:5173`

- Check `CORS_ALLOWED_ORIGINS` in backend `.env`
- Verify `django-cors-headers` is installed on backend

### Session Cookies Not Working

- Check `SESSION_COOKIE_SAMESITE` in Django settings
- Verify `credentials: 'include'` in urql client config (`src/config/api.ts`)
- Ensure backend and frontend are on same domain or CORS is properly configured

### GraphQL Errors

- Verify backend is running on correct port (default: 8000)
- Check `VITE_API_URL` environment variable
- Inspect network tab in browser DevTools for detailed error messages
- Check GraphQL Playground at `http://localhost:8000/graphql/`

### Type Errors

- Run `bun run type-check` to see all TypeScript errors
- Ensure all GraphQL operations have corresponding TypeScript types
- Check for missing imports or incorrect type definitions

### Styling Issues

- Verify Tailwind is processing correctly: `bun run build`
- Check that `main.css` is imported in `main.ts`
- Ensure PrimeVue theme is configured in `main.ts`
- Verify dark mode classes are applied (`.dark` on `<html>` element)

## 📚 Additional Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [PrimeVue Components](https://primevue.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pinia State Management](https://pinia.vuejs.org/)
- [urql GraphQL Client](https://formidable.com/open-source/urql/)
- [Vee-Validate](https://vee-validate.logaretm.com/v4/)

## 📄 License

This project is part of the Daily Helper system.
