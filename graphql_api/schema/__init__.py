from graphene import Schema
from graphql_api.auto import schema_operations_builder


AssembledQuery = schema_operations_builder(
    operation_name="Query",
    operation_module="query",
    operation_base="BaseQuery",
    cls_name="Query",
    __doc__="This API is currently in ALPHA status and may change without notice.\n\nFor an overview of this public GraphQL API for Pokémon data, view the documentation at [pokeapi.co/docs/graphql](https://pokeapi.co/docs/graphql.html). If you would like to contribute to this open source project, the source code is available at [github.com/cmmartti/pokeapi/tree/graphql](https://github.com/cmmartti/pokeapi/tree/graphql).\n\nUse the search box above to search for a specific object type, or scroll through the list below.\n\nSeveral key object types like Move and Item have not yet been completed due to their complexity and time constraints, but rest assured they're in the pipeline."
)

schema = Schema(query=AssembledQuery)
