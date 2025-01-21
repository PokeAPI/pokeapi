import re
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import *
from .serializers import *

# pylint: disable=no-member, attribute-defined-outside-init

###########################
#  BEHAVIOR ABSTRACTIONS  #
###########################


class ListOrDetailSerialRelation:
    """
    Mixin to allow association with separate serializers
    for list or detail view.
    """

    list_serializer_class = None

    def get_serializer_class(self):
        if self.action == "list" and self.list_serializer_class is not None:
            return self.list_serializer_class
        return self.serializer_class


class NameOrIdRetrieval:
    """
    Mixin to allow retrieval of resources by
    pk (in this case ID) or by name
    """

    idPattern = re.compile(r"^-?[0-9]+$")
    # Allow alphanumeric, hyphen, plus, and space (Space added for test cases using name for lookup, ex: 'base pkm')
    namePattern = re.compile(r"^[0-9A-Za-z\-\+ ]+$")

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = self.request.GET.get("q", "")

        if filter:
            queryset = queryset.filter(Q(name__icontains=filter))

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        lookup = self.kwargs["pk"]

        if self.idPattern.match(lookup):
            lookup_id = int(lookup)
            if abs(lookup_id) > 2147483647:
                raise Http404

            resp = get_object_or_404(queryset, pk=lookup)

        elif self.namePattern.match(lookup):
            resp = get_object_or_404(queryset, name__iexact=lookup)

        else:
            raise Http404

        return resp


q_query_string_parameter = OpenApiParameter(
    name="q",
    description="> Only available locally and not at [pokeapi.co](https://pokeapi.co/docs/v2)\nCase-insensitive query applied on the `name` property. ",
    location=OpenApiParameter.QUERY,
    type=OpenApiTypes.STR,
)

retrieve_path_parameter = OpenApiParameter(
    name="id",
    description="This parameter can be a string or an integer.",
    location=OpenApiParameter.PATH,
    type=OpenApiTypes.STR,
    required=True,
)


@extend_schema_view(list=extend_schema(parameters=[q_query_string_parameter]))
class PokeapiCommonViewset(
    ListOrDetailSerialRelation, NameOrIdRetrieval, viewsets.ReadOnlyModelViewSet
):
    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)

    pass


##########
#  APIS  #
##########


@extend_schema(
    description="Abilities provide passive effects for Pokémon in battle or in the overworld. Pokémon have multiple possible abilities but can have only one ability at a time. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Ability) for greater detail.",
    tags=["pokemon"],
)
class AbilityResource(PokeapiCommonViewset):
    queryset = Ability.objects.all()
    serializer_class = AbilityDetailSerializer
    list_serializer_class = AbilitySummarySerializer


@extend_schema(
    description="Berries are small fruits that can provide HP and status condition restoration, stat enhancement, and even damage negation when eaten by Pokémon. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Berry) for greater detail.",
    tags=["berries"],
    summary="Get a berry",
)
@extend_schema_view(
    list=extend_schema(
        summary="List berries",
    )
)
class BerryResource(PokeapiCommonViewset):
    queryset = Berry.objects.all()
    serializer_class = BerryDetailSerializer
    list_serializer_class = BerrySummarySerializer


@extend_schema(
    description="Berries can be soft or hard. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Category:Berries_by_firmness) for greater detail.",
    tags=["berries"],
    summary="Get berry by firmness",
)
@extend_schema_view(
    list=extend_schema(
        summary="List berry firmness",
    )
)
class BerryFirmnessResource(PokeapiCommonViewset):
    queryset = BerryFirmness.objects.all()
    serializer_class = BerryFirmnessDetailSerializer
    list_serializer_class = BerryFirmnessSummarySerializer


