import graphene as g
from pokemon_v2 import models
from ..loader_key import LoaderKey
from ..utils import get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Generation(g.ObjectType):
    """
    A generation is a grouping of the Pokémon games that separates them based on the Pokémon they include. In each generation, a new set of Pokémon, Moves, Abilities and Types that did not exist in the previous generation are released.
    """

    pk = None
    # abilities = g.relay.ConnectionField(
    #     g.lazy_import("graphql_api.ability.connection.AbilityConnection"),
    #     description="A list of abilities that were introduced in this generation.",
    # )
    region_id = None
    main_region = g.Field(
        g.lazy_import("graphql_api.region.types.Region"),
        description="The main region travelled in this generation.",
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: GenerationName,
        description="The name of this resource listed in different languages.",
    )
    # moves = g.relay.ConnectionField(
    #     g.lazy_import("graphql_api.move.connection.MoveConnection"),
    #     description="A list of moves that were introduced in this generation.",
    # )
    # pokemon_species = g.relay.ConnectionField(
    #     g.lazy_import(
    #         "graphql_api.pokemon_species.connection.PokemonSpeciesConnection"
    #     ),
    #     description="A list of Pokémon species that were introduced in this generation.",
    # )
    # types = g.List(
    #     g.lazy_import("graphql_api.type.types.Type"),
    #     description="A list of types that were introduced in this generation.",
    # )
    version_groups = g.List(
        g.lazy_import("graphql_api.version_group.types.VersionGroup"),
        description="A list of version groups that were introduced in this generation.",
    )

    # def resolve_abilities(self, info, **kwargs):
    #     from ..ability import connection as conn

    #     q = models.Ability.objects.filter(generation_id=self.pk)
    #     return getConnection(q, types.AbilityConnection, **kwargs)

    def resolve_names(self, info, **kwargs):
        return info.context.loaders.generation_names.load(LoaderKey(self.pk, **kwargs))

    def resolve_main_region(self, info):
        return info.context.loaders.region.load(self.region_id)

    # def resolve_moves(self, info, **kwargs):
    #     from ..move import connection as conn

    #     q = models.Move.objects.filter(generation_id=self.pk)
    #     return getConnection(q, conn.MoveConnection, **kwargs)

    # def resolve_pokemon_species(self, info, **kwargs):
    #     from ..pokemon_species import connection as conn

    #     q = models.PokemonSpecies.objects.filter(generation_id=self.pk)
    #     return getConnection(q, conn.PokemonSpeciesConnection, **kwargs)

    def resolve_types(self, info):
        return info.context.loaders.generation_types.load(self.pk)

    def resolve_version_groups(self, info):
        return info.context.loaders.generation_versiongroups.load(self.pk)


class GenerationName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
