import re

from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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
    namePattern = re.compile(r"^[0-9A-Za-z\-\+]+$")

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
            resp = get_object_or_404(queryset, name=lookup)

        else:
            raise Http404

        return resp


class PokeapiCommonViewset(
    ListOrDetailSerialRelation, NameOrIdRetrieval, viewsets.ReadOnlyModelViewSet
):
    pass


##########
#  APIS  #
##########

retrieve_path_parameter = OpenApiParameter(
    name="id",
    description="This parameter can be a string or an integer.",
    location=OpenApiParameter.PATH,
    type=OpenApiTypes.STR,
    required=True,
)


class AbilityResource(PokeapiCommonViewset):
    queryset = Ability.objects.all()
    serializer_class = AbilityDetailSerializer
    list_serializer_class = AbilitySummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class BerryResource(PokeapiCommonViewset):
    queryset = Berry.objects.all()
    serializer_class = BerryDetailSerializer
    list_serializer_class = BerrySummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class BerryFirmnessResource(PokeapiCommonViewset):
    queryset = BerryFirmness.objects.all()
    serializer_class = BerryFirmnessDetailSerializer
    list_serializer_class = BerryFirmnessSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class BerryFlavorResource(PokeapiCommonViewset):
    queryset = BerryFlavor.objects.all()
    serializer_class = BerryFlavorDetailSerializer
    list_serializer_class = BerryFlavorSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class CharacteristicResource(PokeapiCommonViewset):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicDetailSerializer
    list_serializer_class = CharacteristicSummarySerializer


class ContestEffectResource(PokeapiCommonViewset):
    queryset = ContestEffect.objects.all()
    serializer_class = ContestEffectDetailSerializer
    list_serializer_class = ContestEffectSummarySerializer


class ContestTypeResource(PokeapiCommonViewset):
    queryset = ContestType.objects.all()
    serializer_class = ContestTypeDetailSerializer
    list_serializer_class = ContestTypeSummarySerializer


class EggGroupResource(PokeapiCommonViewset):
    queryset = EggGroup.objects.all()
    serializer_class = EggGroupDetailSerializer
    list_serializer_class = EggGroupSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class EncounterConditionResource(PokeapiCommonViewset):
    queryset = EncounterCondition.objects.all()
    serializer_class = EncounterConditionDetailSerializer
    list_serializer_class = EncounterConditionSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class EncounterConditionValueResource(PokeapiCommonViewset):
    queryset = EncounterConditionValue.objects.all()
    serializer_class = EncounterConditionValueDetailSerializer
    list_serializer_class = EncounterConditionValueSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class EncounterMethodResource(PokeapiCommonViewset):
    queryset = EncounterMethod.objects.all()
    serializer_class = EncounterMethodDetailSerializer
    list_serializer_class = EncounterMethodSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class EvolutionChainResource(PokeapiCommonViewset):
    queryset = EvolutionChain.objects.all()
    serializer_class = EvolutionChainDetailSerializer
    list_serializer_class = EvolutionChainSummarySerializer


class EvolutionTriggerResource(PokeapiCommonViewset):
    queryset = EvolutionTrigger.objects.all()
    serializer_class = EvolutionTriggerDetailSerializer
    list_serializer_class = EvolutionTriggerSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class GenerationResource(PokeapiCommonViewset):
    queryset = Generation.objects.all()
    serializer_class = GenerationDetailSerializer
    list_serializer_class = GenerationSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class GenderResource(PokeapiCommonViewset):
    queryset = Gender.objects.all()
    serializer_class = GenderDetailSerializer
    list_serializer_class = GenderSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class GrowthRateResource(PokeapiCommonViewset):
    queryset = GrowthRate.objects.all()
    serializer_class = GrowthRateDetailSerializer
    list_serializer_class = GrowthRateSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ItemResource(PokeapiCommonViewset):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    list_serializer_class = ItemSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ItemCategoryResource(PokeapiCommonViewset):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategoryDetailSerializer
    list_serializer_class = ItemCategorySummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ItemAttributeResource(PokeapiCommonViewset):
    queryset = ItemAttribute.objects.all()
    serializer_class = ItemAttributeDetailSerializer
    list_serializer_class = ItemAttributeSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ItemFlingEffectResource(PokeapiCommonViewset):
    queryset = ItemFlingEffect.objects.all()
    serializer_class = ItemFlingEffectDetailSerializer
    list_serializer_class = ItemFlingEffectSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class ItemPocketResource(PokeapiCommonViewset):
    queryset = ItemPocket.objects.all()
    serializer_class = ItemPocketDetailSerializer
    list_serializer_class = ItemPocketSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class LanguageResource(PokeapiCommonViewset):
    queryset = Language.objects.all()
    serializer_class = LanguageDetailSerializer
    list_serializer_class = LanguageSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class LocationResource(PokeapiCommonViewset):
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer
    list_serializer_class = LocationSummarySerializer


class LocationAreaResource(ListOrDetailSerialRelation, viewsets.ReadOnlyModelViewSet):
    queryset = LocationArea.objects.all()
    serializer_class = LocationAreaDetailSerializer
    list_serializer_class = LocationAreaSummarySerializer


class MachineResource(PokeapiCommonViewset):
    queryset = Machine.objects.all()
    serializer_class = MachineDetailSerializer
    list_serializer_class = MachineSummarySerializer


