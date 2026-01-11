import strawberry
from typing import Optional
from django.contrib.auth import authenticate, login, logout
from asgiref.sync import sync_to_async
from strawberry.types import Info
from .types import UserType, LoginInput, LoginPayload, RegisterInput, RegisterPayload, LogoutPayload
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


@strawberry.type
class Mutation:
    """User authentication mutations."""
    
    @strawberry.mutation
    async def login(self, info: Info, username: str, password: str) -> LoginPayload:
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
        # Wrap synchronous Django auth functions with sync_to_async
        authenticate_sync = sync_to_async(authenticate, thread_sensitive=True)
        login_sync = sync_to_async(login, thread_sensitive=True)
        
        # Helper function to get user by email if username contains @
        @sync_to_async
        def get_username_from_email(email: str) -> Optional[str]:
            try:
                user = User.objects.get(email=email)
                return user.username
            except User.DoesNotExist:
                return None
        
        # If username contains @, treat it as email and get the actual username
        actual_username = username
        if '@' in username:
            actual_username = await get_username_from_email(username)
            if actual_username is None:
                return LoginPayload(
                    success=False,
                    message="Invalid username or password",
                    user=None
                )
        
        # Authenticate the user
        user = await authenticate_sync(info.context.request, username=actual_username, password=password)
        
        if user is not None:
            if user.is_active:
                # Log the user in (creates session)
                await login_sync(info.context.request, user)
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
    async def register(self, info: Info, input: RegisterInput) -> RegisterPayload:
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
        
        # Wrap User.objects.create_user with sync_to_async
        @sync_to_async
        def create_user():
            # Check if username already exists
            if User.objects.filter(username=input.username).exists():
                return None, "Username already exists"
            
            # Check if email already exists
            if input.email and User.objects.filter(email=input.email).exists():
                return None, "Email already exists"
            
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
            return user, None
        
        user, error = await create_user()
        
        if error:
            return RegisterPayload(
                success=False,
                message=error,
                user=None
            )
        
        return RegisterPayload(
            success=True,
            message=f"User '{user.username}' registered successfully",
            user=user
        )

    
    @strawberry.mutation
    async def logout(self, info: Info) -> LogoutPayload:
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
        logout_sync = sync_to_async(logout, thread_sensitive=True)
        
        if info.context.request.user.is_authenticated:
            await logout_sync(info.context.request)
            return LogoutPayload(
                success=True,
                message="Logout successful"
            )
        else:
            return LogoutPayload(
                success=False,
                message="No user is currently logged in"
            )

