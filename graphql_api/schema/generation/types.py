import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load, load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Generation(g.ObjectType):
    """
    A generation is a grouping of the Pokémon games that separates them based on the Pokémon they include. In each generation, a new set of Pokémon, Moves, Abilities and Types that did not exist in the previous generation are released.
    """

    pk = None
    # abilities = g.relay.ConnectionField(
    #     g.lazy_import("graphql_api.schema.ability.connection.AbilityConnection"),
    #     description="A list of abilities that were introduced in this generation.",
    # )
    region_id = None
    main_region = g.Field(
        g.lazy_import("graphql_api.schema.region.types.Region"),
        description="The main region travelled in this generation.",
        resolver=load("region", using="region_id")
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: GenerationName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("generation_names", using="pk")
    )
    # moves = g.relay.ConnectionField(
    #     g.lazy_import("graphql_api.schema.move.connection.MoveConnection"),
    #     description="A list of moves that were introduced in this generation.",
    # )
    pokemon_species = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.types.PokemonSpeciesConnection"
        ),
        description="A list of Pokémon species that were introduced in this generation.",
    )
    # types = g.List(
    #     g.lazy_import("graphql_api.schema.type.types.Type"),
    #     description="A list of types that were introduced in this generation.",
    #     resolver=load("generation_types", using="pk")
    # )
    version_groups = g.List(
        g.lazy_import("graphql_api.schema.version_group.types.VersionGroup"),
        description="A list of version groups that were introduced in this generation.",
        resolver=load("generation_versiongroups", using="pk")
    )

    # def resolve_abilities(self, info, **kwargs):
    #     from ..ability import connection as conn

    #     q = models.Ability.objects.filter(generation_id=self.pk)
    #     return get_connection(q, types.AbilityConnection, **kwargs)

    # def resolve_moves(self, info, **kwargs):
    #     from ..move import connection as conn

    #     q = models.Move.objects.filter(generation_id=self.pk)
    #     return get_connection(q, conn.MoveConnection, **kwargs)

    def resolve_pokemon_species(self, info, **kwargs):
        from ..pokemon_species import connection as conn

        q = models.PokemonSpecies.objects.filter(generation_id=self.pk)
        return get_connection(q, conn.PokemonSpeciesConnection, **kwargs)



class GenerationName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )