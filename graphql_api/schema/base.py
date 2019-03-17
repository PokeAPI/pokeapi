import re
from typing import List
import graphene as g
from django.db.models import Count
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
    def apply(cls, query_set, prefix="", **where):
        """Iteratively apply each where clause to query_set."""

        for arg, value in where.items():
            if value is not None:
                if isinstance(value, BaseWhere):
                    query_set = value.apply(query_set, prefix=prefix + arg, **value)
                elif isinstance(value, List):
                    value = [v for v in value if v is not None]
                    if value:
                        query_set = query_set.filter(**{prefix + arg + "__in": value})
                else:
                    query_set = query_set.filter(**{prefix + arg: value})

        return query_set.distinct()


class IntFilter(BaseWhere):
    exact = g.Int(name="eq", description="Exactly equal to.")
    lt = g.Int(description="Less than.")
    lte = g.Int(description="Less than or equal to.")
    gt = g.Int(description="Greater than.")
    gte = g.Int(description="Greater than or equal to.")

    @classmethod
    def apply(cls, query_set, prefix="", **where):
        filters = {
            f"{prefix}__{operator}": value
            for operator, value in where.items()
            if value is not None
        }
        return query_set.filter(**filters)


class ListFilter(BaseWhere):
    eq = g.List(g.ID, description="Exactly equal to.")
    all = g.List(g.ID, description="Contains all of.")
    some = g.List(g.ID, description="Contains some of (at least one).")

    @classmethod
    def apply(cls, query_set, prefix="", **where):
        for operator, value in where.items():
            if value is not None:
                value = [v for v in value if v is not None]  # filter out null values
                if value:
                    if operator == "eq":
                        query_set = query_set.annotate(
                            **{prefix + "__count": Count(prefix)}
                        )
                        query_set = query_set.filter(**{prefix + "__count": len(value)})

                    if operator in ["eq", "all"]:
                        for v in value:
                            query_set = query_set.filter(**{prefix + "__exact": v})
                    elif operator == "some":
                        query_set = query_set.filter(**{prefix + "__in": value})

        return query_set


class TextFilter(BaseWhere):
    sw = g.String(description="Starts with.")
    has = g.String(description="Has/Contains.")
    eq = g.String(description="Exactly equals to.")
    ne = g.String(description="Not equals to.")
    regex = g.String()
    in_ = g.List(g.String, name="in", description="In.")
    nin = g.List(g.String, description="Not in.")
    lang = g.String(
        description="Restrict search results to a specific language. By default, searches will be performed against all languages."
    )

    @classmethod
    def apply(cls, query_set, prefix="", lang=None, **where):
        filters = {}
        exclude = {}

        if lang is not None:
            resource_name = re.findall("(.+)__.+$", prefix)[0]
            filters[resource_name + "__language__name"] = lang

        for operator, value in where.items():
            if value is not None:
                if operator == "sw":
                    filters[prefix + "__istartswith"] = value
                elif operator == "has":
                    filters[prefix + "__icontains"] = value
                elif operator == "eq":
                    filters[prefix + "__exact"] = value
                elif operator == "regex":
                    filters[prefix + "__regex"] = value
                elif operator == "in_":
                    filters[prefix + "__in"] = value
                elif operator == "ne":
                    exclude[prefix + "__exact"] = value
                elif operator == "nin":
                    exclude[prefix + "__in"] = value

        return query_set.filter(**filters).exclude(**exclude)


class SortOrder(g.Enum):
    ASC = "asc"
    DESC = "desc"

    @property
    def description(self):
        if self == SortOrder.ASC:
            return "Ascending order"
        elif self == SortOrder.DESC:
            return "Descending order"


class BaseSort(g.InputObjectType):
    order = SortOrder(
        description="The sort direction (default: ASC).", default_value=SortOrder.ASC
    )
    lang = g.String(
        description="For sorts with text translations (such as `NAME`), you **must** specify the language by which to sort. This argument will be ignored for non translated sorts."
    )

    @classmethod
    def apply(cls, query_set, order_by):
        return query_set, order_by

        # order_by = order_by or []
        # ordering = []
        # for o in order_by:
        #     if o.order == "asc":
        #         ordering.append(o.field)
        #     else:
        #         ordering.append("-" + o.field)
        # return query_set.order_by(*ordering), order_by

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
                g.String,
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
