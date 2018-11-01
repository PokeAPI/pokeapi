import graphene as g
from graphql import GraphQLError


class BaseQuery(g.ObjectType):
    pass


class BaseConnection:
    total_count = g.Int(
        description='A count of the total number of objects in this connection, ignoring pagination. This allows a client to fetch the first five objects by passing "5" as the argument to "first", then fetch the total count so it could display "5 of 83", for example.'
    )


class URI(g.String):
    """An RFC 3986, RFC 3987, and RFC 6570 (level 4) compliant URI string."""

    pass


class BaseWhere(g.InputObjectType):
    @classmethod
    def apply(cls, query_set, **where):
        """Iteratively apply each where clause to query_set."""
        for arg, value in where.items():
            query_set = query_set.filter(**{arg: value})

        return query_set.distinct()

    @classmethod
    def text_filter(cls, query_set, arg, resource_name, field_name):
        filters = {}
        if arg.case_sensitive:
            filters[f"{resource_name}__{field_name}__contains"] = arg.query
        else:
            filters[f"{resource_name}__{field_name}__icontains"] = arg.query
        if arg.lang:
            filters[f"{resource_name}__language__name"] = arg.lang

        return query_set.filter(**filters)


class TextSearch(g.InputObjectType):
    query = g.String(description="The text to search for.", required=True)
    case_sensitive = g.Boolean(default_value=False)
    lang = g.Field(
        g.lazy_import("graphql_api.schema.language_enum.LanguageEnum"),
        description="Restrict search results to a specific language. By default, searches will be performed against all languages.",
    )
    # exact = Boolean(
    #     default_value=False,
    #     description="Return only exact, case-sensitive matches."
    # )


class SortDirection(g.Enum):
    ASC = "asc"
    DESC = "desc"

    @property
    def description(self):
        if self == SortDirection.ASC:
            return "Ascending order"
        if self == SortDirection.DESC:
            return "Descending order"


class BaseSort(g.InputObjectType):
    direction = SortDirection(
        description="The sort direction.", default_value=SortDirection.ASC
    )
    lang = g.Field(
        g.lazy_import("graphql_api.schema.language_enum.LanguageEnum"),
        description="For sorts with text translations (such as `NAME`), you **must** specify the language by which to sort. This argument will be ignored for non translated sorts.",
    )

    @classmethod
    def apply(cls, query_set, order_by):
        order_by = order_by or []
        ordering = []
        for o in order_by:
            if o.direction == "asc":
                ordering.append(o.field)
            else:
                ordering.append("-" + o.field)

        return query_set.order_by(*ordering)

    @staticmethod
    def check_lang(order_by_entry):
        if "lang" not in order_by_entry:
            raise GraphQLError(
                "Argument `lang` **must** be specified for sorts with text translations."
            )


class TranslationList(g.List):
    def __init__(self, of_type, *args, **kwargs):
        kwargs.setdefault(
            "lang",
            g.List(
                g.lazy_import("graphql_api.schema.language_enum.LanguageEnum"),
                description="Restrict results to specific languages, in the order specified. This allows a client to specify a primary language with one or more fall-back languages to be used when the primary language is not available.",
            ),
        )
        super().__init__(of_type, *args, **kwargs)


class BaseTranslation(g.ObjectType):
    language_id = None
    language = g.Field(
        g.lazy_import("graphql_api.schema.language.types.Language"),
        description="The language this name is in.",
    )

    def resolve_language(self, info):
        return info.context.loaders.language.load(self.language_id)
