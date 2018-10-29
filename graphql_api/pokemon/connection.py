import graphene as g
from .. import base
from . import types  # pylint: disable=unused-import


class PokemonConnection(g.relay.Connection, base.BaseConnection, node=types.Pokemon):
    pass


class PokemonWhere(base.BaseWhere):
    name = g.Argument(base.TextSearch)

    @classmethod
    def apply(cls, query_set, name=None, **where):
        # Unfortunately, Pokemon doesn't have a 'names' property,
        # so searching against the 'name' property will have to do.
        if name:
            if name.case_sensitive:
                query_set = query_set.filter(name__contains=name.query)
            else:
                query_set = query_set.filter(name__icontains=name.query)

        return super().apply(query_set, **where)


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