@extend_schema(
    description="Flavors determine whether a Pokémon will benefit or suffer from eating a berry based on their **nature**. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Flavor) for greater detail.",
    summary="Get berries by flavor",
    tags=["berries"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List berry flavors",
    )
)
class BerryFlavorResource(PokeapiCommonViewset):
    queryset = BerryFlavor.objects.all()
    serializer_class = BerryFlavorDetailSerializer
    list_serializer_class = BerryFlavorSummarySerializer


@extend_schema(
    description="Characteristics indicate which stat contains a Pokémon's highest IV. A Pokémon's Characteristic is determined by the remainder of its highest IV divided by 5 (gene_modulo). Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Characteristic) for greater detail.",
    summary="Get characteristic",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List charecterictics",
    )
)
class CharacteristicResource(PokeapiCommonViewset):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicDetailSerializer
    list_serializer_class = CharacteristicSummarySerializer


@extend_schema(
    description="Contest effects refer to the effects of moves when used in contests.",
    tags=["contests"],
    summary="Get contest effect",
)
@extend_schema_view(
    list=extend_schema(
        summary="List contest effects",
    )
)
class ContestEffectResource(PokeapiCommonViewset):
    queryset = ContestEffect.objects.all()
    serializer_class = ContestEffectDetailSerializer
    list_serializer_class = ContestEffectSummarySerializer


@extend_schema(
    description="Contest types are categories judges used to weigh a Pokémon's condition in Pokémon contests. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Contest_condition) for greater detail.",
    summary="Get contest type",
    tags=["contests"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List contest types",
    )
)
class ContestTypeResource(PokeapiCommonViewset):
    queryset = ContestType.objects.all()
    serializer_class = ContestTypeDetailSerializer
    list_serializer_class = ContestTypeSummarySerializer


@extend_schema(
    description="Egg Groups are categories which determine which Pokémon are able to interbreed. Pokémon may belong to either one or two Egg Groups. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Egg_Group) for greater detail.",
    summary="Get egg group",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List egg groups",
    )
)
class EggGroupResource(PokeapiCommonViewset):
    queryset = EggGroup.objects.all()
    serializer_class = EggGroupDetailSerializer
    list_serializer_class = EggGroupSummarySerializer


@extend_schema(
    description="Conditions which affect what pokemon might appear in the wild, e.g., day or night.",
    summary="Get encounter condition",
    tags=["encounters"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List encounter conditions",
    )
)
class EncounterConditionResource(PokeapiCommonViewset):
    queryset = EncounterCondition.objects.all()
    serializer_class = EncounterConditionDetailSerializer
    list_serializer_class = EncounterConditionSummarySerializer


@extend_schema(
    description="Encounter condition values are the various states that an encounter condition can have, i.e., time of day can be either day or night.",
    summary="Get encounter condition value",
    tags=["encounters"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List encounter condition values",
    )
)
class EncounterConditionValueResource(PokeapiCommonViewset):
    queryset = EncounterConditionValue.objects.all()
    serializer_class = EncounterConditionValueDetailSerializer
    list_serializer_class = EncounterConditionValueSummarySerializer


@extend_schema(
    description="Methods by which the player might can encounter Pokémon in the wild, e.g., walking in tall grass. Check out Bulbapedia for greater detail.",
    summary="Get encounter method",
    tags=["encounters"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List encounter methods",
    )
)
class EncounterMethodResource(PokeapiCommonViewset):
    queryset = EncounterMethod.objects.all()
    serializer_class = EncounterMethodDetailSerializer
    list_serializer_class = EncounterMethodSummarySerializer


@extend_schema(
    description="Evolution chains are essentially family trees. They start with the lowest stage within a family and detail evolution conditions for each as well as Pokémon they can evolve into up through the hierarchy.",
    summary="Get evolution chain",
    tags=["evolution"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List evolution chains",
    )
)
class EvolutionChainResource(PokeapiCommonViewset):
    queryset = EvolutionChain.objects.all()
    serializer_class = EvolutionChainDetailSerializer
    list_serializer_class = EvolutionChainSummarySerializer


