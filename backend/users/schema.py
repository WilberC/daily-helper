import strawberry
from typing import Optional
from django.contrib.auth import authenticate, login, logout
from strawberry.types import Info
from .types import UserType, LoginInput, LoginPayload, RegisterInput, RegisterPayload, LogoutPayload, UpdateUserInput, UpdateUserPayload
from .models import User


@strawberry.type
class Query:
    """User-related GraphQL queries."""
    
    @strawberry.field
    def me(self, info: Info) -> Optional[UserType]:
        """
        Returns the currently authenticated user, or None if not authenticated.
        
        Example:
            query {
                me {
                    id
                    username
                    email
                }
            }
        """
        user = info.context.request.user
        if user.is_authenticated:
            return user
        return None
    
    @strawberry.field
    def all_users(self, info: Info) -> list[UserType]:
        """
        Returns all users in the system. ADMIN-ONLY.
        
        Returns:
            List of all users (excluding superusers for safety)
        
        Example:
            query {
                allUsers {
                    id
                    username
                    email
                    firstName
                    lastName
                    isStaff
                    isActive
                }
            }
        """
        # Check if user is authenticated and is an admin
        user = info.context.request.user
        if not (user.is_authenticated and user.is_staff):
            return []
        
        # Get all users except superusers (for safety)
        return list(User.objects.filter(is_superuser=False).order_by('-date_joined'))


@strawberry.type
class Mutation:
    """User authentication mutations."""
    
    @strawberry.mutation
    def login(self, info: Info, username: str, password: str) -> LoginPayload:
        """
        Authenticates a user and creates a session.
        
        Args:
            username: The username or email
            password: The user's password
        
        Returns:
            LoginPayload with success status, message, and user data if successful
        
        Example:
            mutation {
                login(username: "testuser", password: "password123") {
                    success
                    message
                    user {
                        id
                        username
                        email
                    }
                }
            }
        """
        # If username contains @, treat it as email and get the actual username
        actual_username = username
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                actual_username = user_obj.username
            except User.DoesNotExist:
                return LoginPayload(
                    success=False,
                    message="Invalid username or password",
                    user=None
                )
        
        # Authenticate the user
        user = authenticate(info.context.request, username=actual_username, password=password)
        
        if user is not None:
            if user.is_active:
                # Log the user in (creates session)
                login(info.context.request, user)
                return LoginPayload(
                    success=True,
                    message="Login successful",
                    user=user
                )
            else:
                return LoginPayload(
                    success=False,
                    message="This account has been disabled",
                    user=None
                )
        else:
            return LoginPayload(
                success=False,
                message="Invalid username or password",
                user=None
            )
    
    @strawberry.mutation
    def register(self, info: Info, input: RegisterInput) -> RegisterPayload:
        """
        Registers a new user. ADMIN-ONLY: Only authenticated admin users can create new users.
        
        Args:
            input: RegisterInput containing user details
        
        Returns:
            RegisterPayload with success status, message, and user data if successful
        
        Example:
            mutation {
                register(input: {
                    username: "newuser"
                    email: "newuser@example.com"
                    password: "securepass123"
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
                    }
                }
            }
        """
        # Check if user is authenticated and is an admin
        current_user = info.context.request.user
        if not current_user.is_authenticated:
            return RegisterPayload(
                success=False,
                message="Authentication required. You must be logged in as an admin to register users.",
                user=None
            )
        
        if not current_user.is_staff:
            return RegisterPayload(
                success=False,
                message="Permission denied. Only admin users can register new users.",
                user=None
            )
        
        # Check if username already exists
        if User.objects.filter(username=input.username).exists():
            return RegisterPayload(
                success=False,
                message="Username already exists",
                user=None
            )
        
        # Check if email already exists
        if input.email and User.objects.filter(email=input.email).exists():
            return RegisterPayload(
                success=False,
                message="Email already exists",
                user=None
            )
        
        # Create the user
        user = User.objects.create_user(
            username=input.username,
            email=input.email,
            password=input.password,
            first_name=input.first_name or "",
            last_name=input.last_name or "",
            is_staff=input.is_staff or False,
            is_active=input.is_active if input.is_active is not None else True
        )
        
        return RegisterPayload(
            success=True,
            message=f"User '{user.username}' registered successfully",
            user=user
        )
    
    @strawberry.mutation
    def update_user(self, info: Info, input: UpdateUserInput) -> UpdateUserPayload:
        """
        Updates user information and permissions. ADMIN-ONLY.
        Admins cannot modify other admin users' permissions.
        
        Args:
            input: UpdateUserInput containing user ID and fields to update
        
        Returns:
            UpdateUserPayload with success status, message, and updated user data
        
        Example:
            mutation {
                updateUser(input: {
                    userId: "123"
                    email: "newemail@example.com"
                    isActive: false
                }) {
                    success
                    message
                    user {
                        id
                        username
                        email
                        isActive
                    }
                }
            }
        """
        # Check if user is authenticated and is an admin
        current_user = info.context.request.user
        if not current_user.is_authenticated:
            return UpdateUserPayload(
                success=False,
                message="Authentication required. You must be logged in as an admin to update users.",
                user=None
            )
        
        if not current_user.is_staff:
            return UpdateUserPayload(
                success=False,
                message="Permission denied. Only admin users can update users.",
                user=None
            )
        
        try:
            # Get the user to update
            user = User.objects.get(id=input.user_id)
            
            # Prevent modifying admin users (except for non-permission fields)
            if user.is_staff and str(user.id) != str(current_user.id):
                # Allow updating email, first_name, last_name but not permissions
                if input.is_staff is not None or input.is_active is not None:
                    return UpdateUserPayload(
                        success=False,
                        message="Cannot modify permissions of admin users.",
                        user=None
                    )
            
            # Prevent modifying superusers
            if user.is_superuser:
                return UpdateUserPayload(
                    success=False,
                    message="Cannot modify superuser accounts.",
                    user=None
                )
            
            # Update fields if provided
            if input.email is not None:
                # Check if email already exists for another user
                if User.objects.filter(email=input.email).exclude(id=user.id).exists():
                    return UpdateUserPayload(
                        success=False,
                        message="Email already exists for another user.",
                        user=None
                    )
                user.email = input.email
            
            if input.first_name is not None:
                user.first_name = input.first_name
            
            if input.last_name is not None:
                user.last_name = input.last_name
            
            # Only update permissions if target user is not an admin
            if not user.is_staff:
                if input.is_staff is not None:
                    user.is_staff = input.is_staff
                
                if input.is_active is not None:
                    user.is_active = input.is_active
            
            user.save()
            
            return UpdateUserPayload(
                success=True,
                message=f"User '{user.username}' updated successfully",
                user=user
            )
        except User.DoesNotExist:
            return UpdateUserPayload(
                success=False,
                message="User not found.",
                user=None
            )
        except Exception as e:
            return UpdateUserPayload(
                success=False,
                message=f"Error updating user: {str(e)}",
                user=None
            )

    
    @strawberry.mutation
    def logout(self, info: Info) -> LogoutPayload:
        """
        Logs out the current user and destroys the session.
        
        Returns:
            LogoutPayload with success status and message
        
        Example:
            mutation {
                logout {
                    success
                    message
                }
            }
        """
        if info.context.request.user.is_authenticated:
            logout(info.context.request)
            return LogoutPayload(
                success=True,
                message="Logout successful"
            )
        else:
            return LogoutPayload(
                success=False,
                message="No user is currently logged in"
            )

