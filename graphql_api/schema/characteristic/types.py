import graphene as g
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Characteristic(g.ObjectType):
    """
    Characteristics indicate which stat contains a Pokémon's highest [IV (individual value)](https://bulbapedia.bulbagarden.net/wiki/Individual_values). A Pokémon's Characteristic is determined by the remainder of its highest IV divided by 5 (geneModulo). Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Characteristic) for greater detail.
    """

    descriptions = base.TranslationList(
        lambda: CharacteristicDescription,
        description="The description of this resource listed in different languages.",
        resolver=load_with_args("characteristic_descriptions", using="pk"),
    )
    gene_mod_5 = g.Int(
        name="geneModulo",
        description="The remainder of the highest stat/IV divided by 5."
    )
    stat_id = None
    highest_stat = g.Field(
        g.lazy_import("graphql_api.schema.stat.types.Stat"),
        description="The stat that contains a Pokémon's highest [IV (indivual value)](https://bulbapedia.bulbagarden.net/wiki/Individual_values).",
        resolver=load("stat", using="stat_id"),
    )
    pk = g.ID(name="name", description="The name of this resource.")
    possible_values = g.List(
        g.Int,
        description="The possible values of the highest stat that would result in a Pokémon receiving this characteristic when divided by 5."
    )

    def resolve_possible_values(self, info):
        mod = self.gene_mod_5
        values = []
        while mod <= 30:
            values.append(mod)
            mod += 5
        return values


class CharacteristicDescription(base.BaseTranslation, interfaces=[i.Translation]):
    description = g.String(
        name="text",
        description="The localized resource description in a specific language.",
    )