@extend_schema(
    description="Evolution triggers are the events and conditions that cause a Pokémon to evolve. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Methods_of_evolution) for greater detail.",
    summary="Get evolution trigger",
    tags=["evolution"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List evolution triggers",
    )
)
class EvolutionTriggerResource(PokeapiCommonViewset):
    queryset = EvolutionTrigger.objects.all()
    serializer_class = EvolutionTriggerDetailSerializer
    list_serializer_class = EvolutionTriggerSummarySerializer


@extend_schema(
    description="A generation is a grouping of the Pokémon games that separates them based on the Pokémon they include. In each generation, a new set of Pokémon, Moves, Abilities and Types that did not exist in the previous generation are released.",
    summary="Get genration",
    tags=["games"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List genrations",
    )
)
class GenerationResource(PokeapiCommonViewset):
    queryset = Generation.objects.all()
    serializer_class = GenerationDetailSerializer
    list_serializer_class = GenerationSummarySerializer


@extend_schema(
    description="Genders were introduced in Generation II for the purposes of breeding Pokémon but can also result in visual differences or even different evolutionary lines. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Gender) for greater detail.",
    summary="Get gender",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List genders",
    )
)
class GenderResource(PokeapiCommonViewset):
    queryset = Gender.objects.all()
    serializer_class = GenderDetailSerializer
    list_serializer_class = GenderSummarySerializer


@extend_schema(
    description="Growth rates are the speed with which Pokémon gain levels through experience. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Experience) for greater detail.",
    summary="Get growth rate",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List growth rates",
    )
)
class GrowthRateResource(PokeapiCommonViewset):
    queryset = GrowthRate.objects.all()
    serializer_class = GrowthRateDetailSerializer
    list_serializer_class = GrowthRateSummarySerializer


@extend_schema(
    description="An item is an object in the games which the player can pick up, keep in their bag, and use in some manner. They have various uses, including healing, powering up, helping catch Pokémon, or to access a new area.",
    summary="Get item",
    tags=["items"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List items",
    )
)
class ItemResource(PokeapiCommonViewset):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    list_serializer_class = ItemSummarySerializer


@extend_schema(
    description="Item categories determine where items will be placed in the players bag.",
    summary="Get item category",
    tags=["items"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List item categories",
    )
)
class ItemCategoryResource(PokeapiCommonViewset):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategoryDetailSerializer
    list_serializer_class = ItemCategorySummarySerializer


@extend_schema(
    description='Item attributes define particular aspects of items, e.g."usable in battle" or "consumable".',
    summary="Get item attribute",
    tags=["items"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List item attributes",
    )
)
class ItemAttributeResource(PokeapiCommonViewset):
    queryset = ItemAttribute.objects.all()
    serializer_class = ItemAttributeDetailSerializer
    list_serializer_class = ItemAttributeSummarySerializer


@extend_schema(
    description='The various effects of the move"Fling" when used with different items.',
    summary="Get item fling effect",
    tags=["items"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List item fling effects",
    )
)
class ItemFlingEffectResource(PokeapiCommonViewset):
    queryset = ItemFlingEffect.objects.all()
    serializer_class = ItemFlingEffectDetailSerializer
    list_serializer_class = ItemFlingEffectSummarySerializer


@extend_schema(
    description="Pockets within the players bag used for storing items by category.",
    summary="Get item pocket",
    tags=["items"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List item pockets",
    )
)
class ItemPocketResource(PokeapiCommonViewset):
    queryset = ItemPocket.objects.all()
    serializer_class = ItemPocketDetailSerializer
    list_serializer_class = ItemPocketSummarySerializer


@extend_schema(
    description="Languages for translations of API resource information.",
    summary="Get language",
    tags=["utility"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List languages",
    )
)
class LanguageResource(PokeapiCommonViewset):
    queryset = Language.objects.all()
    serializer_class = LanguageDetailSerializer
    list_serializer_class = LanguageSummarySerializer


