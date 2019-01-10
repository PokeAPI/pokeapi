import graphene as g
from graphql_api.utils import load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class EncounterMethod(g.ObjectType):
    """
    Methods by which the player might encounter Pokémon in the wild, e.g., walking in tall grass. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Wild_Pok%C3%A9mon) for greater detail.
    """

    pk = None
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: EncounterMethodName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("encountermethod_names", using="pk"),
    )
    order = g.Int(description="A good value for sorting.")


class EncounterMethodName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text",
        description="The localized resource name in a specific language.",
    )
