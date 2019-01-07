from django.http import HttpResponseNotAllowed
from django.http.response import HttpResponseBadRequest
from graphene_django.views import HttpError, GraphQLView as GrapheneGraphQLView
from graphql.execution import ExecutionResult

from .cost_analysis_backend import CostAnalysisBackend


class GraphQLView(GrapheneGraphQLView):
    """
    Modify Graphene's default GraphQL view to use CostAnalysisBackend. Required because CostAnalysisBackend needs access to the query variables.
    """

    def execute_graphql_request(
        self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        if not query:
            if show_graphiql:
                return None
            raise HttpError(HttpResponseBadRequest("Must provide query string."))

        try:
            backend = CostAnalysisBackend(variables=variables)
            document = backend.document_from_string(self.schema, query)
        except Exception as e:  # pylint: disable=broad-except
            return ExecutionResult(errors=[e], invalid=True)

        if request.method.lower() == "get":
            operation_type = document.get_operation_type(operation_name)
            if operation_type and operation_type != "query":
                if show_graphiql:
                    return None

                raise HttpError(
                    HttpResponseNotAllowed(
                        ["POST"],
                        "Can only perform a {} operation from a POST request.".format(
                            operation_type
                        ),
                    )
                )

        try:
            extra_options = {}
            if self.executor:
                # We only include it optionally since
                # executor is not a valid argument in all backends
                extra_options["executor"] = self.executor

            return document.execute(
                root=self.get_root_value(request),
                variables=variables,
                operation_name=operation_name,
                context=self.get_context(request),
                middleware=self.get_middleware(request),
                **extra_options
            )
        except Exception as e:  # pylint: disable=broad-except
            return ExecutionResult(errors=[e], invalid=True)
