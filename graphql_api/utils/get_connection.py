from graphql_relay.connection.connectiontypes import Edge
from .get_page import get_page


def get_connection(query_set, connection_type, get_node_fn=None, **kwargs):
    page = get_page(query_set, connection_type.__name__, **kwargs)
    edges = []
    for item in page.items:
        if get_node_fn:
            node = get_node_fn(item)
        else:
            node = item
        edges.append(Edge(node=node, cursor=page.get_cursor(item)))

    return connection_type(
        edges=edges,
        page_info=page.page_info,
        total_count=page.total_count,
    )
