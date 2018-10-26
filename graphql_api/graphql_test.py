import collections
from django.test import TestCase
from graphene import Context
from graphene.test import Client
from .schema import schema
from .middleware import LoaderMiddleware


def to_plain_dict(ordered_dict):
    """Recursively convert an OrderedDict to a regular dictionary."""

    plain_dict = {}
    for key, value in ordered_dict.items():
        if isinstance(value, collections.OrderedDict):
            plain_dict[key] = to_plain_dict(value)
        elif isinstance(value, list):
            simple_list = []
            for item in value:
                if isinstance(item, collections.OrderedDict):
                    simple_list.append(to_plain_dict(item))
                else:
                    simple_list.append(item)
            plain_dict[key] = simple_list
        else:
            plain_dict[key] = value
    return plain_dict


class GraphQLTest(TestCase):
    """Base class for testing GraphQL queries."""

    maxDiff = None

    def execute_query(self, query):
        client = Client(schema)
        result = client.execute(
            query, middleware=[LoaderMiddleware()], context_value=Context()
        )

        # OrderedDicts screw up the error diffs, so convert to a normal dictionary
        return to_plain_dict(result)
