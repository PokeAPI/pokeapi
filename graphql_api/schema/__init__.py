from graphene import Schema
from graphql_api.auto import schema_operations_builder


AssembledQuery = schema_operations_builder(
    operation_name="Query",
    operation_module="query",
    operation_base="BaseQuery",
    cls_name="Query",
    __doc__="For an overview of this public GraphQL API for Pokémon data, view the documentation at [pokeapi.co/docs/graphql](https://pokeapi.co/docs/graphql.html).\n\nUse the search box above to search for a specific object type, or scroll through the list below."
)

schema = Schema(query=AssembledQuery)
