import strawberry
import strawberry_django
from .types import Category

@strawberry.type
class Query:
    categories: list[Category] = strawberry_django.field()
