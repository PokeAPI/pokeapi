from base64 import b64decode, b64encode
from graphql import GraphQLError
from graphene.relay.connection import PageInfo
from cursor_pagination import CursorPaginator as CP, InvalidCursor


class CursorPaginator(CP):
    """The standard CursorPaginator encodes cursors as ASCII, which breaks when it encounters non-ASCII strings, such as in names."""

    def decode_cursor(self, cursor):
        try:
            orderings = b64decode(cursor.encode("utf-8")).decode("utf-8")
            return orderings.split(self.delimiter)
        except (TypeError, ValueError):
            raise InvalidCursor(self.invalid_cursor_message)

    def encode_cursor(self, position):
        encoded = b64encode(self.delimiter.join(position).encode("utf-8")).decode(
            "utf-8"
        )
        return encoded


class Page:
    """
    An iterable object that holds page entries and meta data.
    """

    def __init__(self, items, page_info, get_cursor):
        self.items = items
        self.page_info = page_info
        self.get_cursor = get_cursor

    def __getitem__(self, key):
        return self.items.__getitem__(key)

    def __len__(self):
        return len(self.items)


def get_page(
    query_set,
    order_by,
    connection_name,
    first=None,
    last=None,
    after=None,
    before=None,
    **other_kwargs,
):

    if first and last:
        raise GraphQLError(
            f"You must provide either `first` or `last` values (not both) to properly paginate `{connection_name}`."
        )
    if (first and before) or (last and after):
        raise GraphQLError(
            f"You must provide either `first`/`after` or `last`/`before` values to properly paginate `{connection_name}`."
        )
    if not first and not last:
        raise GraphQLError(
            f"You must provide either a `first` or `last` value to properly paginate `{connection_name}`."
        )
    if (first and first < 0) or (last and last < 0):
        raise GraphQLError(
            f"You must provide a positive paging `first`/`last` value to properly paginate `{connection_name}`."
        )

    # # Read the orderBy values from the query_set
    # if query_set.query.order_by:
    #     order_by = list(query_set.query.order_by)
    # elif query_set.query.get_meta().ordering:
    #     order_by = list(query_set.query.get_meta().ordering)
    # else:
    #     order_by = []

    order_by = order_by or []

    # # fmt: off
    # if (
    #     not all(o.order == "desc" for o in order_by) or
    #     not all(o.order == "asc" for o in order_by)
    # ):
    # # fmt: on
    #     raise GraphQLError(
    #         f"All `orderBy` entries must have the same `order` value to properly sort `{connection_name}`."
    #     )

    ordering = []
    for o in order_by:
        if o.order == "asc":
            ordering.append(o.field)
        else:
            ordering.append("-" + o.field)

    # Put `pk` at the end to ensure unique cursors and consistent ordering between queries
    if ordering and ordering[0].startswith("-"):
        ordering.append("-pk")
    else:
        ordering.append("pk")

    # TODO: Catch incorrect cursor-related errors (the cursor structure depends on the
    # orderBy argument, so passing in an invalid cursor will cause an exception).

    paginator = CursorPaginator(query_set, ordering=ordering)
    page = paginator.page(first=first, last=last, after=after, before=before)

    return Page(
        items=page,
        page_info=PageInfo(
            start_cursor=paginator.cursor(page[0]) if page else None,
            end_cursor=paginator.cursor(page[-1]) if page else None,
            has_previous_page=page.has_previous,
            has_next_page=page.has_next,
        ),
        get_cursor=paginator.cursor,
    )
