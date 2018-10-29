import graphene as g
from pokemon_v2 import models
from ..utils import load, load_with_args, get_page
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base
from ..pokemon_species.types import PokemonSpecies  # pylint: disable=unused-import


class Pokedex(g.ObjectType):
    """
    A Pokédex is a handheld electronic encyclopedia device; one which is capable of recording and retaining information of the various Pokémon in a given region with the exception of the national dex and some smaller dexes related to portions of a region. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pokedex) for greater detail.
    """

    pk = None
    is_main_series = g.Boolean(
        description="Whether or not this Pokédex originated in the main series of the video games."
    )
    descriptions = base.TranslationList(
        lambda: PokedexDescription,
        description="The description of this resource listed in different languages.",
        resolver=load_with_args("pokedex_descriptions", using="pk")
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: PokedexName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("pokedex_names", using="pk")
    )
    pokemon_entries = g.relay.ConnectionField(
        lambda: PokedexEntryConnection,
        description="A list of Pokémon catalogued in this Pokédex and their indexes.",
        order_by=g.List(lambda: PokedexEntrySort),
    )

    def resolve_pokemon_entries(self, info, order_by=None, **kwargs):
        q = models.PokemonDexNumber.objects.filter(pokedex_id=self.pk)
        q = q.select_related("pokemon_species")
        q = PokedexEntrySort.apply(q, order_by)

        page = get_page(q, PokedexEntryConnection.__name__, **kwargs)
        edges = []
        for entry in page:
            edges.append(
                PokedexEntryConnection.Edge(
                    node=entry.pokemon_species,
                    entry_number=entry.pokedex_number,
                    cursor=page.get_cursor(entry),
                )
            )
        return PokedexEntryConnection(
            edges=edges, page_info=page.page_info, total_count=page.total_count
        )


class PokedexDescription(base.BaseTranslation, interfaces=[i.Translation]):
    description = g.String(
        name="text",
        description="The localized resource description in a specific language.",
    )


class PokedexName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class PokedexEntryConnection(
    base.BaseConnection, g.relay.Connection, node=PokemonSpecies
):
    class Edge:
        entry_number = g.Int(
            description="The index of this Pokémon species entry within the Pokédex."
        )


class PokedexEntrySort(base.BaseSort):
    sort = g.InputField(
        g.Enum("PokedexEntrySortOptions", [("ENTRY_NUMBER", "pokedex_number")]),
        description="The field to sort by.",
    )
