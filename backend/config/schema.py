import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from products.schema import Query as ProductsQuery
from comparator.schema import Query as ComparatorQuery

@strawberry.type
class Query(ProductsQuery, ComparatorQuery):
    pass

schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)