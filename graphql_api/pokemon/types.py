import json
import graphene as g
from pokemon_v2 import models
from ..constants import IMAGE_HOST
from ..loader_key import LoaderKey
from ..utils import load, load_with_args, get_connection, get_page
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base

# from ..move.types import Move


class Pokemon(g.ObjectType):
    """
    Pokémon are the creatures that inhabit the world of the Pokémon games. They can be caught using Pokéballs and trained by battling with other Pokémon. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_%28species%29) for greater detail.
    """

    pk = None
    abilities = g.List(
        lambda: PokemonAbility,
        description="A list of abilities this Pokémon could potentially have.",
        resolver=load("pokemon_abilities", using="pk"),
    )
    base_experience = g.Int(
        description="The base experience gained for defeating this Pokémon."
    )
    # forms = g.List(
    #     g.lazy_import("graphql_api.pokemon_form.types.PokemonForm"),
    #     description="A list of forms this Pokémon can take on.",
    #     resolver=load("pokemon_forms", using="pk"),
    # )
    game_indices = g.List(
        lambda: PokemonGameIndex,
        description="A list of game indices relevent to Pokémon item by generation.",
        resolver=load("pokemon_gameindices", using="pk"),
    )
    height = g.Int(description="The height of this Pokémon.")
    # held_items = g.List(
    #     lambda: PokemonHeldItem,
    #     description="A list of items this Pokémon may be holding when encountered.",
    # )
    is_default = g.Boolean(
        description="Set for exactly one Pokémon used as the default for each species."
    )
    # location_area_encounters = g.relay.ConnectionField(
    #     g.lazy_import("graphql_api.pokemon_encounter.types.PokemonEncounterConnection"),
    #     description="A list of location area encounters for this Pokémon."
    # )
    # moves = g.relay.ConnectionField(
    #     lambda: PokemonMoveConnection,
    #     description="A list of moves along with learn methods and level details pertaining to specific version groups."
    # )
    name = g.String(description="The name of this resource.")
    order = g.Int(
        description="Order for sorting. Almost national order, except families are grouped together."
    )
    pokemon_species_id = None
    # species = g.Field(
    #     g.lazy_import("graphql_api.pokemon_species.types.PokemonSpecies"),
    #     description="The species this Pokémon belongs to.",
    #     resolver=load("pokemonspecies", using="pokemon_species_id"),
    # )
    sprites = g.Field(
        lambda: PokemonSprites,
        description="A set of sprites used to depict this Pokémon in the game.",
        resolver=load("pokemon_sprites", using="pk"),
    )
    stats = g.List(
        lambda: PokemonStat,
        description="A list of base stat values for this Pokémon.",
        resolver=load("pokemon_stats", using="pk"),
    )
    types = g.List(
        lambda: PokemonType,
        description="A list of details showing types this Pokémon has.",
        resolver=load("pokemon_types", using="pk"),
    )
    weight = g.Int(description="The weight of this Pokémon.")

    def resolve_held_items(self, info):
        def del_duplicates(pokemon_items):
            held_items = set()
            for pokemon_item in pokemon_items:
                held_item = PokemonHeldItem()
                held_item.item_id = pokemon_item.item_id
                held_item.pokemon_id = pokemon_item.pokemon_id
                held_items.add(held_item)

            return held_items

        return info.context.loaders.pokemon_items.load(self.pk).then(del_duplicates)

    # def resolve_location_area_encounters(self, info, **kwargs):
    #     from ..pokemon_encounter.connection import PokemonEncounterConnection

    #     q = models.LocationArea.objects.filter(encounter__pokemon_id=self.id).distinct()
    #     return get_connection(
    #         q, PokemonEncounterConnection,
    #         lambda data: Pokemon.get_pkmn_encounter(self, data),
    #         **kwargs
    #     )

    # def resolve_moves(self, info, **kwargs):
    #     q = models.Move.objects.filter(pokemonmove__pokemon_id=self.pk).distinct()
    #     page = get_page(q, PokemonMoveConnection.__name__, **kwargs)

    #     edges = []
    #     for entry in page:
    #         edge = PokemonMoveConnection.Edge(node=entry, cursor=page.get_cursor(entry))
    #         edge.pokemon_id = self.pk
    #         edge.move_id = entry.id
    #         edges.append(edge)

    #     return PokemonMoveConnection(
    #         edges=edges,
    #         page_info=page.page_info,
    #         total_count=page.total_count,
    #     )


class PokemonAbility(g.ObjectType):
    is_hidden = g.Boolean(description="Whether this is a hidden ability.")
    slot = g.Int(
        name="order", description="The sorting order of this ability in this Pokémon."
    )
    ability_id = None
    # ability = g.Field(
    #     g.lazy_import("graphql_api.ability.types.Ability"),
    #     description="The ability the Pokémon may have.",
    #     resolver=load("ability", using="ability_id"),
    # )


class PokemonGameIndex(g.ObjectType):
    game_index = g.Int(description="The internal ID of a resource within game data.")
    version_id = None
    version = g.Field(
        g.lazy_import("graphql_api.version.types.Version"),
        description="The version relevent to this game index.",
        resolver=load("version", using="version_id"),
    )


