from graphene import Schema
from .auto import schema_operations_builder

ALL_QUERIES = schema_operations_builder(
    operationName="Query",
    operationModule="query",
    operationBase="BaseQuery",
    clsName="Query",
)

schema = Schema(query=ALL_QUERIES)