class MoveResource(PokeapiCommonViewset):
    queryset = Move.objects.all()
    serializer_class = MoveDetailSerializer
    list_serializer_class = MoveSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class MoveDamageClassResource(PokeapiCommonViewset):
    queryset = MoveDamageClass.objects.all()
    serializer_class = MoveDamageClassDetailSerializer
    list_serializer_class = MoveDamageClassSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class MoveMetaAilmentResource(PokeapiCommonViewset):
    queryset = MoveMetaAilment.objects.all()
    serializer_class = MoveMetaAilmentDetailSerializer
    list_serializer_class = MoveMetaAilmentSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class MoveBattleStyleResource(PokeapiCommonViewset):
    queryset = MoveBattleStyle.objects.all()
    serializer_class = MoveBattleStyleDetailSerializer
    list_serializer_class = MoveBattleStyleSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class MoveMetaCategoryResource(PokeapiCommonViewset):
    queryset = MoveMetaCategory.objects.all()
    serializer_class = MoveMetaCategoryDetailSerializer
    list_serializer_class = MoveMetaCategorySummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class MoveLearnMethodResource(PokeapiCommonViewset):
    queryset = MoveLearnMethod.objects.all()
    serializer_class = MoveLearnMethodDetailSerializer
    list_serializer_class = MoveLearnMethodSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class MoveTargetResource(PokeapiCommonViewset):
    queryset = MoveTarget.objects.all()
    serializer_class = MoveTargetDetailSerializer
    list_serializer_class = MoveTargetSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class NatureResource(PokeapiCommonViewset):
    queryset = Nature.objects.all()
    serializer_class = NatureDetailSerializer
    list_serializer_class = NatureSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PalParkAreaResource(PokeapiCommonViewset):
    queryset = PalParkArea.objects.all()
    serializer_class = PalParkAreaDetailSerializer
    list_serializer_class = PalParkAreaSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokeathlonStatResource(PokeapiCommonViewset):
    queryset = PokeathlonStat.objects.all()
    serializer_class = PokeathlonStatDetailSerializer
    list_serializer_class = PokeathlonStatSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokedexResource(PokeapiCommonViewset):
    queryset = Pokedex.objects.all()
    serializer_class = PokedexDetailSerializer
    list_serializer_class = PokedexSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonColorResource(PokeapiCommonViewset):
    queryset = PokemonColor.objects.all()
    serializer_class = PokemonColorDetailSerializer
    list_serializer_class = PokemonColorSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonFormResource(PokeapiCommonViewset):
    queryset = PokemonForm.objects.all()
    serializer_class = PokemonFormDetailSerializer
    list_serializer_class = PokemonFormSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonHabitatResource(PokeapiCommonViewset):
    queryset = PokemonHabitat.objects.all()
    serializer_class = PokemonHabitatDetailSerializer
    list_serializer_class = PokemonHabitatSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonShapeResource(PokeapiCommonViewset):
    queryset = PokemonShape.objects.all()
    serializer_class = PokemonShapeDetailSerializer
    list_serializer_class = PokemonShapeSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonResource(PokeapiCommonViewset):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonDetailSerializer
    list_serializer_class = PokemonSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonSpeciesResource(PokeapiCommonViewset):
    queryset = PokemonSpecies.objects.all().order_by("id")
    serializer_class = PokemonSpeciesDetailSerializer
    list_serializer_class = PokemonSpeciesSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class RegionResource(PokeapiCommonViewset):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer
    list_serializer_class = RegionSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class StatResource(PokeapiCommonViewset):
    queryset = Stat.objects.all()
    serializer_class = StatDetailSerializer
    list_serializer_class = StatSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class SuperContestEffectResource(PokeapiCommonViewset):
    queryset = SuperContestEffect.objects.all()
    serializer_class = SuperContestEffectDetailSerializer
    list_serializer_class = SuperContestEffectSummarySerializer


class TypeResource(PokeapiCommonViewset):
    queryset = Type.objects.all()
    serializer_class = TypeDetailSerializer
    list_serializer_class = TypeSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class VersionResource(PokeapiCommonViewset):
    queryset = Version.objects.all()
    serializer_class = VersionDetailSerializer
    list_serializer_class = VersionSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class VersionGroupResource(PokeapiCommonViewset):
    queryset = VersionGroup.objects.all()
    serializer_class = VersionGroupDetailSerializer
    list_serializer_class = VersionGroupSummarySerializer

    @extend_schema(parameters=[retrieve_path_parameter])
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class PokemonEncounterView(APIView):
    """
    Handles Pokemon Encounters as a sub-resource.
    """

    @extend_schema(
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "location_area": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "url": {"type": "string"},
                            },
                        },
                        "version_details": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "version": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "url": {"type": "string"},
                                        },
                                    },
                                    "max_chance": {"type": "integer"},
                                    "encounter_details": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "min_level": {"type": "integer"},
                                                "max_level": {"type": "integer"},
                                                "condition_values": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "name": {"type": "string"},
                                                            "url": {"type": "string"},
                                                        },
                                                    },
                                                },
                                                "chance": {"type": "integer"},
                                                "method": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {"type": "string"},
                                                        "url": {"type": "string"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
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
