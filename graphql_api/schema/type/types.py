import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load, load_with_args, get_page  #, get_connection
from ..pokemon.types import Pokemon  # pylint: disable=unused-import
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


def load_damage_to(damage_factor):
    def get(response):
        return [t.target_type for t in response if t.damage_factor == damage_factor]

    def inner(root, info):
        return info.context.loaders.damagetype_typeefficacies.load(root.pk).then(get)

    return inner


def load_damage_from(damage_factor):
    def get(response):
        return [t.damage_type for t in response if t.damage_factor == damage_factor]

    def inner(root, info):
        return info.context.loaders.targettype_typeefficacies.load(root.pk).then(get)

    return inner


class Type(g.ObjectType):
    """
    Types are properties for Pokémon and their moves. Each type has three properties: which types of Pokémon it is super effective against, which types of Pokémon it is not very effective against, and which types of Pokémon it is completely ineffective against.
    """

    pk = None
    game_indices = g.List(
        lambda: TypeGameIndex,
        description="A list of game indices relevent to this item by generation.",
        resolver=load("type_gameindices", using="pk")
    )
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.schema.generation.types.Generation"),
        description="The generation this type was introduced in.",
        resolver=load("generation", using="generation_id"),
    )
    # move_damage_class_id = None
    # move_damage_class = g.Field(
    #     g.lazy_import("graphql_api.schema.move_damage_class.types.MoveDamageClass"),
    #     description="The class of damage inflicted by moves of this type.",
    # )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: TypeName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("type_names", using="pk"),
    )
    pokemon = g.relay.ConnectionField(
        lambda: TypePokemonConnection,
        description="A list of details of Pokémon that have this type.",
        order_by=g.List(lambda: TypePokemonSort),
    )
    # moves = g.relay.ConnectionField(
    #     g.lazy_import("graphql_api.schema.move.connection.MoveConnection"),
    #     description="A list of moves that have this type.",
    # )
    no_damage_to = g.List(
        lambda: Type,
        description="A list of types this type has no effect on.",
        resolver=load_damage_to(0),
    )
    half_damage_to = g.List(
        lambda: Type,
        description="A list of types this type is not very effective against.",
        resolver=load_damage_to(50),
    )
    double_damage_to = g.List(
        lambda: Type,
        description="A list of types this type is very effective against.",
        resolver=load_damage_to(200),
    )
    no_damage_from = g.List(
        lambda: Type,
        description="A list of types that have no effect on this type.",
        resolver=load_damage_from(0),
    )
    half_damage_from = g.List(
        lambda: Type,
        description="A list of types that are not very effective against this type.",
        resolver=load_damage_from(50),
    )
    double_damage_from = g.List(
        lambda: Type,
        description="A list of types that are very effective against this type.",
        resolver=load_damage_from(200),
    )

    def resolve_pokemon(self, info, order_by=None, **kwargs):
        q = models.PokemonType.objects.filter(type_id=self.pk)
        q = q.select_related("pokemon")
        q = TypePokemonSort.apply(q, order_by)

        page = get_page(q, TypePokemonConnection.__name__, **kwargs)
        return TypePokemonConnection(
            edges=[
                TypePokemonConnection.Edge(
                    node=entry.pokemon, order=entry.slot, cursor=page.get_cursor(entry)
                )
                for entry in page
            ],
            page_info=page.page_info,
            total_count=page.total_count,
        )

    # def resolve_moves(self, info, **kwargs):
    #     from ..move.connection import MoveConnection

    #     q = models.Move.objects.filter(type_id=self.pk)
    #     return get_connection(q, MoveConnection, **kwargs)


class TypeGameIndex(g.ObjectType):
    game_index = g.Int(description="The internal id of a resource within game data.")
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.schema.generation.types.Generation"),
        description="The generation relevent to this game index.",
        resolver=load("generation", using="generation_id"),
    )


class TypeName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class TypePokemonConnection(base.BaseConnection, g.relay.Connection, node=Pokemon):
    class Edge:
        order = g.Int(description="The order the Pokémon's types are listed in.")


class TypePokemonSort(base.BaseSort):
    field = g.InputField(
        g.Enum("TypePokemonSortOptions", [("ORDER", "slot")]),
        description="The field to sort by.",
    )
