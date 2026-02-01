export const en = {
  common: {
    welcome: 'Welcome',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    create: 'Create',
    search: 'Search',
    filter: 'Filter',
    loading: 'Loading...',
    noData: 'No data available',
    error: 'An error occurred',
    success: 'Success',
    confirm: 'Confirm',
    back: 'Back',
    next: 'Next',
    previous: 'Previous',
    close: 'Close',
    greeting: 'Hello, {name}!',
  },

  login: {
    title: 'Daily Helper',
    subtitle: 'Sign in to your account',
    username: 'Username',
    password: 'Password',
    signIn: 'Sign In',
    enterUsername: 'Enter your username',
    enterPassword: 'Enter your password',
    adminRequired: 'Admin access required for user management',
    loginSuccess: 'Login successful',
    loginError: 'Invalid credentials',
  },

  dashboard: {
    title: 'Dashboard',
    welcome: 'Welcome, {name}!',
    overview: 'Overview',
    quickActions: 'Quick Actions',
    stats: {
      total: 'Total',
      active: 'Active',
      inactive: 'Inactive',
    },
  },

  users: {
    management: 'User Management',
    list: 'User List',
    allUsers: 'All Users',
    createAdmin: 'Create Admin',
    createStaff: 'Create Staff',
    createNormal: 'Create Normal User',

    types: {
      admin: 'Admin',
      staff: 'Staff',
      normal: 'Normal',
    },

    form: {
      username: 'Username',
      email: 'Email',
      password: 'Password',
      firstName: 'First Name',
      lastName: 'Last Name',
      isActive: 'Active Account',

      enterUsername: 'Enter username',
      enterEmail: 'Enter email',
      enterPassword: 'Enter password',
      enterFirstName: 'Enter first name',
      enterLastName: 'Enter last name',

      create: 'Create {type} User',
      createSuccess: 'User created successfully',
      createError: 'Failed to create user',

      updateSuccess: 'User updated successfully',
      updateError: 'Failed to update user',

      deleteSuccess: 'User deleted successfully',
      deleteError: 'Failed to delete user',
    },

    table: {
      username: 'Username',
      email: 'Email',
      firstName: 'First Name',
      lastName: 'Last Name',
      role: 'Role',
      status: 'Status',
      actions: 'Actions',
      createdAt: 'Created At',
      lastLogin: 'Last Login',
      joined: 'Joined',
    },

    info: {
      adminAccount: 'Administrator Account',
      adminDescription:
        'This user will have full access to all features including user management.',
      staffAccount: 'Staff Account',
      staffDescription:
        'This user will have elevated privileges but no user management capabilities.',
      normalAccount: 'Normal User Account',
      normalDescription: 'This user will have standard access without administrative capabilities.',
    },

    actions: {
      edit: 'Edit User',
      delete: 'Delete User',
      activate: 'Activate',
      deactivate: 'Deactivate',
      resetPassword: 'Reset Password',
      refresh: 'Refresh',
      cannotEditAdmin: 'Cannot edit admin users',
      editUser: 'Edit user {username}',
    },

    modal: {
      editTitle: 'Edit User: {username}',
      permissions: 'Permissions',
      adminAccess: 'Admin Access',
      activeAccount: 'Active Account',
      adminWarning: "⚠️ Admin users' permissions cannot be modified",
      cancel: 'Cancel',
      saveChanges: 'Save Changes',
    },
  },

  validation: {
    required: '{field} is required',
    minLength: '{field} must be at least {min} characters',
    maxLength: '{field} must not exceed {max} characters',
    email: {
      invalid: 'Must be a valid email',
      required: 'Email is required',
    },
    password: {
      required: 'Password is required',
      minLength: 'Password must be at least {min} characters',
      weak: 'Password is too weak',
    },
    username: {
      required: 'Username is required',
      minLength: 'Username must be at least {min} characters',
      invalid: 'Username contains invalid characters',
    },
  },

  nav: {
    home: 'Home',
    dashboard: 'Dashboard',
    users: 'Users',
    settings: 'Settings',
    logout: 'Logout',
    profile: 'Profile',
  },
}
