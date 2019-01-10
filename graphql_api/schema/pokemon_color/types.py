import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class PokemonColor(g.ObjectType):
    """
    Colors used for sorting Pokémon in a Pokédex. The color listed in the Pokédex is usually the color most apparent or covering each Pokémon's body. No orange category exists; Pokémon that are primarily orange are listed as red or brown.
    """

    pk = None
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: PokemonColorName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("pokemoncolor_names", using="pk"),
    )
    pokemon_speciess = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.connection.PokemonSpeciesConnection"
        ),
        description="A list of all Pokémon species that have this color.",
    )

    def resolve_pokemon_speciess(self, info, **kwargs):
        from ..pokemon_species.connection import PokemonSpeciesConnection

        q = models.PokemonSpecies.objects.filter(pokemon_color_id=self.pk)
        return get_connection(q, PokemonSpeciesConnection, **kwargs)


class PokemonColorName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text",
        description="The localized resource name in a specific language.",
    )
