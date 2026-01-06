import strawberry_django
from . import models

@strawberry_django.type(models.Category, fields='__all__')
class Category:
    pass