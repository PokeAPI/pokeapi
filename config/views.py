#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

# from pokemon.models import (
#     Pokemon, Sprite, Move, Description, Game,
#     EggGroup, Type, Ability, MovePokemon
# )

from pokemon_v2.models import *

from hits.models import ResourceView


def _total_site_data():

    """
    Compute the total count of objects on the site

    Using count() is drastically cheaper than len(objects.all())
    """

    # v1
    # data = dict(
    #     pokemon=Pokemon.objects.count(),
    #     sprites=Sprite.objects.count(),
    #     moves=Move.objects.count(),
    #     descriptions=Description.objects.count(),
    #     games=Game.objects.count(),
    #     egg_groups=EggGroup.objects.count(),
    #     types=Type.objects.count(),
    #     abilities=Ability.objects.count(),
    #     move_pokes=MovePokemon.objects.count()
    # )
    

    # v2
    data = dict (
        abilities=Ability.objects.count(),
        abilitie_names=AbilityName.objects.count(),
        abilitie_effect_texts=AbilityEffectText.objects.count(),
        abilities_flavor_texts=AbilityFlavorText.objects.count(),
        abilities_changes=AbilityChange.objects.count(),
        abilities_change_effect_texts=AbilityChangeEffectText.objects.count(),

        berries=Berry.objects.count(),
        berry_flavors=BerryFlavor.objects.count(),
        berry_firmnesses=BerryFirmness.objects.count(),
        berry_firmness_names=BerryFirmnessName.objects.count(),

        characteristic=Characteristic.objects.count(),
        characteristic_descriptions=CharacteristicDescription.objects.count(),

        contest_combos=ContestCombo.objects.count(),
        contest_types=ContestType.objects.count(),
        contest_type_names=ContestTypeName.objects.count(),
        contest_effects=ContestEffect.objects.count(),
        contest_effect_texts=ContestEffectEffectText.objects.count(),
        contest_effect_flavor_texts=ContestEffectFlavorText.objects.count(),

        egg_groups=EggGroup.objects.count(),
        egg_group_names=EggGroupName.objects.count(),

        encounter_methods=EncounterMethod.objects.count(),
        encounter_method_names=EncounterMethodName.objects.count(),
        encounter_conditions=EncounterCondition.objects.count(),
        encounter_condition_names=EncounterConditionName.objects.count(),
        encounter_condition_values=EncounterConditionValue.objects.count(),
        encounter_condition_value_names=EncounterConditionValueName.objects.count(),
        encounter_condition_value_maps=EncounterConditionValueMap.objects.count(),
        encounter_slots=EncounterSlot.objects.count(),
        encounters=Encounter.objects.count(),

        evolution_chain=EvolutionChain.objects.count(),
        evolution_trigger=EvolutionTrigger.objects.count(),
        evolution_trigger_names=EvolutionTriggerName.objects.count(),

        experiences=Experience.objects.count(),

        generations=Generation.objects.count(),
        generation_names=GenerationName.objects.count(),
        gender=Gender.objects.count(),

        growth_rate=GrowthRate.objects.count(),
        growth_rate_descriptions=GrowthRateDescription.objects.count(),

        items=Item.objects.count(),
        item_names=ItemName.objects.count(),
        item_effect_texts=ItemEffectText.objects.count(),
        item_categories=ItemCategory.objects.count(),
        item_category_names=ItemCategoryName.objects.count(),

        item_attributes=ItemAttribute.objects.count(),
        item_attribute_maps=ItemAttributeMap.objects.count(),
        item_attribute_descriptions=ItemAttributeDescription.objects.count(),
        item_flavor_texts=ItemFlavorText.objects.count(),

        item_fling_effects=ItemFlingEffect.objects.count(),
        item_fling_effect_effect_texts=ItemFlingEffectEffectText.objects.count(),


        item_pockets=ItemPocket.objects.count(),
        item_pocket_names=ItemPocketName.objects.count(),
        item_game_indexes=ItemGameIndex.objects.count(),

        languages=Language.objects.count(),
        language_names=LanguageName.objects.count(),

        locations=Location.objects.count(),
        location_game_indexes=LocationGameIndex.objects.count(),
        location_names=LocationName.objects.count(),
        location_areas=LocationArea.objects.count(),
        location_area_names=LocationAreaName.objects.count(),
        location_area_encounter_rates=LocationAreaEncounterRate.objects.count(),

        machines=Machine.objects.count(),

        moves=Move.objects.count(),
        move_names=MoveName.objects.count(),
        move_changes=MoveChange.objects.count(),
        move_flavor_text=MoveFlavorText.objects.count(),
        move_effects=MoveEffect.objects.count(),
        move_effect_changes=MoveEffectChange.objects.count(),
        move_effect_change_effect_texts=MoveEffectChangeEffectText.objects.count(),
        move_effect_effect_texts=MoveEffectEffectText.objects.count(),
        move_attributes=MoveAttribute.objects.count(),
        move_attribute_names=MoveAttributeName.objects.count(),
        move_attribute_maps=MoveAttributeMap.objects.count(),
        move_attribute_descriptions=MoveAttributeDescription.objects.count(),
        move_metas=MoveMeta.objects.count(),
        move_ailments=MoveMetaAilment.objects.count(),
        move_ailment_names=MoveMetaAilmentName.objects.count(),
        move_battle_styles=MoveBattleStyle.objects.count(),
        move_battle_style_names=MoveBattleStyleName.objects.count(),
        move_categories=MoveMetaCategory.objects.count(),
        move_damage_classes=MoveDamageClass.objects.count(),
        move_damage_class_descriptions=MoveDamageClassDescription.objects.count(),
        move_learn_methods=MoveLearnMethod.objects.count(),
        move_learn_method_names=MoveLearnMethodName.objects.count(),
        move_targets=MoveTarget.objects.count(),
        move_target_descriptions=MoveTargetDescription.objects.count(),
        move_state_changes=MoveMetaStatChange.objects.count(),

        natures=Nature.objects.count(),
        pal_park_areas=PalParkArea.objects.count(),
        pokedexes=Pokedex.objects.count(),
        pokemon=Pokemon.objects.count(),
        pokemon_colors=PokemonColor.objects.count(),
        pokemon_forms=PokemonForm.objects.count(),
        pokemon_habitats=PokemonHabitat.objects.count(),
        pokemon_shapes=PokemonShape.objects.count(),
        pokemon_species=PokemonSpecies.objects.count(),
        pokeathlon_stats=PokeathlonStat.objects.count(),
        region=Region.objects.count(),
        stat=Stat.objects.count(),
        super_contest_effects=SuperContestEffect.objects.count(),
        types=Type.objects.count(),
        versions=Version.objects.count(),
        version_groups=VersionGroup.objects.count()
    ) 

    t = 0
    for i in data.iteritems():
        t += i[1]

    data['total_items'] = t

    return data


@login_required
def moderate(request):

    return render_to_response(
        'pages/moderate.html',
        {}, context_instance=RequestContext(request))


def about(request):

    site_data = _total_site_data()

    total_views = ResourceView.objects.total_count()

    # average_day = int(round(total_views / ResourceView.objects.count()))
    
    average_day = 0;

    return render_to_response(
        'about.html',
        {
            'total': total_views,
            'average_day': average_day,
            'site_data': site_data,
        },
        context_instance=RequestContext(request)
    )


def home(request):

    total_views = ResourceView.objects.total_count()

    if total_views > 100:
        total_views = int(round(total_views, -2))

    return render_to_response(
        'home.html',
        {
            'total_views': total_views,
        },
        context_instance=RequestContext(request)
    )


def twilio(request):

    return render_to_response(
        'pages/twilio.html',
        {}, context_instance=RequestContext(request))
