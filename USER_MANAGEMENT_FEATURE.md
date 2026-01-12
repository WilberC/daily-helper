# User Management Feature - Implementation Summary

## Overview
Added a comprehensive user list and management feature to the User Management section. Admins can now view all users, update their information, and manage permissions for non-admin users.

## Backend Changes

### 1. Updated Types (`backend/users/types.py`)
- Added `UpdateUserInput` - Input type for updating user information
- Added `UpdateUserPayload` - Response payload for update operations

### 2. Updated Schema (`backend/users/schema.py`)
- **New Query: `all_users`**
  - Returns list of all users (excluding superusers)
  - Admin-only access
  - Ordered by date joined (newest first)

- **New Mutation: `update_user`**
  - Updates user information and permissions
  - Admin-only access
  - Security features:
    - Cannot modify superuser accounts
    - Cannot modify admin users' permissions (only their basic info)
    - Email uniqueness validation
    - Prevents privilege escalation

## Frontend Changes

### 1. Updated Types (`frontend/src/types/user.ts`)
- Added `UpdateUserInput` interface
- Added `UpdateUserPayload` interface

### 2. Updated GraphQL Operations (`frontend/src/graphql/auth.graphql.ts`)
- Added `ALL_USERS_QUERY` - Fetches all users
- Added `UPDATE_USER_MUTATION` - Updates user information

### 3. Updated Auth Store (`frontend/src/stores/auth.ts`)
- Added `fetchAllUsers()` method - Fetches all users from the API
- Added `updateUser()` method - Updates a user's information

### 4. New Component: `UserList.vue`
Features:
- **DataTable Display**
  - Shows all users with pagination (5, 10, 20, 50 rows per page)
  - Sortable columns
  - Striped rows for better readability
  - Responsive design

- **User Information Columns**
  - Username (with icon)
  - Email
  - First Name
  - Last Name
  - Role (Admin/Staff badge)
  - Status (Active/Inactive badge)
  - Date Joined
  - Actions (Edit button)

- **Edit Dialog**
  - Edit email, first name, last name
  - Toggle admin access (for non-admin users only)
  - Toggle active status
  - Validation and error handling
  - Cannot edit admin users' permissions

- **Security**
  - Admin users cannot be edited (button disabled)
  - Tooltip explains why admin users can't be edited
  - Permission changes only allowed for non-admin users

### 5. Updated View: `UserManagementView.vue`
- Added new "Manage Users" tab
- Integrated UserList component
- Consistent dark theme styling

## Usage

### For Admins:
1. Navigate to User Management
2. Click on "Manage Users" tab
3. View all users in the system
4. Click edit button (pencil icon) for non-admin users
5. Update user information and permissions
6. Save changes

### Restrictions:
- Only admin users can access the user list
- Admin users' permissions cannot be modified
- Superuser accounts are hidden and cannot be modified
- Email addresses must be unique

## GraphQL Examples

### Query All Users
```graphql
query {
  allUsers {
    id
    username
    email
    firstName
    lastName
    isStaff
    isActive
    dateJoined
  }
}
```

### Update User
```graphql
mutation {
  updateUser(input: {
    userId: "123"
    email: "newemail@example.com"
    firstName: "John"
    lastName: "Doe"
    isStaff: false
    isActive: true
  }) {
    success
    message
    user {
      id
      username
      email
      isStaff
      isActive
    }
  }
}
```

## Design Features
- Dark theme consistent with the rest of the application
- PrimeVue DataTable with full features
- Responsive layout
- Toast notifications for success/error feedback
- Loading states for better UX
- Color-coded badges for roles and status
- Disabled state for protected actions
