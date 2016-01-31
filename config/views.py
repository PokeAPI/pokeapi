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
    

    # v2 Sorry for the brute force. Theres probably a better way to do this.
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
        characteristics=Characteristic.objects.count(),
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
        evolution_chains=EvolutionChain.objects.count(),
        evolution_triggers=EvolutionTrigger.objects.count(),
        evolution_trigger_names=EvolutionTriggerName.objects.count(),
        experiences=Experience.objects.count(),
        generations=Generation.objects.count(),
        generation_names=GenerationName.objects.count(),
        genders=Gender.objects.count(),
        growth_rates=GrowthRate.objects.count(),
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
        nature_names=NatureName.objects.count(),
        nature_pokeathlon_stats=NaturePokeathlonStat.objects.count(),
        nature_battle_style_preference=NatureBattleStylePreference.objects.count(),
        pal_park_areas=PalParkArea.objects.count(),
        pal_park_area_names=PalParkAreaName.objects.count(),
        pal_parks=PalPark.objects.count(),
        pokeathlon_stat_names=PokeathlonStatName.objects.count(),
        pokeathlon_stats=PokeathlonStat.objects.count(),
        pokedexes=PokedexVersionGroup.objects.count(),
        pokedex_descriptions=PokedexDescription.objects.count(),
        pokedex_version_groups=PokedexVersionGroup.objects.count(),
        pokemon=Pokemon.objects.count(),
        pokemon_abilities=PokemonAbility.objects.count(),
        pokemon_colors=PokemonColor.objects.count(),
        pokemon_names=PokemonColorName.objects.count(),
        pokemon_dex_numbers=PokemonDexNumber.objects.count(),
        pokemon_egg_groups=PokemonEggGroup.objects.count(),
        pokemon_evolutions=PokemonEvolution.objects.count(),
        pokemon_forms=PokemonForm.objects.count(),
        pokemon_form_names=PokemonFormName.objects.count(),
        pokemon_form_generations=PokemonFormGeneration.objects.count(),
        pokemon_game_indices=PokemonGameIndex.objects.count(),
        pokemon_habitats=PokemonHabitat.objects.count(),
        pokemon_habitat_names=PokemonHabitatName.objects.count(),
        pokemon_items=PokemonItem.objects.count(),
        pokemon_moves=PokemonMove.objects.count(),
        pokemon_shapes=PokemonShape.objects.count(),
        pokemon_shape_names=PokemonShapeName.objects.count(),
        pokemon_species=PokemonSpecies.objects.count(),
        pokemon_species_names=PokemonSpeciesName.objects.count(),
        pokemon_descriptions=PokemonSpeciesDescription.objects.count(),
        pokemon_flavor_texts=PokemonSpeciesFlavorText.objects.count(),
        pokemon_stat=PokemonStat.objects.count(),
        pokemon_type=PokemonType.objects.count(),
        regions=Region.objects.count(),
        region_names=RegionName.objects.count(),
        stats=Stat.objects.count(),
        stat_names=StatName.objects.count(),
        super_contest_effects=SuperContestEffect.objects.count(),
        super_contest_combos=SuperContestCombo.objects.count(),
        super_contest_effect_flavor_texts=SuperContestEffectFlavorText.objects.count(),
        types=Type.objects.count(),
        type_names=TypeName.objects.count(),
        type_game_indices=TypeGameIndex.objects.count(),
        type_efficacy=TypeEfficacy.objects.count(),
        versions=Version.objects.count(),
        version_names=VersionName.objects.count(),
        version_groups=VersionGroup.objects.count(),
        version_group_move_learn_methods=VersionGroupMoveLearnMethod.objects.count(),
        version_group_regions=VersionGroupRegion.objects.count(),
    ) 

    lines = 0
    for i in data.iteritems():
        lines += i[1]

    resources = 0
    resources += data['abilities'];
    resources += data['berries'];
    resources += data['berry_flavors'];
    resources += data['berry_firmnesses'];
    resources += data['characteristics'];
    resources += data['contest_types'];
    resources += data['contest_effects'];
    resources += data['egg_groups'];
    resources += data['encounter_methods'];
    resources += data['encounter_conditions'];
    resources += data['encounter_condition_values'];
    resources += data['evolution_chains'];
    resources += data['evolution_triggers'];
    resources += data['generations'];
    resources += data['genders'];
    resources += data['growth_rates'];
    resources += data['items'];
    resources += data['item_attributes'];
    resources += data['item_categories'];
    resources += data['item_fling_effects'];
    resources += data['item_pockets'];
    resources += data['languages'];
    resources += data['locations'];
    resources += data['location_areas'];
    resources += data['moves'];
    resources += data['move_ailments'];
    resources += data['move_categories'];
    resources += data['move_battle_styles'];
    resources += data['move_damage_classes'];
    resources += data['move_learn_methods'];
    resources += data['move_targets'];
    resources += data['natures'];
    resources += data['pal_park_areas'];
    resources += data['pokedexes'];
    resources += data['pokemon'];
    resources += data['pokemon_colors'];
    resources += data['pokemon_forms'];
    resources += data['pokemon_habitats'];
    resources += data['pokemon_shapes'];
    resources += data['pokemon_species'];
    resources += data['pokeathlon_stats'];
    resources += data['regions'];
    resources += data['stats'];
    resources += data['super_contest_effects'];
    resources += data['types'];
    resources += data['versions'];
    resources += data['version_groups'];


    data['total_lines'] = lines
    data['total_resources'] = resources

    return data


def about(request):

    site_data = _total_site_data()

    total_views = ResourceView.objects.total_count()
    total_v1_views = ResourceView.objects.total_count(version=1)
    total_v2_views = ResourceView.objects.total_count(version=2)

    average_day = int(round(total_views / ResourceView.objects.count()))

    return render_to_response(
        'pages/about.html',
        {
            'total': total_views,
            'total_v1': total_v1_views,
            'total_v2': total_v2_views,
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
        'pages/home.html',
        {
            'total_views': total_views,
        },
        context_instance=RequestContext(request)
    )
