from graphene import Schema
from .auto import schema_operations_builder

ALL_QUERIES = schema_operations_builder(
    operation_name="Query",
    operation_module="query",
    operation_base="BaseQuery",
    cls_name="Query",
)

schema = Schema(query=ALL_QUERIES)
