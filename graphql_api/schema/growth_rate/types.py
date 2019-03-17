import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load, load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class GrowthRate(g.ObjectType):
    """
    Growth rates are the speed with which Pokémon gain levels through experience. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Experience) for greater detail.
    """

    pk = None
    descriptions = base.TranslationList(
        lambda: GrowthRateDescription,
        description="The description of this resource listed in different languages.",
        resolver=load_with_args("growthrate_descriptions", using="pk"),
    )
    experience = g.Int(
        description="The experience needed to reach the supplied level at this growth rate.",
        level=g.Int(required=True),
    )
    formula = g.String(
        description="The formula used to calculate the rate at which the Pokémon species gains level."
    )
    levels = g.List(
        lambda: GrowthRateExperienceLevel,
        description="A list of levels and the amount of experience needed to atain them based on this growth rate. Unless you need a complete list, we recommend using the 'experience' field with a supplied level argument instead.",
        resolver=load("growthrate_experiences", using="pk"),
    )
    name = g.ID(name="idName", description="The name of this resource.")
    pokemon_speciess = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_species.types.PokemonSpeciesConnection"
        ),
        description="A list of Pokémon species that gain levels at this growth rate.",
    )

    def resolve_experience(self, info, level=None):
        def pick_exp(experiences):
            for e in experiences:
                if e.level == level:
                    return e.experience

        return info.context.loaders.growthrate_experiences.load(self.pk).then(pick_exp)

    def resolve_pokemon_speciess(self, info, **kwargs):
        from ..pokemon_species.types import PokemonSpeciesConnection

        q = models.PokemonSpecies.objects.filter(growth_rate_id=self.pk)
        return get_connection(q, PokemonSpeciesConnection, **kwargs)


class GrowthRateDescription(base.BaseTranslation, interfaces=[i.Translation]):
    description = g.String(
        name="text",
        description="The localized resource description in a specific language.",
    )


class GrowthRateExperienceLevel(g.ObjectType):
    level = g.Int(description="The level gained.")
    experience = g.Int(
        description="The amount of experience required to reach the referenced level."
    )
