import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from products.schema import Query as ProductsQuery
from comparator.schema import Query as ComparatorQuery
from users.schema import Query as UsersQuery, Mutation as UsersMutation

@strawberry.type
class Query(ProductsQuery, ComparatorQuery, UsersQuery):
    pass

@strawberry.type
class Mutation(UsersMutation):
    pass

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)