@extend_schema(
    description="Locations that can be visited within the games. Locations make up sizable portions of regions, like cities or routes.",
    summary="Get location",
    tags=["location"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List locations",
    )
)
class LocationResource(PokeapiCommonViewset):
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer
    list_serializer_class = LocationSummarySerializer


@extend_schema(
    description="Location areas are sections of areas, such as floors in a building or cave. Each area has its own set of possible Pokémon encounters.",
    summary="Get location area",
    tags=["location"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List location areas",
    )
)
class LocationAreaResource(ListOrDetailSerialRelation, viewsets.ReadOnlyModelViewSet):
    queryset = LocationArea.objects.all()
    serializer_class = LocationAreaDetailSerializer
    list_serializer_class = LocationAreaSummarySerializer


@extend_schema(
    description="Machines are the representation of items that teach moves to Pokémon. They vary from version to version, so it is not certain that one specific TM or HM corresponds to a single Machine.",
    summary="Get machine",
    tags=["machines"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List machines",
    )
)
class MachineResource(PokeapiCommonViewset):
    queryset = Machine.objects.all()
    serializer_class = MachineDetailSerializer
    list_serializer_class = MachineSummarySerializer


@extend_schema(
    description="Moves are the skills of Pokémon in battle. In battle, a Pokémon uses one move each turn. Some moves (including those learned by Hidden Machine) can be used outside of battle as well, usually for the purpose of removing obstacles or exploring new areas.",
    summary="Get move",
    tags=["moves"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List moves",
    )
)
class MoveResource(PokeapiCommonViewset):
    queryset = Move.objects.all()
    serializer_class = MoveDetailSerializer
    list_serializer_class = MoveSummarySerializer


@extend_schema(
    description="Damage classes moves can have, e.g. physical, special, or non-damaging.",
    summary="Get move damage class",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List move damage classes",
    )
)
class MoveDamageClassResource(PokeapiCommonViewset):
    queryset = MoveDamageClass.objects.all()
    serializer_class = MoveDamageClassDetailSerializer
    list_serializer_class = MoveDamageClassSummarySerializer


@extend_schema(
    description="Move Ailments are status conditions caused by moves used during battle. See [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Status_condition) for greater detail.",
    summary="Get move meta ailment",
    tags=["moves"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List move meta ailments",
    )
)
class MoveMetaAilmentResource(PokeapiCommonViewset):
    queryset = MoveMetaAilment.objects.all()
    serializer_class = MoveMetaAilmentDetailSerializer
    list_serializer_class = MoveMetaAilmentSummarySerializer


@extend_schema(
    description="Styles of moves when used in the Battle Palace. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Battle_Frontier_(Generation_III)) for greater detail.",
    summary="Get move battle style",
    tags=["moves"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List move battle styles",
    )
)
class MoveBattleStyleResource(PokeapiCommonViewset):
    queryset = MoveBattleStyle.objects.all()
    serializer_class = MoveBattleStyleDetailSerializer
    list_serializer_class = MoveBattleStyleSummarySerializer


@extend_schema(
    description="Very general categories that loosely group move effects.",
    summary="Get move meta category",
    tags=["moves"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List move meta categories",
    )
)
class MoveMetaCategoryResource(PokeapiCommonViewset):
    queryset = MoveMetaCategory.objects.all()
    serializer_class = MoveMetaCategoryDetailSerializer
    list_serializer_class = MoveMetaCategorySummarySerializer


@extend_schema(
    description="Methods by which Pokémon can learn moves.",
    summary="Get move learn method",
    tags=["moves"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List move learn methods",
    )
)
class MoveLearnMethodResource(PokeapiCommonViewset):
    queryset = MoveLearnMethod.objects.all()
    serializer_class = MoveLearnMethodDetailSerializer
    list_serializer_class = MoveLearnMethodSummarySerializer


