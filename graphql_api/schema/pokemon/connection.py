import graphene as g
from .. import base
from . import types  # pylint: disable=unused-import


class PokemonConnection(g.relay.Connection, base.BaseConnection, node=types.Pokemon):
    pass


class PokemonWhere(base.BaseWhere):
    base_experience = g.Argument(base.IntFilter)
    height = g.Argument(base.IntFilter)
    is_default = g.Boolean()
    species = g.Argument(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.connection.PokemonSpeciesWhere"
        )
    )
    pokemontype__type__name = g.Argument(base.ListFilter, name="types")
    weight = g.Argument(base.IntFilter)

    @classmethod
    def apply(cls, qs, prefix="", species=None, **where):
        from graphql_api.schema.pokemon_species.connection import PokemonSpeciesWhere

        if species:
            qs = PokemonSpeciesWhere.apply(
                qs, **species, prefix=prefix + "pokemon_species__"
            )

        return super().apply(qs, **where)


class PokemonSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "PokemonSortOptions",
            [
                ("ORDER", "order"),
                ("HEIGHT", "height"),
                ("IS_DEFAULT", "is_default"),
                ("WEIGHT", "weight"),
                ("NAME", "name"),
            ],
        ),
        description="The field to sort by.",
    )
