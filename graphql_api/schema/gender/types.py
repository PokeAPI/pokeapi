import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection


class Gender(g.ObjectType):
    """
    Genders were introduced in Generation II for the purposes of breeding Pokémon but can also result in visual differences or even different evolutionary lines. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Gender) for greater detail.
    """

    pk = None
    name = g.ID(name="idName", description="The name of this resource.")
    pokemon_speciess = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.connection.PokemonSpeciesConnection"
        ),
        description="A list of Pokémon species that can be this gender and how likely it is that they will be, as well as if it's required for evolution.",
    )

    def resolve_pokemon_speciess(self, info, **kwargs):
        from ..pokemon_species.connection import PokemonSpeciesConnection

        if self.name == "male":
            q = models.PokemonSpecies.objects.filter(gender_rate__gt=0)
        elif self.name == "female":
            q = models.PokemonSpecies.objects.filter(gender_rate__range=[0, 7])
        elif self.name == "genderless":
            q = models.PokemonSpecies.objects.filter(gender_rate=-1)
        return get_connection(q, PokemonSpeciesConnection, **kwargs)