@extend_schema(
    description="Targets moves can be directed at during battle. Targets can be Pokémon, environments or even other moves.",
    summary="Get move target",
    tags=["moves"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List move targets",
    )
)
class MoveTargetResource(PokeapiCommonViewset):
    queryset = MoveTarget.objects.all()
    serializer_class = MoveTargetDetailSerializer
    list_serializer_class = MoveTargetSummarySerializer


@extend_schema(
    description="Natures influence how a Pokémon's stats grow. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Nature) for greater detail.",
    summary="Get nature",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List natures",
    )
)
class NatureResource(PokeapiCommonViewset):
    queryset = Nature.objects.all()
    serializer_class = NatureDetailSerializer
    list_serializer_class = NatureSummarySerializer


@extend_schema(
    description="Areas used for grouping Pokémon encounters in Pal Park. They're like habitats that are specific to Pal Park.",
    summary="Get pal park area",
    tags=["location"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pal park areas",
    )
)
class PalParkAreaResource(PokeapiCommonViewset):
    queryset = PalParkArea.objects.all()
    serializer_class = PalParkAreaDetailSerializer
    list_serializer_class = PalParkAreaSummarySerializer


@extend_schema(
    description="Pokeathlon Stats are different attributes of a Pokémon's performance in Pokéathlons. In Pokéathlons, competitions happen on different courses; one for each of the different Pokéathlon stats. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9athlon) for greater detail.",
    summary="Get pokeathlon stat",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokeathlon stats",
    )
)
class PokeathlonStatResource(PokeapiCommonViewset):
    queryset = PokeathlonStat.objects.all()
    serializer_class = PokeathlonStatDetailSerializer
    list_serializer_class = PokeathlonStatSummarySerializer


@extend_schema(
    description="A Pokédex is a handheld electronic encyclopedia device; one which is capable of recording and retaining information of the various Pokémon in a given region with the exception of the national dex and some smaller dexes related to portions of a region. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pokedex) for greater detail.",
    summary="Get pokedex",
    tags=["games"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokedex",
    )
)
class PokedexResource(PokeapiCommonViewset):
    queryset = Pokedex.objects.all()
    serializer_class = PokedexDetailSerializer
    list_serializer_class = PokedexSummarySerializer


@extend_schema(
    description="Colors used for sorting Pokémon in a Pokédex. The color listed in the Pokédex is usually the color most apparent or covering each Pokémon's body. No orange category exists; Pokémon that are primarily orange are listed as red or brown.",
    summary="Get pokemon color",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokemon colors",
    )
)
class PokemonColorResource(PokeapiCommonViewset):
    queryset = PokemonColor.objects.all()
    serializer_class = PokemonColorDetailSerializer
    list_serializer_class = PokemonColorSummarySerializer


@extend_schema(
    description="Some Pokémon may appear in one of multiple, visually different forms. These differences are purely cosmetic. For variations within a Pokémon species, which do differ in more than just visuals, the 'Pokémon' entity is used to represent such a variety.",
    summary="Get pokemon form",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokemon forms",
    )
)
class PokemonFormResource(PokeapiCommonViewset):
    queryset = PokemonForm.objects.all()
    serializer_class = PokemonFormDetailSerializer
    list_serializer_class = PokemonFormSummarySerializer


@extend_schema(
    description="Habitats are generally different terrain Pokémon can be found in but can also be areas designated for rare or legendary Pokémon.",
    summary="Get pokemom habita",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokemom habitas",
    )
)
class PokemonHabitatResource(PokeapiCommonViewset):
    queryset = PokemonHabitat.objects.all()
    serializer_class = PokemonHabitatDetailSerializer
    list_serializer_class = PokemonHabitatSummarySerializer


@extend_schema(
    description="Shapes used for sorting Pokémon in a Pokédex.",
    summary="Get pokemon shape",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokemon shapes",
    )
)
class PokemonShapeResource(PokeapiCommonViewset):
    queryset = PokemonShape.objects.all()
    serializer_class = PokemonShapeDetailSerializer
    list_serializer_class = PokemonShapeSummarySerializer


