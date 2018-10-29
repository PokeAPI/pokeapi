from graphql_relay.connection.connectiontypes import Edge as _Edge
from ..loader_key import LoaderKey as _LoaderKey

from .get_page import get_page
from .batch_fetch import batch_fetch


def get_connection(query_set, connection_type, get_node_fn=None, **kwargs):
    page = get_page(query_set, connection_type.__name__, **kwargs)
    edges = []
    for item in page.items:
        if get_node_fn:
            node = get_node_fn(item)
        else:
            node = item
        edges.append(_Edge(node=node, cursor=page.get_cursor(item)))

    return connection_type(
        edges=edges,
        page_info=page.page_info,
        total_count=page.total_count,
    )


def load(loader_name, *, using=None):
    if using is None:
        raise ValueError("'using' is a required argument of the 'resolve' function.")

    def inner(root, info):
        loader = getattr(info.context.loaders, loader_name)
        key = getattr(root, using)
        if key is None:
            return None
        return loader.load(key)

    return inner


def load_with_args(loader_name, *, using=None):
    if using is None:
        raise ValueError(
            "'using' is a required argument of the 'resolve_with_args' function."
        )

    def inner(root, info, **kwargs):
        loader = getattr(info.context.loaders, loader_name)
        key = _LoaderKey(getattr(root, using), **kwargs)
        return loader.load(key)

    return inner
