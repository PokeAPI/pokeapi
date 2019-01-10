import graphene as g
from django.db.models import OuterRef, Subquery
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import


class PokemonSpeciesConnection(
    g.relay.Connection, base.BaseConnection, node=types.PokemonSpecies
):
    pass


class PokemonSpeciesWhere(base.BaseWhere):
    pokemonspeciesname__name = g.Argument(base.TextFilter, name="name")
    base_happiness = g.Argument(base.IntFilter)
    capture_rate = g.Argument(base.IntFilter)
    pokemon_color__name = g.List(g.ID, name="color_idName")
    pokemonegggroup__egg_group__name = g.Argument(base.ListFilter, name="eggGroups")
    evolves_from_species__name = g.List(g.ID, name="evolvesFromSpecies_idName")
    gender_rate = g.Argument(base.IntFilter)
    generation__name = g.List(g.ID, name="generation_idName")
    growth_rate__name = g.List(g.ID, name="growthRate_idName")
    pokemon_habitat__name = g.List(g.ID, name="habitat_idName")
    has_gender_differences = g.Boolean()
    hatch_counter = g.Argument(base.IntFilter)
    is_baby = g.Boolean()
    is_genderless = g.Boolean()
    forms_switchable = g.Boolean(name="isFormsSwitchable")
    pokemon_shape__name = g.List(g.ID, name="shape_idName")

    @classmethod
    def apply(cls, query_set, prefix="", gender_rate=None, is_genderless=None, **where):
        if is_genderless is not None:
            query_set = query_set.filter(**{prefix + "gender_rate": -1})
        if gender_rate:
            filters = {
                prefix + "gender_rate__" + operator: value / 12.5
                for operator, value in gender_rate.items()
            }
            query_set = query_set.filter(**filters)
            query_set = query_set.exclude(**{prefix + "gender_rate": -1})

        return super().apply(query_set, **where, prefix=prefix)


class PokemonSpeciesSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "PokemonSpeciesSortOptions",
            [
                ("BASE_HAPPINESS", "base_happiness"),
                ("CAPTURE_RATE", "capture_rate"),
                ("GENDER_RATE", "gender_rate"),
                ("HAS_GENDER_DIFFERENCES", "has_gender_differences"),
                ("HATCH_COUNTER", "hatch_counter"),
                ("IS_BABY", "is_baby"),
                ("IS_FORMS_SWITCHABLE", "forms_switchable"),
                ("ORDER", "order"),
                ("NAME", "name_annotation"),
            ],
        ),
        description="The field to sort by.",
    )

    @classmethod
    def apply(cls, query_set, order_by):
        order_by = order_by or []
        for o in order_by:
            if o.field == "name_annotation":
                cls.check_lang(o)
                # Add an annotation with the name to sort by
                subquery = models.PokemonSpeciesName.objects.filter(
                    pokemon_species_id=OuterRef("pk"), language__name=o.lang
                )
                query_set = query_set.annotate(
                    name_annotation=Subquery(subquery.values("name")[:1])
                )

        return super().apply(query_set, order_by)