@extend_schema(
    description="Pokémon are the creatures that inhabit the world of the Pokémon games. They can be caught using Pokéballs and trained by battling with other Pokémon. Each Pokémon belongs to a specific species but may take on a variant which makes it differ from other Pokémon of the same species, such as base stats, available abilities and typings. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_(species)) for greater detail.",
    summary="Get pokemon",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokemon",
    ),
)
class PokemonResource(PokeapiCommonViewset):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonDetailSerializer
    list_serializer_class = PokemonSummarySerializer


@extend_schema(
    description="A Pokémon Species forms the basis for at least one Pokémon. Attributes of a Pokémon species are shared across all varieties of Pokémon within the species. A good example is Wormadam; Wormadam is the species which can be found in three different varieties, Wormadam-Trash, Wormadam-Sandy and Wormadam-Plant.",
    summary="Get pokemon species",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List pokemon species",
    )
)
class PokemonSpeciesResource(PokeapiCommonViewset):
    queryset = PokemonSpecies.objects.all().order_by("id")
    serializer_class = PokemonSpeciesDetailSerializer
    list_serializer_class = PokemonSpeciesSummarySerializer


@extend_schema(
    description="A region is an organized area of the Pokémon world. Most often, the main difference between regions is the species of Pokémon that can be encountered within them.",
    summary="Get region",
    tags=["location"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List regions",
    )
)
class RegionResource(PokeapiCommonViewset):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer
    list_serializer_class = RegionSummarySerializer


@extend_schema(
    description="Stats determine certain aspects of battles. Each Pokémon has a value for each stat which grows as they gain levels and can be altered momentarily by effects in battles.",
    summary="Get stat",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List stats",
    )
)
class StatResource(PokeapiCommonViewset):
    queryset = Stat.objects.all()
    serializer_class = StatDetailSerializer
    list_serializer_class = StatSummarySerializer


@extend_schema(
    description="Super contest effects refer to the effects of moves when used in super contests.",
    summary="Get super contest effect",
    tags=["contests"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List super contest effects",
    )
)
class SuperContestEffectResource(PokeapiCommonViewset):
    queryset = SuperContestEffect.objects.all()
    serializer_class = SuperContestEffectDetailSerializer
    list_serializer_class = SuperContestEffectSummarySerializer


@extend_schema(
    description="Types are properties for Pokémon and their moves. Each type has three properties: which types of Pokémon it is super effective against, which types of Pokémon it is not very effective against, and which types of Pokémon it is completely ineffective against.",
    summary="Get types",
    tags=["pokemon"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List types",
    )
)
class TypeResource(PokeapiCommonViewset):
    queryset = Type.objects.all()
    serializer_class = TypeDetailSerializer
    list_serializer_class = TypeSummarySerializer


@extend_schema(
    description="Versions of the games, e.g., Red, Blue or Yellow.",
    summary="Get version",
    tags=["games"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List versions",
    )
)
class VersionResource(PokeapiCommonViewset):
    queryset = Version.objects.all()
    serializer_class = VersionDetailSerializer
    list_serializer_class = VersionSummarySerializer


@extend_schema(
    description="Version groups categorize highly similar versions of the games.",
    summary="Get version group",
    tags=["games"],
)
@extend_schema_view(
    list=extend_schema(
        summary="List version groups",
    )
)
class VersionGroupResource(PokeapiCommonViewset):
    queryset = VersionGroup.objects.all()
    serializer_class = VersionGroupDetailSerializer
    list_serializer_class = VersionGroupSummarySerializer


