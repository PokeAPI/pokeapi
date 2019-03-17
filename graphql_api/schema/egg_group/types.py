import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class EggGroup(g.ObjectType):
    """
    Egg Groups are categories which determine which Pokémon are able to interbreed. Pokémon may belong to either one or two Egg Groups. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Egg_Group) for greater detail.
    """

    pk = None
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: EggGroupName,
        description="The name of this language listed in different languages.",
        resolver=load_with_args("egggroup_names", using="pk"),
    )
    pokemon_species = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.types.PokemonSpeciesConnection"
        ),
        description="A list of all Pokémon species that are members of this egg group.",
    )

    def resolve_pokemon_species(self, info, **kwargs):
        from ..pokemon_species.types import PokemonSpeciesConnection

        q = models.PokemonSpecies.objects.filter(pokemonegggroup__egg_group_id=self.pk)
        return get_connection(q, PokemonSpeciesConnection, **kwargs)


class EggGroupName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
