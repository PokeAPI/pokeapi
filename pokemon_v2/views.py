
from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
import re


###########################
#  BEHAVOIR ABSTRACTIONS  #
###########################

class ListOrDetailSerialRelation():
    """
    Mixin to allow association with separate serializers
    for list or detail view.
    """

    list_serializer_class = None

    def get_serializer_class(self):
        if (self.action == 'list' and self.list_serializer_class != None):
            return self.list_serializer_class
        return self.serializer_class


class NameOrIdRetrieval():
    """
    Mixin to allow retrieval of resources by 
    pk (in this case ID) or by name
    """

    idPattern = re.compile("^[0-9]+$")
    namePattern = re.compile("^[0-9A-Za-z\-]+$")

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        lookup =  self.kwargs['pk']

        if self.idPattern.match(lookup):
            resp = get_object_or_404(queryset, pk=lookup)

        elif self.namePattern.match(lookup):
            resp = get_object_or_404(queryset, name=lookup)

        else:
            resp = get_object_or_404(queryset, pk="")
        
        return resp


class PokeapiCommonViewset(ListOrDetailSerialRelation, NameOrIdRetrieval, viewsets.ReadOnlyModelViewSet):
    pass


##########
#  APIS  #
##########

class AbilityResource(PokeapiCommonViewset):

    queryset = Ability.objects.all()
    serializer_class = AbilityDetailSerializer
    list_serializer_class = AbilitySummarySerializer


class BerryResource(PokeapiCommonViewset):

    queryset = Berry.objects.all()
    serializer_class = BerryDetailSerializer
    list_serializer_class = BerrySummarySerializer


class BerryFirmnessResource(PokeapiCommonViewset):

    queryset = BerryFirmness.objects.all()
    serializer_class = BerryFirmnessDetailSerializer
    list_serializer_class = BerryFirmnessSummarySerializer

class BerryFlavorResource(PokeapiCommonViewset):

    queryset = BerryFlavor.objects.all()
    serializer_class = BerryFlavorDetailSerializer
    list_serializer_class = BerryFlavorSummarySerializer


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


class EncounterConditionResource(PokeapiCommonViewset):

    queryset = EncounterCondition.objects.all()
    serializer_class = EncounterConditionDetailSerializer
    list_serializer_class = EncounterConditionSummarySerializer


class EncounterConditionValueResource(PokeapiCommonViewset):

    queryset = EncounterConditionValue.objects.all()
    serializer_class = EncounterConditionValueDetailSerializer
    list_serializer_class = EncounterConditionValueSummarySerializer


class EncounterMethodResource(PokeapiCommonViewset):

    queryset = EncounterMethod.objects.all()
    serializer_class = EncounterMethodDetailSerializer
    list_serializer_class = EncounterMethodSummarySerializer


class EvolutionChainResource(PokeapiCommonViewset):

    queryset = EvolutionChain.objects.all()
    serializer_class = EvolutionChainDetailSerializer
    list_serializer_class = EvolutionChainSummarySerializer


class EvolutionTriggerResource(PokeapiCommonViewset):

    queryset = EvolutionTrigger.objects.all()
    serializer_class = EvolutionTriggerDetailSerializer
    list_serializer_class = EvolutionTriggerSummarySerializer


class GenerationResource(PokeapiCommonViewset):

    queryset = Generation.objects.all()
    serializer_class = GenerationDetailSerializer
    list_serializer_class = GenerationSummarySerializer


class GenderResource(PokeapiCommonViewset):

    queryset = Gender.objects.all()
    serializer_class = GenderDetailSerializer
    list_serializer_class = GenderSummarySerializer


class GrowthRateResource(PokeapiCommonViewset):

    queryset = GrowthRate.objects.all()
    serializer_class = GrowthRateDetailSerializer
    list_serializer_class = GrowthRateSummarySerializer


class ItemResource(PokeapiCommonViewset):

    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    list_serializer_class = ItemSummarySerializer


class ItemCategoryResource(PokeapiCommonViewset):

    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategoryDetailSerializer
    list_serializer_class = ItemCategorySummarySerializer


class ItemAttributeResource(PokeapiCommonViewset):

    queryset = ItemAttribute.objects.all()
    serializer_class = ItemAttributeDetailSerializer
    list_serializer_class = ItemAttributeSummarySerializer


class ItemFlingEffectResource(PokeapiCommonViewset):

    queryset = ItemFlingEffect.objects.all()
    serializer_class = ItemFlingEffectDetailSerializer
    list_serializer_class = ItemFlingEffectSummarySerializer


class ItemPocketResource(PokeapiCommonViewset):

    queryset = ItemPocket.objects.all()
    serializer_class = ItemPocketDetailSerializer
    list_serializer_class = ItemPocketSummarySerializer


class LanguageResource(PokeapiCommonViewset):

    queryset = Language.objects.all()
    serializer_class = LanguageDetailSerializer
    list_serializer_class = LanguageSummarySerializer


class LocationResource(PokeapiCommonViewset):

    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer
    list_serializer_class = LocationSummarySerializer