@extend_schema(
    description="Handles Pokemon Encounters as a sub-resource.",
    summary="Get pokemon encounter",
    tags=["encounters"],
    responses={
        "200": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["location_area", "version_details"],
                "properties": {
                    "location_area": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "example": "cerulean-city-area"},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "example": "https://pokeapi.co/api/v2/location-area/281/",
                            },
                        },
                    },
                    "version_details": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["encounter_details", "max_chance", "version"],
                            "properties": {
                                "encounter_details": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "required": [
                                            "chance",
                                            "condition_values",
                                            "max_level",
                                            "method",
                                            "min_level",
                                        ],
                                        "properties": {
                                            "chance": {
                                                "type": "number",
                                                "example": 100,
                                            },
                                            "condition_values": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "required": ["name", "url"],
                                                    "properties": {
                                                        "name": {
                                                            "type": "string",
                                                            "example": "story-progress-beat-red",
                                                        },
                                                        "url": {
                                                            "type": "string",
                                                            "format": "uri",
                                                            "example": "https://pokeapi.co/api/v2/encounter-condition-value/55/",
                                                        },
                                                    },
                                                },
                                            },
                                            "max_level": {
                                                "type": "number",
                                                "example": 10,
                                            },
                                            "method": {
                                                "type": "object",
                                                "required": ["name", "url"],
                                                "properties": {
                                                    "name": {
                                                        "type": "string",
                                                        "example": "gift",
                                                    },
                                                    "url": {
                                                        "type": "string",
                                                        "format": "uri",
                                                        "example": "https://pokeapi.co/api/v2/encounter-method/18/",
                                                    },
                                                },
                                            },
                                            "min_level": {
                                                "type": "number",
                                                "example": 10,
                                            },
                                        },
                                    },
                                },
                                "max_chance": {"type": "number", "example": 100},
                                "version": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {"type": "string", "example": "red"},
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "example": "https://pokeapi.co/api/v2/version/1/",
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    },
)
class PokemonEncounterView(APIView):
    def get(self, request, pokemon_id):
        self.context = dict(request=request)

        try:
            pokemon = Pokemon.objects.get(pk=pokemon_id)
        except Pokemon.DoesNotExist:
            raise Http404

        encounter_objects = Encounter.objects.filter(pokemon=pokemon)

        area_ids = (
            encounter_objects.order_by("location_area")
            .distinct("location_area")
            .values_list("location_area", flat=True)
        )

        location_area_objects = LocationArea.objects.filter(pk__in=area_ids)
        version_objects = Version.objects

        encounters_list = []

        for area_id in area_ids:
            location_area = location_area_objects.get(pk=area_id)

            area_encounters = encounter_objects.filter(location_area_id=area_id)

            version_ids = (
                area_encounters.order_by("version_id")
                .distinct("version_id")
                .values_list("version_id", flat=True)
            )

            version_details_list = []

            for version_id in version_ids:
                version = version_objects.get(pk=version_id)

                version_encounters = area_encounters.filter(
                    version_id=version_id
                ).order_by("encounter_slot_id")

                encounters_data = EncounterDetailSerializer(
                    version_encounters, many=True, context=self.context
                ).data

                max_chance = 0
                encounter_details_list = []

                for encounter in encounters_data:
                    slot = EncounterSlot.objects.get(pk=encounter["encounter_slot"])
                    slot_data = EncounterSlotSerializer(slot, context=self.context).data

                    del encounter["pokemon"]
                    del encounter["encounter_slot"]
                    del encounter["location_area"]
                    del encounter["version"]
                    encounter["chance"] = slot_data["chance"]
                    max_chance += slot_data["chance"]
                    encounter["method"] = slot_data["encounter_method"]

                    encounter_details_list.append(encounter)

                version_details_list.append(
                    {
                        "version": VersionSummarySerializer(
                            version, context=self.context
                        ).data,
                        "max_chance": max_chance,
                        "encounter_details": encounter_details_list,
                    }
                )

            encounters_list.append(
                {
                    "location_area": LocationAreaSummarySerializer(
                        location_area, context=self.context
                    ).data,
                    "version_details": version_details_list,
                }
            )

        return Response(encounters_list)
