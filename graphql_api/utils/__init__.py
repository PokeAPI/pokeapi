from graphql_relay.connection.connectiontypes import Edge as _Edge
from ..loader_key import LoaderKey as _LoaderKey

from .get_page import get_page
from .batch_fetch import batch_fetch
from .text_annotate import text_annotate


def get_connection(query_set, order_by, connection_type, get_node_fn=None, **kwargs):
    total_count = query_set.count()
    page = get_page(query_set, order_by, connection_type.__name__, **kwargs)
    edges = []
    for item in page.items:
        if get_node_fn:
            node = get_node_fn(item)
        else:
            node = item
        edges.append(_Edge(node=node, cursor=page.get_cursor(item)))

    return connection_type(
        edges=edges, page_info=page.page_info, total_count=total_count
    )


def load(loader_name, *, using=None):
    if using is None:
        raise ValueError("'using' is a required argument of the 'load' function.")

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
            "'using' is a required argument of the 'load_with_args' function."
        )

    def inner(root, info, **kwargs):
        loader = getattr(info.context.loaders, loader_name)
        key = _LoaderKey(getattr(root, using), **kwargs)
        return loader.load(key)

    return inner


def group(iterable, group_by):
    groups = {}
    for item in iterable:
        if getattr(item, group_by) not in groups:
            groups[getattr(item, group_by)] = []
        groups[getattr(item, group_by)].append(item)
    return groups


def add_prefix(options, name_prefix, value_prefix):
    return [
        (name_prefix + "__" + name, value_prefix + "__" + value)
        for name, value in options
    ]