class LocationAreaResource(ListOrDetailSerialRelation, viewsets.ReadOnlyModelViewSet):

    queryset = LocationArea.objects.all()
    serializer_class = LocationAreaDetailSerializer
    list_serializer_class = LocationAreaSummarySerializer


# class MachineResource(PokeapiCommonViewset):

#     queryset = Machine.objects.all()
#     serializer_class = MachineDetailSerializer
#     list_serializer_class = MachineSummarySerializer


class MoveResource(PokeapiCommonViewset):

    queryset = Move.objects.all()
    serializer_class = MoveDetailSerializer
    list_serializer_class = MoveSummarySerializer


class MoveDamageClassResource(PokeapiCommonViewset):

    queryset = MoveDamageClass.objects.all()
    serializer_class = MoveDamageClassDetailSerializer
    list_serializer_class = MoveDamageClassSummarySerializer


class MoveMetaAilmentResource(PokeapiCommonViewset):

    queryset = MoveMetaAilment.objects.all()
    serializer_class = MoveMetaAilmentDetailSerializer
    list_serializer_class = MoveMetaAilmentSummarySerializer


class MoveBattleStyleResource(PokeapiCommonViewset):

    queryset = MoveBattleStyle.objects.all()
    serializer_class = MoveBattleStyleDetailSerializer
    list_serializer_class = MoveBattleStyleSummarySerializer


class MoveMetaCategoryResource(PokeapiCommonViewset):

    queryset = MoveMetaCategory.objects.all()
    serializer_class = MoveMetaCategoryDetailSerializer
    list_serializer_class = MoveMetaCategorySummarySerializer


class MoveLearnMethodResource(PokeapiCommonViewset):

    queryset = MoveLearnMethod.objects.all()
    serializer_class = MoveLearnMethodDetailSerializer
    list_serializer_class = MoveLearnMethodSummarySerializer


class MoveTargetResource(PokeapiCommonViewset):

    queryset = MoveTarget.objects.all()
    serializer_class = MoveTargetDetailSerializer
    list_serializer_class = MoveTargetSummarySerializer


class NatureResource(PokeapiCommonViewset):

    queryset = Nature.objects.all()
    serializer_class = NatureDetailSerializer
    list_serializer_class = NatureSummarySerializer


class PalParkAreaResource(PokeapiCommonViewset):

    queryset = PalParkArea.objects.all()
    serializer_class = PalParkAreaDetailSerializer
    list_serializer_class = PalParkAreaSummarySerializer


class PokeathlonStatResource(PokeapiCommonViewset):

    queryset = PokeathlonStat.objects.all()
    serializer_class = PokeathlonStatDetailSerializer
    list_serializer_class = PokeathlonStatSummarySerializer


class PokedexResource(PokeapiCommonViewset):

    queryset = Pokedex.objects.all()
    serializer_class = PokedexDetailSerializer
    list_serializer_class = PokedexSummarySerializer


class PokemonColorResource(PokeapiCommonViewset):

    queryset = PokemonColor.objects.all()
    serializer_class = PokemonColorDetailSerializer
    list_serializer_class = PokemonColorSummarySerializer


class PokemonFormResource(PokeapiCommonViewset):

    queryset = PokemonForm.objects.all()
    serializer_class = PokemonFormDetailSerializer
    list_serializer_class = PokemonFormSummarySerializer


class PokemonHabitatResource(PokeapiCommonViewset):

    queryset = PokemonHabitat.objects.all()
    serializer_class = PokemonHabitatDetailSerializer
    list_serializer_class = PokemonHabitatSummarySerializer


class PokemonShapeResource(PokeapiCommonViewset):

    queryset = PokemonShape.objects.all()
    serializer_class = PokemonShapeDetailSerializer
    list_serializer_class = PokemonShapeSummarySerializer


class PokemonResource(PokeapiCommonViewset):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonDetailSerializer
    list_serializer_class =PokemonSummarySerializer


class PokemonSpeciesResource(PokeapiCommonViewset):

    queryset = PokemonSpecies.objects.all().order_by('id')
    serializer_class = PokemonSpeciesDetailSerializer
    list_serializer_class = PokemonSpeciesSummarySerializer


class RegionResource(PokeapiCommonViewset):

    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer
    list_serializer_class = RegionSummarySerializer


class StatResource(PokeapiCommonViewset):

    queryset = Stat.objects.all()
    serializer_class = StatDetailSerializer
    list_serializer_class = StatSummarySerializer


class SuperContestEffectResource(PokeapiCommonViewset):

    queryset = SuperContestEffect.objects.all()
    serializer_class = SuperContestEffectDetailSerializer
    list_serializer_class = SuperContestEffectSummarySerializer


class TypeResource(PokeapiCommonViewset):

    queryset = Type.objects.all()
    serializer_class = TypeDetailSerializer
    list_serializer_class = TypeSummarySerializer


class VersionResource(PokeapiCommonViewset):

    queryset = Version.objects.all()
    serializer_class = VersionDetailSerializer
    list_serializer_class = VersionSummarySerializer


class VersionGroupResource(PokeapiCommonViewset):

    queryset = VersionGroup.objects.all()
    serializer_class = VersionGroupDetailSerializer
    list_serializer_class = VersionGroupSummarySerializer
