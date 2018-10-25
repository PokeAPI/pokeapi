from base64 import b64decode, b64encode
from graphql import GraphQLError
from graphene.relay.connection import PageInfo
from cursor_pagination import CursorPaginator as CP, InvalidCursor


class CursorPaginator(CP):
    """The standard CursorPaginator encoded cursors as ASCII, which breaks when it encounters non-ASCII strings, such as in names."""

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
    An iterable object that holds page entries, as well as other page-related data.
    """

    def __init__(self, items, page_info, get_cursor, total_count=None):
        self.items = items
        self.page_info = page_info
        self.get_cursor = get_cursor
        self.total_count = total_count

    def __getitem__(self, key):
        return self.items.__getitem__(key)

    def __len__(self):
        return len(self.items)


def get_page(
    query_set,
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
    if (first and first < 0) or (last and last < 0):
        raise GraphQLError(
            f"You must provide a positive paging `limit` value to properly paginate `{connection_name}`."
        )
    if not first and not last:
        raise GraphQLError(
            f"You must provide a `first` or `last` value to properly paginate `{connection_name}`."
        )

    if query_set.query.order_by:
        order_by = list(query_set.query.order_by)
    elif query_set.query.get_meta().ordering:
        order_by = list(query_set.query.get_meta().ordering)
    else:
        order_by = []

    # fmt: off
    if (
        not all(o.startswith("-") for o in order_by) and
        not all(not o.startswith("-") for o in order_by)
    ):
    # fmt: on
        raise GraphQLError(
            f"All `orderBy` entries must have the same `direction` value to properly sort `{connection_name}`."
        )

    # Layer the orderBy, with `pk` always at the bottom to ensure unique cursors and consistent ordering between queries
    if order_by and order_by[0].startswith("-"):
        order_by.append("-pk")
    else:
        order_by.append("pk")

    # TODO: Catch incorrect cursor-related errors (the cursor structure depends on the
    # orderBy argument, so passing in an invalid cursor will cause an exception).

    # Total number of entries in the query set _before_ pagination.
    total_count = query_set.count()

    paginator = CursorPaginator(query_set, ordering=order_by)
    page = paginator.page(first=first, last=last, after=after, before=before)

    return Page(
        items=page,
        page_info=PageInfo(
            start_cursor=paginator.cursor(page[0]) if page else None,
            end_cursor=paginator.cursor(page[-1]) if page else None,
            has_previous_page=page.has_previous,
            has_next_page=page.has_next,
        ),
        total_count=total_count,
        get_cursor=paginator.cursor,
    )
