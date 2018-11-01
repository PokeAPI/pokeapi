from graphene import Schema
from graphql_api.auto import schema_operations_builder


AssembledQuery = schema_operations_builder(
    operation_name="Query",
    operation_module="query",
    operation_base="BaseQuery",
    cls_name="Query",
)

schema = Schema(query=AssembledQuery)
