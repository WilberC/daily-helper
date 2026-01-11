import strawberry
import strawberry_django
from typing import Optional
from .models import User


@strawberry_django.type(User)
class UserType:
    """GraphQL type for User model. Excludes sensitive fields like password."""
    id: strawberry.ID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    date_joined: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.input
class LoginInput:
    """Input type for login mutation."""
    username: str
    password: str


@strawberry.type
class LoginPayload:
    """Response payload for login mutation."""
    success: bool
    message: str
    user: Optional[UserType] = None


@strawberry.input
class RegisterInput:
    """Input type for user registration (admin-only)."""
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True


@strawberry.type
class RegisterPayload:
    """Response payload for register mutation."""
    success: bool
    message: str
    user: Optional[UserType] = None


@strawberry.type
class LogoutPayload:
    """Response payload for logout mutation."""
    success: bool
    message: str

