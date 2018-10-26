import graphene as g
from ..utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Language(g.ObjectType):
    """Languages for translations of resource information."""

    pk = None
    name = g.ID(description="The name of this resource.")
    official = g.Boolean(
        name="isOfficial",
        description="Whether or not the games are published in this language.",
    )
    # iso639 = g.String(
    #     name="countryCode",
    #     description="The ISO 639 two-letter code of the country where this language is spoken. Note that it is not unique.",
    # )
    iso3166 = g.String(
        name="languageCode",
        description="The ISO 3166 two-letter code of the language. Note that it is not unique.",
    )
    names = base.TranslationList(
        lambda: LanguageName,
        description="The name of this language listed in different languages.",
        resolver=load_with_args("language_names", using="pk"),
    )


class LanguageName(g.ObjectType, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
    local_language_id = None
    language = g.Field(
        Language,
        description="The local language this language name is in.",
        resolver=load("language", using="local_language_id"),
    )
