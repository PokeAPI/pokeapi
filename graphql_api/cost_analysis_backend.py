from graphql.backend.core import GraphQLCoreBackend
from graphql.language.ast import (
    FragmentDefinition,
    OperationDefinition,
    VariableDefinition,
    FragmentSpread,
)


COMPLEXITY_LIMIT = 1000
SKIP = [
    "edges",
    "node",
    "pageInfo",
    "hasNextPage",
    "hasPreviousPage",
    "startCursor",
    "endCursor",
    "cursor",
]


def measure_cost(selection_set, fragments, variables):
    cost = 0
    for field in selection_set.selections:
        if isinstance(field, FragmentSpread):
            cost += measure_cost(
                fragments[field.name.value].selection_set, fragments, variables
            )
        else:
            if field.name.value not in SKIP:
                cost += 1
            if field.selection_set:
                for arg in field.arguments:
                    # Nested connections can't be batch-loaded from the database,
                    # so make them expensive to use
                    if arg.name.value in ["first", "last"]:

                        # Check if the arg value is a variable, if necessary
                        value = None
                        if isinstance(arg.value, VariableDefinition):
                            if arg.name.value in variables:
                                value = variables[arg.name.value]
                        else:
                            value = arg.value.value

                        # The multiplier is the page size of the connection, or 10.
                        # It multiplies the cost of the connection's contents.
                        multiplier = max(10, int(value))
                        cost += multiplier * measure_cost(
                            field.selection_set, fragments, variables
                        )
                        break
                else:
                    cost += measure_cost(field.selection_set, fragments, variables)
    return cost


class CostAnalysisBackend(GraphQLCoreBackend):
    def __init__(self, variables, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables = variables

    def document_from_string(self, schema, document_string):
        document = super().document_from_string(schema, document_string)
        ast = document.document_ast

        query = None
        fragments = {}
        for definition in ast.definitions:
            if isinstance(definition, FragmentDefinition):
                fragments[definition.name.value] = definition
            if (
                isinstance(definition, OperationDefinition)
                and definition.operation == "query"
            ):
                query = definition

        if query:
            cost = int(measure_cost(query.selection_set, fragments, self.variables))
            if cost > COMPLEXITY_LIMIT:
                raise Exception(
                    f"Query with complexity of {cost} exceeds complexity limit of {COMPLEXITY_LIMIT}."
                )

        return document



# Document(
#     definitions=[
#         OperationDefinition(
#             operation="query",
#             name=None,
#             variable_definitions=[],
#             directives=[],
#             selection_set=SelectionSet(
#                 selections=[
#                     Field(
#                         alias=None,
#                         name=Name(value="languages"),
#                         arguments=[],
#                         directives=[],
#                         selection_set=SelectionSet(
#                             selections=[
#                                 FragmentSpread(name=Name(value="fields"), directives=[])
#                             ]
#                         ),
#                     )
#                 ]
#             ),
#         ),
#         FragmentDefinition(
#             name=Name(value="fields"),
#             type_condition=NamedType(name=Name(value="Language")),
#             directives=[],
#             selection_set=SelectionSet(
#                 selections=[
#                     Field(
#                         alias=None,
#                         name=Name(value="name"),
#                         arguments=[],
#                         directives=[],
#                         selection_set=None,
#                     ),
#                     Field(
#                         alias=None,
#                         name=Name(value="isOfficial"),
#                         arguments=[],
#                         directives=[],
#                         selection_set=None,
#                     ),
#                 ]
#             ),
#         ),
#     ]
# )
