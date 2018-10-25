import graphene as g


class Translation(g.Interface):
    """Represents a text translation for a resource in a specific language."""

    language = g.Field(
        g.lazy_import("graphql_api.language.types.Language"),
        description="The language this text translation is in.",
    )
    text = g.String(
        description="The localized text for a resource in a specific language."
    )
