import graphene as g
from .. import base


class PokemonSpeciesWhere(base.BaseWhere):
    base_happiness = g.Argument(base.IntFilter)
    capture_rate = g.Argument(base.IntFilter)
    pokemon_color__name = g.List(g.ID, name="color__idName")
    pokemonegggroup__egg_group__name = g.Argument(base.ListFilter, name="eggGroups")
    evolves_from_species__name = g.List(g.ID, name="evolvesFromSpecies__idName")
    gender_rate = g.Argument(base.IntFilter)
    generation__name = g.List(g.ID, name="generation__idName")
    growth_rate__name = g.List(g.ID, name="growthRate__idName")
    pokemon_habitat__name = g.List(g.ID, name="habitat__idName")
    has_gender_differences = g.Boolean()
    hatch_counter = g.Argument(base.IntFilter)
    is_baby = g.Boolean()
    is_genderless = g.Boolean()
    forms_switchable = g.Boolean(name="isFormsSwitchable")
    pokemonspeciesname__name = g.Argument(base.TextFilter, name="name")
    pokemon_shape__name = g.List(g.ID, name="shape__idName")

    @classmethod
    def apply(cls, query_set, prefix="", gender_rate=None, is_genderless=None, **where):
        if is_genderless is not None:
            query_set = query_set.filter(**{prefix + "gender_rate": -1})
        if gender_rate:
            filters = {
                prefix + "gender_rate__" + operator: value / 12.5
                for operator, value in gender_rate.items()
                if value is not None
            }
            query_set = query_set.filter(**filters)
            query_set = query_set.exclude(**{prefix + "gender_rate": -1})

        return super().apply(query_set, **where, prefix=prefix)
