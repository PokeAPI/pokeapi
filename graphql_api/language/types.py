import graphene as g
from ..loader_key import LoaderKey
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
    )

    def resolve_names(self, info, **kwargs):
        return info.context.loaders.language_names.load(LoaderKey(self.pk, **kwargs))


class LanguageName(g.ObjectType, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
    local_language_id = None
    language = g.Field(
        Language, description="The local language this language name is in."
    )

    def resolve_language(self, info):
        return info.context.loaders.language.load(self.local_language_id)
