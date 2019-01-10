import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class PokemonHabitat(g.ObjectType):
    """
    Habitats are generally different terrain Pokémon can be found in but can also be areas designated for rare or legendary Pokémon.
    """

    pk = None
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: PokemonHabitatName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("pokemonhabitat_names", using="pk"),
    )
    pokemon_speciess = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.connection.PokemonSpeciesConnection"
        ),
        description="A list of the Pokémon species that can be found in this habitat.",
    )

    def resolve_pokemon_speciess(self, info, **kwargs):
        from ..pokemon_species.connection import PokemonSpeciesConnection

        q = models.PokemonSpecies.objects.filter(pokemon_habitat_id=self.pk)
        return get_connection(q, PokemonSpeciesConnection, **kwargs)


class PokemonHabitatName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text",
        description="The localized resource name in a specific language.",
    )