class PokemonHeldItem(g.ObjectType):
    item_id = None
    pokemon_id = None
    # item = g.Field(
    #     lazy_import("graphql_api.item_interface.types.ItemInterface"),
    #     description="The item the referenced Pokémon holds.",
    #     resolver=load("item", using="item_id"),
    # )
    # versions = g.List(
    #     lambda: PokemonHeldItemVersion,
    #     description="The details of the different versions in which the item is held.",
    # )

    # def resolve_versions(self, info):
    #     pokemon_items = models.PokemonItem.objects.filter(
    #         item_id=self.item_id, pokemon_id=self.pokemon_id
    #     )

    #     # Group pokemon_items by version
    #     versions = {}
    #     for pi in pokemon_items:
    #         if pi.version_id not in versions:
    #             pkmn_held_itm_ver = PokemonHeldItemVersion()
    #             pkmn_held_itm_ver.rarity = pi.rarity
    #             pkmn_held_itm_ver.version_id = pi.version_id
    #             versions[pi.version_id] = pkmn_held_itm_ver
    #     return versions.values()


class PokemonHeldItemVersion(g.ObjectType):
    rarity = g.Int(description="How often the item is held.")
    version_id = None
    version = g.Field(
        g.lazy_import("graphql_api.version.types.Version"),
        description="The version in which the item is held.",
        resolver=load("version", using="version_id"),
    )


# class PokemonMoveConnection(base.BaseConnection, g.relay.Connection, node=Move):
#     class Edge:
#         move_id = None
#         pokemon_id = None
#         version_groups = g.List(
#             lambda: PokemonMoveVersion,
#             description="The details of the version group in which the Pokémon can learn the move.",
#         )

#         def resolve_version_groups(self, info):
#             def get_version_groups(pokemon_moves):
#                 # Group pokemon_moves by version group
#                 pk_mv_vers = {}
#                 for pk_mv in pokemon_moves:
#                     if pk_mv.version_group_id not in pk_mv_vers:
#                         obj = PokemonMoveVersion(level_learned_at=pk_mv.level)
#                         obj.move_learn_method_id = pk_mv.move_learn_method_id
#                         obj.version_group_id = pk_mv.version_group_id

#                         pk_mv_vers[pk_mv.version_group_id] = obj

#                 # Return results in a consistent order
#                 return sorted(
#                     pk_mv_vers.values(),
#                     key=lambda pk_mv_ver: pk_mv_ver.level_learned_at,
#                 )

#             key = LoaderKey(0, move_id=self.move_id, pokemon_id=self.pokemon_id)
#             return info.context.loaders.pokemonmove_by_move_and_pokemon.load(key).then(
#                 get_version_groups
#             )


class PokemonMoveVersion(g.ObjectType):
    level_learned_at = g.Int(description="The minimum level to learn the move.")
    move_learn_method_id = None
    move_learn_method = g.Field(
        g.lazy_import("graphql_api.move_learn_method.types.MoveLearnMethod"),
        description="The method by which the move is learned.",
        resolver=load("movelearnmethod", using="move_learn_method_id"),
    )
    version_group_id = None
    version_group = g.Field(
        g.lazy_import("graphql_api.version_group.types.VersionGroup"),
        description="The version group in which the move is learned.",
        resolver=load("versiongroup", using="version_group_id"),
    )


def get_sprite(sprite_name):
    def inner(root, info):
        sprites_data = json.loads(root.sprites)
        if sprites_data[sprite_name]:
            return IMAGE_HOST + sprites_data[sprite_name].replace("/media/", "")
        return None

    return inner


class PokemonSprites(g.ObjectType):
    """Image sprites depicting Pokémon in battle."""

    sprites = None
    front_default = base.URI(resolver=get_sprite("front_default"))
    front_shiny = base.URI(resolver=get_sprite("front_shiny"))
    front_female = base.URI(resolver=get_sprite("front_female"))
    front_shiny_female = base.URI(resolver=get_sprite("front_shiny_female"))
    back_default = base.URI(resolver=get_sprite("back_default"))
    back_shiny = base.URI(resolver=get_sprite("back_shiny"))
    back_female = base.URI(resolver=get_sprite("back_female"))
    back_shiny_female = base.URI(resolver=get_sprite("back_shiny_female"))


class PokemonStat(g.ObjectType):
    base_stat = g.Int(name="baseValue", description="The base value of the stat.")
    effort = g.Int(
        name="effortPoints",
        description="The effort points (EV) the Pokémon has in the stat.",
    )
    stat_id = None
    # stat = g.Field(
    #     g.lazy_import("graphql_api.stat.types.Stat"),
    #     description="The stat the Pokémon has.",
    #     resolver=load("stat", using="stat_id"),
    # )


class PokemonType(g.ObjectType):
    slot = g.Int(
        name="order", description="The sorting order of this type for this Pokémon."
    )
    type_id = None
    # type = g.Field(
    #     g.lazy_import("graphql_api.type.types.Type"),
    #     description="The type the Pokémon has.",
    #     resolver=load("type", using="type_id"),
    # )
