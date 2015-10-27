from __future__ import unicode_literals
# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from pokemon_v2.models import *

test_host = 'http://testserver'
api_v2 = '/api/v2'


"""
Data Initializers
"""

class LanguageData():

    @classmethod
    def setup_language_data(self, name='lang'):

        language = Language.objects.create (
            iso639 = 'ts',
            iso3166 = 'tt',
            name = name,
            official = True,
            order = 1,
        )
        language.save()

        return language

    @classmethod
    def setup_language_name_data(self, language, name='lang nm'):

        local_language = self.setup_language_data(
            name='lang for '+name)

        language_name = LanguageName.objects.create (
            language = language,
            local_language = local_language,
            name = name
        )
        language_name.save()

        return language_name


class RegionData(LanguageData):

    @classmethod
    def setup_region_data(self, name='reg'):

        region = Region.objects.create (
            name = name
        )
        region.save()

        return region

    @classmethod
    def setup_region_name_data(self, region, name='reg nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        region_name = RegionName.objects.create (
            region = region,
            language = language,
            name = name
        )
        region_name.save()

        return region_name


class GenerationData(RegionData, LanguageData):

    @classmethod
    def setup_generation_data(self, name='gen'):

        region = self.setup_region_data(
            name='reg for '+name)

        generation = Generation.objects.create (
            region = region,
            name = name
        )
        generation.save()

        return generation

    @classmethod
    def setup_generation_name_data(self, generation, name='gen nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        generation_name = GenerationName.objects.create (
            generation = generation,
            language = language,
            name = name
        )
        generation_name.save()

        return generation_name


class VersionData(GenerationData, LanguageData):

    @classmethod
    def setup_version_group_data(self, name='ver grp'):

        generation = self.setup_generation_data(
            name='gen for '+name)

        version_group = VersionGroup.objects.create (
            name = name,
            generation = generation,
            order = 1
        )
        version_group.save()

        return version_group

    @classmethod
    def setup_version_data(self, name='ver'):

        version_group = self.setup_version_group_data(
            name='ver grp for '+name)

        version = Version.objects.create (
            name = name,
            version_group = version_group,
        )
        version.save()

        return version

    @classmethod
    def setup_version_name_data(self, version, name='ver nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        version_name = VersionName.objects.create (
            version = version,
            language = language,
            name = name
        )
        version_name.save()

        return version_name


class AbilityData(GenerationData, VersionData):

    @classmethod
    def setup_ability_data(self, name='ablty'):

        generation = self.setup_generation_data(
            name='gen for '+name)

        ability = Ability.objects.create (
            name = name,
            generation = generation,
            is_main_series = False
        )
        ability.save()

        return ability

    @classmethod
    def setup_ability_name_data(self, ability, name='ablty nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        ability_name = AbilityName.objects.create (
            ability = ability,
            language = language,
            name = name
        )
        ability_name.save()

        return ability_name

    @classmethod
    def setup_ability_effect_text_data(self, ability, short_effect='ablty shrt efct', effect='ablty efct'):

        language = self.setup_language_data(
            name='lang for '+effect)

        ability_effect_text = AbilityEffectText.objects.create (
            ability = ability,
            language = language,
            short_effect = short_effect,
            effect = effect
        )
        ability_effect_text.save()

        return ability_effect_text

    @classmethod
    def setup_ability_flavor_text_data(self, ability, flavor_text='ablty flvr txt'):

        version_group = self.setup_version_group_data(
            name='ver grp for '+flavor_text)

        language = self.setup_language_data(
            name='lang for '+flavor_text)

        ability_flavor_text = AbilityFlavorText.objects.create (
            ability = ability,
            version_group = version_group,
            language = language,
            flavor_text = flavor_text
        )
        ability_flavor_text.save()

        return ability_flavor_text


class ItemData(VersionData):

    @classmethod
    def setup_item_attribute_data(self, name="itm attr"):

        item_attribute = ItemAttribute.objects.create (
            name = name,
        )
        item_attribute.save()

        return item_attribute

    def setup_item_attribute_name_data(self, item_attribute, name='itm attr nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        item_attribute_name = ItemAttributeName.objects.create (
            item_attribute = item_attribute,
            name = name,
            language = language
        )
        item_attribute_name.save()

        return item_attribute_name


    def setup_item_attribute_description_data(self, item_attribute, description='itm attr desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        item_attribute_description = ItemAttributeDescription.objects.create (
            item_attribute = item_attribute,
            description = description,
            language = language
        )
        item_attribute_description.save()

        return item_attribute_description

    @classmethod
    def setup_item_fling_effect_data(self, name="itm flng efct"):

        item_fling_effect = ItemFlingEffect.objects.create (
            name = name,
        )
        item_fling_effect.save()

        return item_fling_effect

    def setup_item_fling_effect_description_data(self, item_fling_effect, description='itm flng efct desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        item_fling_effect_description = ItemFlingEffectDescription.objects.create (
            item_fling_effect = item_fling_effect,
            description = description,
            language = language
        )
        item_fling_effect_description.save()

        return item_fling_effect_description

    @classmethod
    def setup_item_pocket_data(self, name='itm pkt'):

        item_pocket = ItemPocket.objects.create (
            name = name,
        )
        item_pocket.save()

        return item_pocket

    @classmethod
    def setup_item_pocket_name_data(self, item_pocket, name='itm pkt nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        item_pocket_name = ItemPocketName.objects.create (
            item_pocket = item_pocket,
            name = name,
            language = language
        )
        item_pocket_name.save()

        return item_pocket_name

    @classmethod
    def setup_item_category_data(self, name="itm ctgry"):

        item_pocket = self.setup_item_pocket_data(
            name='itm pkt for '+name)

        item_category = ItemCategory.objects.create (
            name = name,
            item_pocket = item_pocket
        )
        item_category.save()

        return item_category

    def setup_item_category_name_data(self, item_category, name='itm ctgry nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        item_category_name = ItemCategoryName.objects.create (
            item_category = item_category,
            name = name,
            language = language
        )
        item_category_name.save()

        return item_category_name

    @classmethod
    def setup_item_data(self, item_category=None, item_fling_effect=None, name='itm', cost=100, fling_power=100):

        item = Item.objects.create (
            name = name,
            item_category = item_category,
            cost = 300,
            fling_power = 100,
            item_fling_effect = item_fling_effect
        )
        item.save()

        return item

    @classmethod
    def setup_item_name_data(self, item, name='itm nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        item_name = ItemName.objects.create (
            item = item,
            name = name,
            language = language
        )
        item_name.save()

        return item_name

    @classmethod
    def setup_item_effect_text_data(self, item, short_effect='ablty shrt efct', effect='ablty efct'):

        language = self.setup_language_data(
            name='lang for '+effect)

        item_effect_text = ItemEffectText.objects.create (
            item = item,
            language = language,
            short_effect = short_effect,
            effect = effect
        )
        item_effect_text.save()

        return item_effect_text

    @classmethod
    def setup_item_flavor_text_data(self, item, flavor_text='itm flvr txt'):

        version_group = self.setup_version_group_data(
            name='ver grp for '+flavor_text)

        language = self.setup_language_data(
            name='lang for '+flavor_text)

        item_flavor_text = ItemFlavorText.objects.create (
            item = item,
            version_group = version_group,
            language = language,
            flavor_text = flavor_text
        )
        item_flavor_text.save()

        return item_flavor_text


class BerryData(ItemData, LanguageData):

    @classmethod
    def setup_berry_firmness_data(self, name='bry frmns'):

        berry_firmness = BerryFirmness.objects.create (
            name = name,
        )
        berry_firmness.save()

        return berry_firmness

    @classmethod
    def setup_berry_firmness_name_data(self, berry_firmness, name='bry frmns nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        berry_firmness_name = BerryFirmnessName.objects.create (
            language = language,
            name = name,
            berry_firmness = berry_firmness
        )
        berry_firmness_name.save()

        return berry_firmness_name

    # NEEDS NATURE

    @classmethod
    def setup_berry_data(self, nature=None, name='bry', natural_gift_power=50, size=20, max_harvest=5, growth_time=2, soil_dryness=15, smoothness=25):

        item = self.setup_item_data(
            name='itm for '+name)

        berry_firmness = self.setup_berry_firmness_data(
            name='bry frmns for '+name)

        berry = Berry.objects.create (
            name = name,
            item = item,
            berry_firmness = berry_firmness,
            natural_gift_power = natural_gift_power,
            nature = nature,
            size = size,
            max_harvest = max_harvest,
            growth_time = growth_time,
            soil_dryness = soil_dryness,
            smoothness = smoothness
        )
        berry.save()

        return berry


class EggGroupData(LanguageData):

    @classmethod
    def setup_egg_group_data(self, name='egg grp'):

        egg_group = EggGroup.objects.create (
            name = name,
        )
        egg_group.save()

        return egg_group

    @classmethod
    def setup_egg_group_name_data(self, egg_group, name='ntr nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        egg_group_name = EggGroupName.objects.create (
            egg_group = egg_group,
            language = language,
            name = name
        )
        egg_group_name.save()

        return egg_group_name


class GrowthRateData(LanguageData):

    @classmethod
    def setup_growth_rate_data(self, name='grth rt', formula="pie*1000"):

        growth_rate = GrowthRate (
            name = name,
            formula = formula
        )
        growth_rate.save()

        return growth_rate

    def setup_growth_rate_description_data(self, growth_rate, description='grth rt desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        growth_rate_description = GrowthRateDescription.objects.create (
            growth_rate = growth_rate,
            description = description,
            language = language
        )
        growth_rate_description.save()

        return growth_rate_description


class LocationData(RegionData, LanguageData):

    @classmethod
    def setup_location_data(self, name='lctn'):

        region = self.setup_region_data(
            name='rgn for '+name)

        location = Location (
            name = name,
            region = region
        )
        location.save()

        return location

    @classmethod
    def setup_location_name_data(self, location, name='lctn nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        location_name = LocationName.objects.create (
            language = language,
            name = name,
            location = location
        )
        location_name.save()

        return location_name


class TypeData(GenerationData, LanguageData):

    @classmethod
    def setup_type_data(self, name='tp'):

        # NEEDS MOVE DAMAGE CLASS

        generation = self.setup_generation_data(
            name='rgn for '+name)

        type = Type (
            name = name,
            generation = generation,
            move_damage_class = None
        )
        type.save()

        return type

    @classmethod
    def setup_type_name_data(self, type, name='tp nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        type_name = TypeName.objects.create (
            language = language,
            name = name,
            type = type
        )
        type_name.save()

        return type_name


class MoveData(GenerationData, TypeData, LanguageData):

    @classmethod
    def setup_move_ailment_data(self, name='mv almnt'):

        move_ailment = MoveMetaAilment.objects.create (
            name = name
        )
        move_ailment.save()

        return move_ailment

    @classmethod
    def setup_move_ailment_name_data(self, move_ailment, name='mv almnt nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        move_ailment_name = MoveMetaAilmentName.objects.create (
            move_meta_ailment = move_ailment,
            language = language,
            name = name
        )
        move_ailment_name.save()

        return move_ailment_name

    @classmethod
    def setup_move_category_data(self, name='mv ctgry'):

        move_category = MoveMetaCategory.objects.create (
            name = name
        )
        move_category.save()

        return move_category

    @classmethod
    def setup_move_category_description_data(self, move_category, description='mv ctgry desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        move_category_description = MoveMetaCategoryDescription.objects.create (
            move_meta_category = move_category,
            language = language,
            description = description
        )
        move_category_description.save()

        return move_category_description

    @classmethod
    def setup_move_damage_class_data(self, name='mv dmg cls'):

        move_damage_class = MoveDamageClass.objects.create (
            name = name
        )
        move_damage_class.save()

        return move_damage_class

    @classmethod
    def setup_move_damage_class_name_data(self, move_damage_class, name='mv dmg cls nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        move_damage_class_name = MoveDamageClassName.objects.create (
            move_damage_class = move_damage_class,
            language = language,
            name = name
        )
        move_damage_class_name.save()

        return move_damage_class_name

    @classmethod
    def setup_move_damage_class_description_data(self, move_damage_class, description='mv dmg cls desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        move_damage_class_description = MoveDamageClassDescription.objects.create (
            move_damage_class = move_damage_class,
            language = language,
            description = description
        )
        move_damage_class_description.save()

        return move_damage_class_description

    @classmethod
    def setup_move_learn_method_data(self, name='mv lrn mthd'):

        move_learn_method = MoveLearnMethod.objects.create (
            name = name
        )
        move_learn_method.save()

        return move_learn_method

    @classmethod
    def setup_move_learn_method_name_data(self, move_learn_method, name='mv lrn mthd nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        move_learn_method_name = MoveLearnMethodName.objects.create (
            move_learn_method = move_learn_method,
            language = language,
            name = name
        )
        move_learn_method_name.save()

        return move_learn_method_name

    @classmethod
    def setup_move_learn_method_description_data(self, move_learn_method, description='mv lrn mthd desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        move_learn_method_description = MoveLearnMethodDescription.objects.create (
            move_learn_method = move_learn_method,
            language = language,
            description = description
        )
        move_learn_method_description.save()

        return move_learn_method_description

    @classmethod
    def setup_move_target_data(self, name='mv trgt'):

        move_target = MoveTarget.objects.create (
            name = name
        )
        move_target.save()

        return move_target

    @classmethod
    def setup_move_target_name_data(self, move_target, name='mv trgt nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        move_target_name = MoveTargetName.objects.create (
            move_target = move_target,
            language = language,
            name = name
        )
        move_target_name.save()

        return move_target_name

    @classmethod
    def setup_move_target_description_data(self, move_target, description='mv trgt desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        move_target_description = MoveTargetDescription.objects.create (
            move_target = move_target,
            language = language,
            description = description
        )
        move_target_description.save()

        return move_target_description

    @classmethod
    def setup_move_data(self, name='mv', power=20, pp=20, accuracy=80, priority=0, effect_chance=50):

        # NEED TO REVISIT WHEN MOVE EFFECTS ARE DONE
        # ALSO CONTEST TYPES/EFFECTS

        generation = self.setup_generation_data(
            name='gen for '+name)

        type = self.setup_type_data(
            name='tp for '+name)

        move_target = self.setup_move_target_data(
            name='mv trgt for '+name)

        move_damage_class = self.setup_move_damage_class_data(
            name='mv dmg cls for '+name)

        move = Move.objects.create (
            name = name,
            generation = generation,
            type = type,
            power = power,
            pp = pp,
            accuracy = accuracy,
            priority = priority,
            move_target = move_target,
            move_damage_class = move_damage_class,
            move_effect = None,
            move_effect_chance = effect_chance,
            contest_type_id = None,
            contest_effect_id = None,
            super_contest_effect_id = None
        )
        move.save()

        return move

    @classmethod
    def setup_move_name_data(self, move, name='mv nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        move_name = MoveName.objects.create (
            move = move,
            language = language,
            name = name
        )
        move_name.save()

        return move_name

    @classmethod
    def setup_move_meta_data(self, move, min_hits=1, max_hits=1, min_turns=1, max_turns=1, drain=0, healing=0, crit_rate=0, ailment_chance=0, flinch_chance=0, stat_chance=0):

        move_ailment = self.setup_move_ailment_data()

        move_category = self.setup_move_category_data()

        move_meta = MoveMeta (
            move = move,
            move_meta_category = move_category,
            move_meta_ailment = move_ailment,
            min_hits = min_hits,
            max_hits = max_hits,
            min_turns = min_turns,
            max_turns = max_turns,
            drain = drain,
            healing = healing,
            crit_rate = crit_rate,
            ailment_chance = ailment_chance,
            flinch_chance = flinch_chance,
            stat_chance = stat_chance
          )
        move_meta.save()

        return move_meta



class StatData(MoveData, LanguageData):

    @classmethod
    def setup_stat_data(self, name='stt', is_battle_only=True, game_index=1):

        move_damage_class = self.setup_move_damage_class_data(
            name='mv dmg cls for '+name)

        stat = Stat.objects.create (
            name = name,
            is_battle_only = is_battle_only,
            move_damage_class = move_damage_class,
            game_index = game_index
        )
        stat.save()

        return stat

    @classmethod
    def setup_stat_name_data(self, stat, name='stt nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        stat_name = StatName.objects.create (
            stat = stat,
            language = language,
            name = name
        )
        stat_name.save()

        return stat_name


class NatureData(StatData, LanguageData):

    @classmethod
    def setup_nature_data(self, name='ntr', game_index=1):

        # NEED FLAVORS ONCE TEHYRE DONE

        decreased_stat = self.setup_stat_data(
            name='decrs stt for '+name)

        increased_stat = self.setup_stat_data(
            name='incrs stt for '+name)
        
        nature = Nature.objects.create (
            name = name,
            decreased_stat = decreased_stat,
            increased_stat = increased_stat,
            hates_flavor = None,
            likes_flavor = None,
            game_index = game_index
        )
        nature.save()

        return nature

    @classmethod
    def setup_nature_name_data(self, nature, name='ntr nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        nature_name = NatureName.objects.create (
            nature = nature,
            language = language,
            name = name
        )
        nature_name.save()

        return nature_name



class PokedexData(RegionData, LanguageData):

    @classmethod
    def setup_pokedex_data(self, name='pkdx'):

        region = self.setup_region_data(
            name='rgn for '+name)

        pokedex = Pokedex.objects.create (
            name = name,
            region = region,
        )
        pokedex.save()

        return pokedex

    @classmethod
    def setup_pokedex_name_data(self, pokedex, name='pkdx nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        pokedex_name = PokedexName.objects.create (
            pokedex = pokedex,
            language = language,
            name = name
        )
        pokedex_name.save()

        return pokedex_name

    @classmethod
    def setup_pokedex_description_data(self, pokedex, description='pkdx desc'):

        language = self.setup_language_data(
            name='lang for '+description)

        pokedex_description = PokedexDescription.objects.create (
            pokedex = pokedex,
            language = language,
            description = description
        )
        pokedex_description.save()

        return pokedex_description


class PokemonData(EggGroupData, PokedexData, GrowthRateData, GenerationData, ItemData, TypeData, AbilityData, StatData, VersionData, MoveData, LanguageData):

    @classmethod
    def setup_pokemon_habitat_data(self, name='pkm hbtt'):

        pokemon_habitat = PokemonHabitat.objects.create (
            name = name,
        )
        pokemon_habitat.save()

        return pokemon_habitat

    @classmethod
    def setup_pokemon_habitat_name_data(self, pokemon_habitat, name='pkm hbtt nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        pokemon_habitat_name = PokemonHabitatName.objects.create (
            pokemon_habitat = pokemon_habitat,
            language = language,
            name = name
        )
        pokemon_habitat_name.save()

        return pokemon_habitat_name

    @classmethod
    def setup_pokemon_color_data(self, name='pkm clr'):

        pokemon_color = PokemonColor.objects.create (
            name = name,
        )
        pokemon_color.save()

        return pokemon_color

    @classmethod
    def setup_pokemon_color_name_data(self, pokemon_color, name='pkm clr nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        pokemon_color_name = PokemonColorName.objects.create (
            pokemon_color = pokemon_color,
            language = language,
            name = name
        )
        pokemon_color_name.save()

        return pokemon_color_name

    @classmethod
    def setup_pokemon_shape_data(self, name='pkm shp'):

        pokemon_shape = PokemonShape.objects.create (
            name = name,
        )
        pokemon_shape.save()

        return pokemon_shape

    @classmethod
    def setup_pokemon_shape_name_data(self, pokemon_shape, name='pkm shp nm', awesome_name='pkm shp awsm nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        pokemon_shape_name = PokemonShapeName.objects.create (
            pokemon_shape = pokemon_shape,
            language = language,
            name = name,
            awesome_name = awesome_name
        )
        pokemon_shape_name.save()

        return pokemon_shape_name

    @classmethod
    def setup_pokemon_species_data(self, evolves_from_species=None, evolution_chain=None, name='pkm spcs', gender_rate=50, capture_rate=20, base_happiness=20, is_baby=False, hatch_counter=10, has_gender_differences=True, growth_rate=20, forms_switchable=False, order=1):

        generation = self.setup_generation_data(
            name='gen for '+name)

        growth_rate = self.setup_growth_rate_data(
            name='grth rt for '+name)

        pokemon_shape = self.setup_pokemon_shape_data(
            name='pkmn shp for '+name)

        pokemon_color = self.setup_pokemon_color_data(
            name='pkmn clr for '+name)

        pokemon_habitat = self.setup_pokemon_habitat_data(
            name='pkm hbtt for '+name)

        pokemon_species = PokemonSpecies.objects.create (
            name = name,
            generation = generation,
            evolves_from_species = evolves_from_species,
            evolution_chain = evolution_chain,
            pokemon_color = pokemon_color,
            pokemon_shape = pokemon_shape,
            pokemon_habitat = pokemon_habitat,
            gender_rate = gender_rate,
            capture_rate = capture_rate,
            base_happiness = base_happiness,
            is_baby = is_baby,
            hatch_counter = hatch_counter,
            has_gender_differences = has_gender_differences,
            growth_rate = growth_rate,
            forms_switchable = forms_switchable,
            order = forms_switchable
        )
        pokemon_species.save()

        return pokemon_species

    classmethod
    def setup_pokemon_species_name_data(self, pokemon_species, name='pkmn spcs nm', genus='pkmn spcs gns'):

        language = self.setup_language_data(
            name='lang for '+name)

        pokemon_species_name = PokemonSpeciesName.objects.create (
            pokemon_species = pokemon_species,
            language = language,
            name = name,
            genus = genus
        )
        pokemon_species_name.save()

        return pokemon_species_name
 
    @classmethod
    def setup_pokemon_data(self, pokemon_species, name='pkmn', height=100, weight=100, base_experience=0, order=1, is_default=False):

        pokemon = Pokemon.objects.create (
            name = name,
            pokemon_species = pokemon_species,
            height = height,
            weight = weight,
            base_experience = base_experience,
            order = order,
            is_default = is_default
        )
        pokemon.save()

        return pokemon

    @classmethod
    def setup_pokemon_form_data(self, pokemon, name='pkmn nrml frm', form_name='nrml', order=1, is_default=True, is_battle_only=True, form_order=1, is_mega=False):

        version_group = self.setup_version_group_data(
            name='ver grp for '+name)

        pokemon_form = PokemonForm (
            name = name,
            form_name = form_name,
            pokemon = pokemon,
            version_group = version_group,
            is_default = is_default,
            is_battle_only = is_battle_only,
            is_mega = is_mega,
            form_order = form_order,
            order = order
          )
        pokemon_form.save()

        return pokemon_form

    @classmethod
    def setup_pokemon_ability_data(self, pokemon, is_hidden=False, slot=1):

        ability = self.setup_ability_data(
            name='ablty for pkmn')

        pokemon_ability = PokemonAbility (
            pokemon = pokemon,
            ability = ability,
            is_hidden = is_hidden,
            slot = slot
          )
        pokemon_ability.save()

        return pokemon_ability

    @classmethod
    def setup_pokemon_stat_data(self, pokemon, base_stat=10, effort=10):

        stat = self.setup_stat_data(
            name='stt for pkmn')

        pokemon_stat = PokemonStat (
            pokemon = pokemon,
            stat = stat,
            base_stat = base_stat,
            effort = effort
          )
        pokemon_stat.save()

        return pokemon_stat

    @classmethod
    def setup_pokemon_type_data(self, pokemon, slot=1):

        type = self.setup_type_data(
            name='tp for pkmn')

        pokemon_type = PokemonType (
            pokemon = pokemon,
            type = type,
            slot = slot
          )
        pokemon_type.save()

        return pokemon_type

    @classmethod
    def setup_pokemon_item_data(self, pokemon, rarity=50):

        item = self.setup_item_data(
            name='itm for pkmn')

        version = self.setup_version_data(
            name='ver grp for pkmn itm')

        pokemon_item = PokemonItem (
            pokemon = pokemon,
            version = version,
            item = item,
            rarity = rarity
          )
        pokemon_item.save()

        return pokemon_item

    @classmethod
    def setup_pokemon_move_data(self, pokemon, level=0, order=1):

        move = self.setup_move_data(
            name='mv for pkmn')

        move_learn_method = self.setup_move_learn_method_data(
            name='mv lrn mthd for pkmn')

        version_group = self.setup_version_group_data(
            name='ver grp for pkmn')

        pokemon_move = PokemonMove.objects.create (
            pokemon = pokemon,
            version_group = version_group,
            move = move,
            move_learn_method = move_learn_method,
            level = level,
            order = order
        )
        pokemon_move.save()

        return pokemon_move



class EvolutionData(PokemonData, LocationData, LanguageData):

    @classmethod
    def setup_evolution_trigger_data(self, name='evltn trgr'):

        evolution_trigger = EvolutionTrigger.objects.create (
            name = name,
        )
        evolution_trigger.save()

        return evolution_trigger

    @classmethod
    def setup_evolution_trigger_name_data(self, evolution_trigger, name='evltn trgr nm'):

        language = self.setup_language_data(
            name='lang for '+name)

        evolution_trigger_name = EvolutionTriggerName.objects.create (
            evolution_trigger = evolution_trigger,
            language = language,
            name = name
        )
        evolution_trigger_name.save()

        return evolution_trigger_name

    @classmethod
    def setup_evolution_chain_data(self, baby_trigger_item=None):

        evolution_chain = EvolutionChain.objects.create (
            baby_trigger_item=baby_trigger_item,
        )
        evolution_chain.save()

        return evolution_chain

    @classmethod
    def setup_pokemon_evolution_data(self, evolved_species=None, party_species=None, trade_species=None, evolution_item=None, party_type=None, min_level=0, gender=None, location=None, held_item=None, time_of_day='', known_move=None, known_move_type=None, min_happiness=0, min_beauty=0, min_affection=0, relative_physical_stats=0, needs_overworld_rain=False, turn_upside_down=False):

        evolution_trigger = self.setup_evolution_trigger_data(
            name='evltn trgr for pkmn evltn')

        pokemon_evolution = PokemonEvolution.objects.create (
            evolved_species = evolved_species,
            evolution_trigger = evolution_trigger,
            evolution_item = evolution_item,
            min_level = min_level,
            gender = gender,
            location = location,
            held_item = held_item,
            time_of_day = time_of_day,
            known_move = known_move,
            known_move_type = known_move_type,
            min_happiness = min_happiness,
            min_beauty = min_beauty,
            min_affection = min_affection,
            relative_physical_stats = relative_physical_stats,
            party_species = party_species,
            party_type = party_type,
            trade_species = trade_species,
            needs_overworld_rain = needs_overworld_rain,
            turn_upside_down = turn_upside_down
        )
        pokemon_evolution.save()

        return pokemon_evolution





""" 
Tests
"""

class LanguageTests(LanguageData, APITestCase):

    def test_language_api(self):

        language = self.setup_language_data(name='base lang')
        language_name = self.setup_language_name_data(language, name='base lang name')

        response = self.client.get('{}/language/{}/'.format(api_v2, language.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], language.pk)
        self.assertEqual(response.data['iso639'], language.iso639)
        self.assertEqual(response.data['iso3166'], language.iso3166)
        self.assertEqual(response.data['name'], language.name)
        self.assertEqual(response.data['official'], language.official)
        #name params
        self.assertEqual(response.data['names'][0]['name'], language_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], language_name.local_language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, language_name.local_language.pk))



class RegionTests(RegionData, APITestCase):

    def test_region_api(self):

        region = self.setup_region_data(name='base reg')
        region_name = self.setup_region_name_data(region, name='base reg name')

        response = self.client.get('{}/region/{}/'.format(api_v2, region.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], region.pk)
        self.assertEqual(response.data['name'], region.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], region_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], region_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, region_name.language.pk))
        



class GenerationTests(GenerationData, APITestCase):

    def test_generation_api(self):

        generation = self.setup_generation_data(name='base gen')
        generation_name = self.setup_generation_name_data(generation, name='base reg name')

        response = self.client.get('{}/generation/{}/'.format(api_v2, generation.pk))

        # base params
        self.assertEqual(response.data['id'], generation.pk)
        self.assertEqual(response.data['name'], generation.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], generation_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], generation_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, generation_name.language.pk))
        # region params
        self.assertEqual(response.data['region']['name'], generation.region.name)
        self.assertEqual(response.data['region']['url'], '{}{}/region/{}/'.format(test_host, api_v2, generation.region.pk))
        



class VersionTests(VersionData, APITestCase):

    def test_version_api(self):

        version = self.setup_version_data(name='base ver')
        version_name = self.setup_version_name_data(version, name='base ver name')

        response = self.client.get('{}/version/{}/'.format(api_v2, version.pk))

        # base params
        self.assertEqual(response.data['id'], version.pk)
        self.assertEqual(response.data['name'], version.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], version_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], version_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, version_name.language.pk))
        # version group params
        self.assertEqual(response.data['version_group']['name'], version.version_group.name)
        self.assertEqual(response.data['version_group']['url'], '{}{}/version-group/{}/'.format(test_host, api_v2, version.version_group.pk))



class EggGroupTests(EggGroupData, APITestCase):

    def test_nature_api(self):

        # NEEDS SPECIES

        egg_group = self.setup_egg_group_data(name='base egg grp')
        egg_group_name = self.setup_egg_group_name_data(egg_group, name='base egg grp name')

        response = self.client.get('{}/egg-group/{}/'.format(api_v2, egg_group.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], egg_group.pk)
        self.assertEqual(response.data['name'], egg_group.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], egg_group_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], egg_group_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, egg_group_name.language.pk))       



class AbilityTests(AbilityData, APITestCase):

    def test_ability_api(self):

        ability = self.setup_ability_data(name='base ablty')
        ability_name = self.setup_ability_name_data(ability, name='base ablty name')
        ability_effect_text = self.setup_ability_effect_text_data(ability, effect='base ablty efct')
        ability_flavor_text = self.setup_ability_flavor_text_data(ability, flavor_text='base flvr txt')

        response = self.client.get('{}/ability/{}/'.format(api_v2, ability.pk))
        
        # base params
        self.assertEqual(response.data['id'], ability.pk)
        self.assertEqual(response.data['name'], ability.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], ability_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], ability_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, ability_name.language.pk))
        # description params
        self.assertEqual(response.data['effect_text_entries'][0]['effect'], ability_effect_text.effect)
        self.assertEqual(response.data['effect_text_entries'][0]['short_effect'], ability_effect_text.short_effect)
        self.assertEqual(response.data['effect_text_entries'][0]['language']['name'], ability_effect_text.language.name)
        self.assertEqual(response.data['effect_text_entries'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, ability_effect_text.language.pk))
        # flavor text params
        self.assertEqual(response.data['flavor_text_entries'][0]['text'], ability_flavor_text.flavor_text)
        self.assertEqual(response.data['flavor_text_entries'][0]['version_group']['name'], ability_flavor_text.version_group.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['name'], ability_flavor_text.language.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, ability_flavor_text.language.pk))
        # generation params
        self.assertEqual(response.data['generation']['name'], ability.generation.name)
        self.assertEqual(response.data['generation']['url'], '{}{}/generation/{}/'.format(test_host, api_v2, ability.generation.pk))



class ItemTests(ItemData, APITestCase):

    def test_item_attribute_api(self):

        # item attribute data
        item_attribute = self.setup_item_attribute_data(name='base itm attr')
        item_attribute_name = self.setup_item_attribute_name_data(item_attribute, name='base itm attr nm')
        item_attribute_description = self.setup_item_attribute_description_data(item_attribute, description='base itm attr desc')

        response = self.client.get('{}/item-attribute/{}/'.format(api_v2, item_attribute.pk))

        # base params
        self.assertEqual(response.data['id'], item_attribute.pk)
        self.assertEqual(response.data['name'], item_attribute.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_attribute_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_attribute_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_attribute_name.language.pk))
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], item_attribute_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], item_attribute_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_attribute_description.language.pk))

    def test_item_category_api(self):

        # item category data
        item_category = self.setup_item_category_data(name='base itm ctgry')
        item_category_name = self.setup_item_category_name_data(item_category, name='base itm ctgry nm')

        response = self.client.get('{}/item-category/{}/'.format(api_v2, item_category.pk))

        # base params
        self.assertEqual(response.data['id'], item_category.pk)
        self.assertEqual(response.data['name'], item_category.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_category_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_category_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_category_name.language.pk))
        # pocket params
        self.assertEqual(response.data['pocket']['name'], item_category.item_pocket.name)
        self.assertEqual(response.data['pocket']['url'], '{}{}/item-pocket/{}/'.format(test_host, api_v2, item_category.item_pocket.pk))

    def test_item_fling_effect_api(self):

        # item category data
        item_fling_effect = self.setup_item_fling_effect_data(name='base itm flng efct')
        item_fling_effect_description = self.setup_item_fling_effect_description_data(item_fling_effect, description='base itm flng efct nm')

        response = self.client.get('{}/item-fling-effect/{}/'.format(api_v2, item_fling_effect.pk))

        # base params
        self.assertEqual(response.data['id'], item_fling_effect.pk)
        self.assertEqual(response.data['name'], item_fling_effect.name)
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], item_fling_effect_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], item_fling_effect_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_fling_effect_description.language.pk))

    def test_item_pocket_api(self):

        # item pocket data
        item_pocket = self.setup_item_pocket_data(name='base itm pkt')
        item_pocket_name = self.setup_item_pocket_name_data(item_pocket, name='base itm pkt nm')

        response = self.client.get('{}/item-pocket/{}/'.format(api_v2, item_pocket.pk))

        # base params
        self.assertEqual(response.data['id'], item_pocket.pk)
        self.assertEqual(response.data['name'], item_pocket.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_pocket_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_pocket_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_pocket_name.language.pk))

    def test_item_api(self):

        item_category = self.setup_item_category_data(name='itm ctgry for base itm')
        item_fling_effect = self.setup_item_fling_effect_data(name='itm flng efct for base itm')
        item = self.setup_item_data(item_category, item_fling_effect, name='base itm')
        item_name = self.setup_item_name_data(item, name='base itm name')
        item_flavor_text = self.setup_item_flavor_text_data(item, flavor_text='base itm flvr txt')
        item_effect_text = self.setup_item_effect_text_data(item, effect='base nrml efct', short_effect='base shrt efct')
        item_attribute = self.setup_item_attribute_data()

        # map item attribute to item
        item_attribute_map = ItemAttributeMap (
            item = item,
            item_attribute = item_attribute
          )
        item_attribute_map.save()

        response = self.client.get('{}/item/{}/'.format(api_v2, item.pk))
        
        # base params
        self.assertEqual(response.data['id'], item.pk)
        self.assertEqual(response.data['name'], item.name)
        self.assertEqual(response.data['cost'], item.cost)
        self.assertEqual(response.data['fling_power'], item.fling_power)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_name.language.pk))
        # flavor text params
        self.assertEqual(response.data['flavor_text_entries'][0]['text'], item_flavor_text.flavor_text)
        self.assertEqual(response.data['flavor_text_entries'][0]['version_group']['name'], item_flavor_text.version_group.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['version_group']['url'], '{}{}/version-group/{}/'.format(test_host, api_v2, item_flavor_text.version_group.pk))
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['name'], item_flavor_text.language.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_flavor_text.language.pk))
        # effect text params
        self.assertEqual(response.data['effect_text_entries'][0]['effect'], item_effect_text.effect)
        self.assertEqual(response.data['effect_text_entries'][0]['short_effect'], item_effect_text.short_effect)
        self.assertEqual(response.data['effect_text_entries'][0]['language']['name'], item_effect_text.language.name)
        self.assertEqual(response.data['effect_text_entries'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, item_effect_text.language.pk))
        # category params
        self.assertEqual(response.data['category']['name'], item_category.name)
        self.assertEqual(response.data['category']['url'], '{}{}/item-category/{}/'.format(test_host, api_v2, item_category.pk))
        # fling effect params
        self.assertEqual(response.data['fling_effect']['name'], item_fling_effect.name)
        self.assertEqual(response.data['fling_effect']['url'], '{}{}/item-fling-effect/{}/'.format(test_host, api_v2, item_fling_effect.pk))
        # attribute params
        self.assertEqual(response.data['attributes'][0]['name'], item_attribute.name)
        self.assertEqual(response.data['attributes'][0]['url'], '{}{}/item-attribute/{}/'.format(test_host, api_v2, item_attribute.pk))


class BerryData(BerryData, APITestCase):

    def test_berry_firmness_api(self):

        berry_firmness = self.setup_berry_firmness_data(name='base bry frmns')
        berry_firmness_name = self.setup_berry_firmness_name_data(berry_firmness, name='base bry frmns nm')

        response = self.client.get('{}/berry-firmness/{}/'.format(api_v2, berry_firmness.pk))

        # base params
        self.assertEqual(response.data['id'], berry_firmness.pk)
        self.assertEqual(response.data['name'], berry_firmness.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], berry_firmness_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], berry_firmness_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, berry_firmness_name.language.pk))

    def test_berry_api(self):

        # NEEDS NATURE

        # item pocket data
        berry = self.setup_berry_data(name='base bry')
        
        response = self.client.get('{}/berry/{}/'.format(api_v2, berry.pk))

        # base params
        self.assertEqual(response.data['id'], berry.pk)
        self.assertEqual(response.data['name'], berry.name)
        self.assertEqual(response.data['growth_time'], berry.growth_time)
        self.assertEqual(response.data['max_harvest'], berry.max_harvest)
        self.assertEqual(response.data['nature_power'], berry.natural_gift_power)
        self.assertEqual(response.data['size'], berry.size)
        self.assertEqual(response.data['smoothness'], berry.smoothness)
        self.assertEqual(response.data['soil_dryness'], berry.soil_dryness)
        # firmness params
        self.assertEqual(response.data['firmness']['name'], berry.berry_firmness.name)
        self.assertEqual(response.data['firmness']['url'], '{}{}/berry-firmness/{}/'.format(test_host, api_v2, berry.berry_firmness.pk))
        # item params
        self.assertEqual(response.data['item']['name'], berry.item.name)
        self.assertEqual(response.data['item']['url'], '{}{}/item/{}/'.format(test_host, api_v2, berry.item.pk))
        


class GrowthRateTests(GrowthRateData, APITestCase):

    def test_growth_rate_api(self):

        # item pocket data
        growth_rate = self.setup_growth_rate_data(name='base grth rt')
        growth_rate_description = self.setup_growth_rate_description_data(growth_rate, description='base grth rt desc')

        # map item attribute to item
        experience = Experience (
            growth_rate = growth_rate,
            level = 10,
            experience = 3000
        )
        experience.save()

        response = self.client.get('{}/growth-rate/{}/'.format(api_v2, growth_rate.pk))

        # base params
        self.assertEqual(response.data['id'], growth_rate.pk)
        self.assertEqual(response.data['name'], growth_rate.name)
        self.assertEqual(response.data['formula'], growth_rate.formula)
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], growth_rate_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], growth_rate_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, growth_rate_description.language.pk))
        # experience params
        self.assertEqual(response.data['levels'][0]['level'], experience.level)
        self.assertEqual(response.data['levels'][0]['experience'], experience.experience)



class LocationTests(LocationData, APITestCase):

    def test_location_api(self):

        location = self.setup_location_data(name='base lctn')
        location_name = self.setup_location_name_data(location, name='base lctn name')

        response = self.client.get('{}/location/{}/'.format(api_v2, location.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], location.pk)
        self.assertEqual(response.data['name'], location.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], location_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], location_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, location_name.language.pk))
        # region params
        self.assertEqual(response.data['region']['name'], location.region.name)
        self.assertEqual(response.data['region']['url'], '{}{}/region/{}/'.format(test_host, api_v2, location.region.pk))
        

class TypeTests(TypeData, APITestCase):

    def test_type_api(self):

        type = self.setup_type_data(name='base tp')
        type_name = self.setup_type_name_data(type, name='base tp nm')

        no_damage_to = self.setup_type_data(name='no damage to tp')
        half_damage_to = self.setup_type_data(name='half damage to tp')
        double_damage_to = self.setup_type_data(name='double damage to tp')
        no_damage_from = self.setup_type_data(name='no damage from tp')
        half_damage_from = self.setup_type_data(name='half damage from tp')
        double_damage_from = self.setup_type_data(name='double damage from tp')

        # type relations
        no_damage_to_relation = TypeEfficacy (
            damage_type = type,
            target_type = no_damage_to,
            damage_factor = 0
        )
        no_damage_to_relation.save()

        half_damage_to_type_relation = TypeEfficacy (
            damage_type = type,
            target_type = half_damage_to,
            damage_factor = 50
        )
        half_damage_to_type_relation.save()

        double_damage_to_type_relation = TypeEfficacy (
            damage_type = type,
            target_type = double_damage_to,
            damage_factor = 200
        )
        double_damage_to_type_relation.save()

        no_damage_from_relation = TypeEfficacy (
            damage_type = no_damage_from,
            target_type = type,
            damage_factor = 0
        )
        no_damage_from_relation.save()

        half_damage_from_type_relation = TypeEfficacy (
            damage_type = half_damage_from,
            target_type = type,
            damage_factor = 50
        )
        half_damage_from_type_relation.save()

        double_damage_from_type_relation = TypeEfficacy (
            damage_type = double_damage_from,
            target_type = type,
            damage_factor = 200
        )
        double_damage_from_type_relation.save()

        response = self.client.get('{}/type/{}/'.format(api_v2, type.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], type.pk)
        self.assertEqual(response.data['name'], type.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], type_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], type_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, type_name.language.pk))
        # generation params
        self.assertEqual(response.data['generation']['name'], type.generation.name)
        self.assertEqual(response.data['generation']['url'], '{}{}/generation/{}/'.format(test_host, api_v2, type.generation.pk))
        # damage relations params
        self.assertEqual(response.data['damage_relations']['no_damage_to'][0]['name'], no_damage_to.name)
        self.assertEqual(response.data['damage_relations']['no_damage_to'][0]['url'], '{}{}/type/{}/'.format(test_host, api_v2, no_damage_to.pk))
        self.assertEqual(response.data['damage_relations']['half_damage_to'][0]['name'], half_damage_to.name)
        self.assertEqual(response.data['damage_relations']['half_damage_to'][0]['url'], '{}{}/type/{}/'.format(test_host, api_v2, half_damage_to.pk))
        self.assertEqual(response.data['damage_relations']['double_damage_to'][0]['name'], double_damage_to.name)
        self.assertEqual(response.data['damage_relations']['double_damage_to'][0]['url'], '{}{}/type/{}/'.format(test_host, api_v2, double_damage_to.pk))
        self.assertEqual(response.data['damage_relations']['no_damage_from'][0]['name'], no_damage_from.name)
        self.assertEqual(response.data['damage_relations']['no_damage_from'][0]['url'], '{}{}/type/{}/'.format(test_host, api_v2, no_damage_from.pk))
        self.assertEqual(response.data['damage_relations']['half_damage_from'][0]['name'], half_damage_from.name)
        self.assertEqual(response.data['damage_relations']['half_damage_from'][0]['url'], '{}{}/type/{}/'.format(test_host, api_v2, half_damage_from.pk))
        self.assertEqual(response.data['damage_relations']['double_damage_from'][0]['name'], double_damage_from.name)
        self.assertEqual(response.data['damage_relations']['double_damage_from'][0]['url'], '{}{}/type/{}/'.format(test_host, api_v2, double_damage_from.pk))


class PokedexTests(PokedexData, APITestCase):

    def test_pokedex_api(self):

        pokedex = self.setup_pokedex_data(name='base pkdx')
        pokedex_name = self.setup_pokedex_name_data(pokedex, name='base pkdx name')
        pokedex_description = self.setup_pokedex_description_data(pokedex, description='base pkdx desc')

        response = self.client.get('{}/pokedex/{}/'.format(api_v2, pokedex.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokedex.pk)
        self.assertEqual(response.data['name'], pokedex.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], pokedex_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], pokedex_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokedex_name.language.pk))
        # descriptions params
        self.assertEqual(response.data['descriptions'][0]['description'], pokedex_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], pokedex_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokedex_description.language.pk))
        # region params
        self.assertEqual(response.data['region']['name'], pokedex.region.name)
        self.assertEqual(response.data['region']['url'], '{}{}/region/{}/'.format(test_host, api_v2, pokedex.region.pk))
        

class MoveTests(MoveData, APITestCase):

    def test_move_ailment_api(self):

        move_ailment = self.setup_move_ailment_data(name='base mv almnt')
        move_ailment_name = self.setup_move_ailment_name_data(move_ailment, name='base mv almnt name')

        response = self.client.get('{}/move-ailment/{}/'.format(api_v2, move_ailment.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], move_ailment.pk)
        self.assertEqual(response.data['name'], move_ailment.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], move_ailment_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], move_ailment_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_ailment_name.language.pk))

    def test_move_category_api(self):

        move_category = self.setup_move_category_data(name='base mv ctgry')
        move_category_description = self.setup_move_category_description_data(move_category, description='base mv ctgry description')

        response = self.client.get('{}/move-category/{}/'.format(api_v2, move_category.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], move_category.pk)
        self.assertEqual(response.data['name'], move_category.name)
        # name params
        self.assertEqual(response.data['descriptions'][0]['description'], move_category_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], move_category_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_category_description.language.pk))

    def test_move_damage_class_api(self):

        move_damage_class = self.setup_move_damage_class_data(name='base mv dmg cls')
        move_damage_class_name = self.setup_move_damage_class_name_data(move_damage_class, name='base mv dmg cls nm')
        move_damage_class_description = self.setup_move_damage_class_description_data(move_damage_class, description='base mv dmg cls desc')

        response = self.client.get('{}/move-damage-class/{}/'.format(api_v2, move_damage_class.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], move_damage_class.pk)
        self.assertEqual(response.data['name'], move_damage_class.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], move_damage_class_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], move_damage_class_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_damage_class_name.language.pk))
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], move_damage_class_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], move_damage_class_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_damage_class_description.language.pk))

    def test_move_learn_method_api(self):

        move_learn_method = self.setup_move_learn_method_data(name='base mv lrn mthd')
        move_learn_method_name = self.setup_move_learn_method_name_data(move_learn_method, name='base mv lrn mthd nm')
        move_learn_method_description = self.setup_move_learn_method_description_data(move_learn_method, description='base mv lrn mthd desc')

        response = self.client.get('{}/move-learn-method/{}/'.format(api_v2, move_learn_method.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], move_learn_method.pk)
        self.assertEqual(response.data['name'], move_learn_method.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], move_learn_method_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], move_learn_method_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_learn_method_name.language.pk))
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], move_learn_method_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], move_learn_method_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_learn_method_description.language.pk))

    def test_move_target_api(self):

        move_target = self.setup_move_target_data(name='base mv trgt')
        move_target_name = self.setup_move_target_name_data(move_target, name='base mv trgt nm')
        move_target_description = self.setup_move_target_description_data(move_target, description='base mv trgt desc')

        response = self.client.get('{}/move-target/{}/'.format(api_v2, move_target.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], move_target.pk)
        self.assertEqual(response.data['name'], move_target.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], move_target_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], move_target_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_target_name.language.pk))
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], move_target_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], move_target_description.language.name)
        self.assertEqual(response.data['descriptions'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_target_description.language.pk))

    def test_move_api(self):

        move = self.setup_move_data(name='base mv')
        move_name = self.setup_move_name_data(move, name='base mv nm')
        move_meta = self.setup_move_meta_data(move)

        response = self.client.get('{}/move/{}/'.format(api_v2, move.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], move.pk)
        self.assertEqual(response.data['name'], move.name)
        self.assertEqual(response.data['accuracy'], move.accuracy)
        self.assertEqual(response.data['effect_chance'], move.move_effect_chance)
        self.assertEqual(response.data['power'], move.power)
        self.assertEqual(response.data['pp'], move.pp)
        self.assertEqual(response.data['priority'], move.priority)
        # name params
        self.assertEqual(response.data['names'][0]['name'], move_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], move_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, move_name.language.pk))
        # damage class params
        self.assertEqual(response.data['damage_class']['name'], move.move_damage_class.name)
        self.assertEqual(response.data['damage_class']['url'], '{}{}/move-damage-class/{}/'.format(test_host, api_v2, move.move_damage_class.pk))
        # generation params
        self.assertEqual(response.data['generation']['name'], move.generation.name)
        self.assertEqual(response.data['generation']['url'], '{}{}/generation/{}/'.format(test_host, api_v2, move.generation.pk))
        # target params
        self.assertEqual(response.data['target']['name'], move.move_target.name)
        self.assertEqual(response.data['target']['url'], '{}{}/move-target/{}/'.format(test_host, api_v2, move.move_target.pk))
        # type params
        self.assertEqual(response.data['type']['name'], move.type.name)
        self.assertEqual(response.data['type']['url'], '{}{}/type/{}/'.format(test_host, api_v2, move.type.pk))
        # meta data
        self.assertEqual(response.data['meta']['min_hits'], move_meta.min_hits)
        self.assertEqual(response.data['meta']['max_hits'], move_meta.max_hits)
        self.assertEqual(response.data['meta']['min_turns'], move_meta.min_turns)
        self.assertEqual(response.data['meta']['max_turns'], move_meta.max_turns)
        self.assertEqual(response.data['meta']['drain'], move_meta.drain)
        self.assertEqual(response.data['meta']['healing'], move_meta.healing)
        self.assertEqual(response.data['meta']['crit_rate'], move_meta.crit_rate)
        self.assertEqual(response.data['meta']['ailment_chance'], move_meta.ailment_chance)
        self.assertEqual(response.data['meta']['flinch_chance'], move_meta.flinch_chance)
        self.assertEqual(response.data['meta']['stat_chance'], move_meta.stat_chance)
        # ailment params
        self.assertEqual(response.data['meta']['ailment']['name'], move_meta.move_meta_ailment.name)
        self.assertEqual(response.data['meta']['ailment']['url'], '{}{}/move-ailment/{}/'.format(test_host, api_v2, move_meta.move_meta_ailment.pk))
        # category params
        self.assertEqual(response.data['meta']['category']['name'], move_meta.move_meta_category.name)
        self.assertEqual(response.data['meta']['category']['url'], '{}{}/move-category/{}/'.format(test_host, api_v2, move_meta.move_meta_category.pk))



class StatTests(StatData, APITestCase):

    def test_stat_api(self):

        stat = self.setup_stat_data(name='base stt')
        stat_name = self.setup_stat_name_data(stat, name='base stt name')

        response = self.client.get('{}/stat/{}/'.format(api_v2, stat.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], stat.pk)
        self.assertEqual(response.data['name'], stat.name)
        self.assertEqual(response.data['game_index'], stat.game_index)
        self.assertEqual(response.data['is_battle_only'], stat.is_battle_only)
        # name params
        self.assertEqual(response.data['names'][0]['name'], stat_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], stat_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, stat_name.language.pk))
        # move damage class params
        self.assertEqual(response.data['move_damage_class']['name'], stat.move_damage_class.name)
        self.assertEqual(response.data['move_damage_class']['url'], '{}{}/move-damage-class/{}/'.format(test_host, api_v2, stat.move_damage_class.pk))



class NatureTests(NatureData, APITestCase):

    def test_nature_api(self):

        nature = self.setup_nature_data(name='base ntr')
        nature_name = self.setup_nature_name_data(nature, name='base ntr name')

        response = self.client.get('{}/nature/{}/'.format(api_v2, nature.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], nature.pk)
        self.assertEqual(response.data['name'], nature.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], nature_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], nature_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, nature_name.language.pk))
        # stat params
        self.assertEqual(response.data['decreased_stat']['name'], nature.decreased_stat.name)
        self.assertEqual(response.data['decreased_stat']['url'], '{}{}/stat/{}/'.format(test_host, api_v2, nature.decreased_stat.pk))
        self.assertEqual(response.data['increased_stat']['name'], nature.increased_stat.name)
        self.assertEqual(response.data['increased_stat']['url'], '{}{}/stat/{}/'.format(test_host, api_v2, nature.increased_stat.pk))


class PokemonTests(PokemonData, APITestCase):

    def test_pokemon_habitat_api(self):

        pokemon_habitat = self.setup_pokemon_habitat_data(name='base pkmn hbtt trgr')
        pokemon_habitat_name = self.setup_pokemon_habitat_name_data(pokemon_habitat, name='base pkmn hbtt name')

        response = self.client.get('{}/pokemon-habitat/{}/'.format(api_v2, pokemon_habitat.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokemon_habitat.pk)
        self.assertEqual(response.data['name'], pokemon_habitat.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], pokemon_habitat_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], pokemon_habitat_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokemon_habitat_name.language.pk))

    def test_pokemon_color_api(self):

        pokemon_color = self.setup_pokemon_color_data(name='base pkmn clr trgr')
        pokemon_color_name = self.setup_pokemon_color_name_data(pokemon_color, name='base pkmn clr name')

        response = self.client.get('{}/pokemon-color/{}/'.format(api_v2, pokemon_color.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokemon_color.pk)
        self.assertEqual(response.data['name'], pokemon_color.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], pokemon_color_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], pokemon_color_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokemon_color_name.language.pk))

    def test_pokemon_shape_api(self):

        pokemon_shape = self.setup_pokemon_shape_data(name='base pkmn shp trgr')
        pokemon_shape_name = self.setup_pokemon_shape_name_data(pokemon_shape, name='base pkmn shp name')

        response = self.client.get('{}/pokemon-shape/{}/'.format(api_v2, pokemon_shape.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokemon_shape.pk)
        self.assertEqual(response.data['name'], pokemon_shape.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], pokemon_shape_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], pokemon_shape_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokemon_shape_name.language.pk))
        # awesome name params
        self.assertEqual(response.data['awesome_names'][0]['awesome_name'], pokemon_shape_name.awesome_name)
        self.assertEqual(response.data['awesome_names'][0]['language']['name'], pokemon_shape_name.language.name)
        self.assertEqual(response.data['awesome_names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokemon_shape_name.language.pk))

    def test_pokemon_species_api(self):

        evolves_from_species = self.setup_pokemon_species_data(name='evolves from pkmn spcs')
        pokemon_species = self.setup_pokemon_species_data(evolves_from_species=evolves_from_species, name='base pkmn spcs')
        pokemon_species_name = self.setup_pokemon_species_name_data(pokemon_species, name='base pkmn shp name')

        pokedex = self.setup_pokedex_data(name='pkdx for pkmn spcs')

        dex_number = PokemonDexNumber (
            pokemon_species = pokemon_species,
            pokedex = pokedex,
            pokedex_number = 100
          )
        dex_number.save()

        egg_group = self.setup_egg_group_data(name='egg grp for pkmn spcs')

        pokemon_egg_group = PokemonEggGroup (
            pokemon_species = pokemon_species,
            egg_group = egg_group
        )
        pokemon_egg_group.save()

        pokemon = self.setup_pokemon_data ( pokemon_species=pokemon_species, name = 'pkm for base pkmn spcs')

        response = self.client.get('{}/pokemon-species/{}/'.format(api_v2, pokemon_species.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokemon_species.pk)
        self.assertEqual(response.data['name'], pokemon_species.name)
        self.assertEqual(response.data['order'], pokemon_species.order)
        self.assertEqual(response.data['capture_rate'], pokemon_species.capture_rate)
        self.assertEqual(response.data['base_happiness'], pokemon_species.base_happiness)
        self.assertEqual(response.data['is_baby'], pokemon_species.is_baby)
        self.assertEqual(response.data['hatch_counter'], pokemon_species.hatch_counter)
        self.assertEqual(response.data['has_gender_differences'], pokemon_species.has_gender_differences)
        self.assertEqual(response.data['forms_switchable'], pokemon_species.forms_switchable)
        # name params
        self.assertEqual(response.data['names'][0]['name'], pokemon_species_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], pokemon_species_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokemon_species_name.language.pk))
        # growth rate params
        self.assertEqual(response.data['growth_rate']['name'], pokemon_species.growth_rate.name)
        self.assertEqual(response.data['growth_rate']['url'], '{}{}/growth-rate/{}/'.format(test_host, api_v2, pokemon_species.growth_rate.pk))
        # dex number params
        self.assertEqual(response.data['pokedex_numbers'][0]['entry_number'], dex_number.pokedex_number)
        self.assertEqual(response.data['pokedex_numbers'][0]['pokedex']['name'], pokedex.name)
        self.assertEqual(response.data['pokedex_numbers'][0]['pokedex']['url'], '{}{}/pokedex/{}/'.format(test_host, api_v2, pokedex.pk))
        # egg group params
        self.assertEqual(response.data['egg_groups'][0]['name'], egg_group.name)
        self.assertEqual(response.data['egg_groups'][0]['url'], '{}{}/egg-group/{}/'.format(test_host, api_v2, egg_group.pk))
        # generation params
        self.assertEqual(response.data['generation']['name'], pokemon_species.generation.name)
        self.assertEqual(response.data['generation']['url'], '{}{}/generation/{}/'.format(test_host, api_v2, pokemon_species.generation.pk))
        # color params
        self.assertEqual(response.data['color']['name'], pokemon_species.pokemon_color.name)
        self.assertEqual(response.data['color']['url'], '{}{}/pokemon-color/{}/'.format(test_host, api_v2, pokemon_species.pokemon_color.pk))
        # shape params
        self.assertEqual(response.data['shape']['name'], pokemon_species.pokemon_shape.name)
        self.assertEqual(response.data['shape']['url'], '{}{}/pokemon-shape/{}/'.format(test_host, api_v2, pokemon_species.pokemon_shape.pk))
        # habitat params
        self.assertEqual(response.data['habitat']['name'], pokemon_species.pokemon_habitat.name)
        self.assertEqual(response.data['habitat']['url'], '{}{}/pokemon-habitat/{}/'.format(test_host, api_v2, pokemon_species.pokemon_habitat.pk))
        # evolves from params
        self.assertEqual(response.data['evolves_from_species']['name'], evolves_from_species.name)
        self.assertEqual(response.data['evolves_from_species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, evolves_from_species.pk))
        # genus params
        self.assertEqual(response.data['genera'][0]['genus'], pokemon_species_name.genus)
        self.assertEqual(response.data['genera'][0]['language']['name'], pokemon_species_name.language.name)
        self.assertEqual(response.data['genera'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, pokemon_species_name.language.pk))
        # pokemon varieties params
        self.assertEqual(response.data['varieties'][0]['is_default'], pokemon.is_default)
        self.assertEqual(response.data['varieties'][0]['pokemon']['name'], pokemon.name)
        self.assertEqual(response.data['varieties'][0]['pokemon']['url'], '{}{}/pokemon/{}/'.format(test_host, api_v2, pokemon.pk))
        
    def test_pokemon_api(self):

        pokemon_species = self.setup_pokemon_species_data(name='pkmn spcs for base pkmn')
        pokemon = self.setup_pokemon_data(pokemon_species=pokemon_species, name='base pkm')
        pokemon_form = self.setup_pokemon_form_data(pokemon=pokemon, name='pkm form for base pkmn')
        pokemon_ability = self.setup_pokemon_ability_data(pokemon=pokemon)
        pokemon_stat = self.setup_pokemon_stat_data(pokemon=pokemon)
        pokemon_type = self.setup_pokemon_type_data(pokemon=pokemon)
        pokemon_item = self.setup_pokemon_item_data(pokemon=pokemon)
        pokemon_move = self.setup_pokemon_move_data(pokemon=pokemon)

        response = self.client.get('{}/pokemon/{}/'.format(api_v2, pokemon.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokemon.pk)
        self.assertEqual(response.data['name'], pokemon.name)
        self.assertEqual(response.data['order'], pokemon.order)
        self.assertEqual(response.data['is_default'], pokemon.is_default)
        self.assertEqual(response.data['height'], pokemon.height)
        self.assertEqual(response.data['weight'], pokemon.weight)
        self.assertEqual(response.data['base_experience'], pokemon.base_experience)
        # species params
        self.assertEqual(response.data['species']['name'], pokemon_species.name)
        self.assertEqual(response.data['species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, pokemon_species.pk))
        # abilities params
        self.assertEqual(response.data['abilities'][0]['is_hidden'], pokemon_ability.is_hidden)
        self.assertEqual(response.data['abilities'][0]['slot'], pokemon_ability.slot)
        self.assertEqual(response.data['abilities'][0]['ability']['name'], pokemon_ability.ability.name)
        self.assertEqual(response.data['abilities'][0]['ability']['url'], '{}{}/ability/{}/'.format(test_host, api_v2, pokemon_ability.ability.pk))
        # stat params
        self.assertEqual(response.data['stats'][0]['base_stat'], pokemon_stat.base_stat)
        self.assertEqual(response.data['stats'][0]['effort'], pokemon_stat.effort)
        self.assertEqual(response.data['stats'][0]['stat']['name'], pokemon_stat.stat.name)
        self.assertEqual(response.data['stats'][0]['stat']['url'], '{}{}/stat/{}/'.format(test_host, api_v2, pokemon_stat.stat.pk))
        # stat params
        self.assertEqual(response.data['types'][0]['slot'], pokemon_type.slot)
        self.assertEqual(response.data['types'][0]['type']['name'], pokemon_type.type.name)
        self.assertEqual(response.data['types'][0]['type']['url'], '{}{}/type/{}/'.format(test_host, api_v2, pokemon_type.type.pk))
        # items params
        self.assertEqual(response.data['held_items'][0]['item']['name'], pokemon_item.item.name)
        self.assertEqual(response.data['held_items'][0]['item']['url'], '{}{}/item/{}/'.format(test_host, api_v2, pokemon_item.item.pk))
        self.assertEqual(response.data['held_items'][0]['version_details'][0]['rarity'], pokemon_item.rarity)
        self.assertEqual(response.data['held_items'][0]['version_details'][0]['version']['name'], pokemon_item.version.name)
        self.assertEqual(response.data['held_items'][0]['version_details'][0]['version']['url'], '{}{}/version/{}/'.format(test_host, api_v2, pokemon_item.version.pk))
        # move params
        self.assertEqual(response.data['moves'][0]['move']['name'], pokemon_move.move.name)
        self.assertEqual(response.data['moves'][0]['move']['url'], '{}{}/move/{}/'.format(test_host, api_v2, pokemon_move.move.pk))
        self.assertEqual(response.data['moves'][0]['version_group_details'][0]['level_learned_at'], pokemon_move.level)
        self.assertEqual(response.data['moves'][0]['version_group_details'][0]['version_group']['name'], pokemon_move.version_group.name)
        self.assertEqual(response.data['moves'][0]['version_group_details'][0]['version_group']['url'], '{}{}/version-group/{}/'.format(test_host, api_v2, pokemon_move.version_group.pk))
        self.assertEqual(response.data['moves'][0]['version_group_details'][0]['move_learn_method']['name'], pokemon_move.move_learn_method.name)
        self.assertEqual(response.data['moves'][0]['version_group_details'][0]['move_learn_method']['url'], '{}{}/move-learn-method/{}/'.format(test_host, api_v2, pokemon_move.move_learn_method.pk))
        
    def test_pokemon_form_api(self):

        pokemon_species = self.setup_pokemon_species_data()
        pokemon = self.setup_pokemon_data(pokemon_species=pokemon_species)
        pokemon_form = self.setup_pokemon_form_data(pokemon=pokemon, name='pkm form for base pkmn')

        response = self.client.get('{}/pokemon-form/{}/'.format(api_v2, pokemon_form.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], pokemon_form.pk)
        self.assertEqual(response.data['name'], pokemon_form.name)
        self.assertEqual(response.data['form_name'], pokemon_form.form_name)
        self.assertEqual(response.data['order'], pokemon_form.order)
        self.assertEqual(response.data['form_order'], pokemon_form.form_order)
        self.assertEqual(response.data['is_default'], pokemon_form.is_default)
        self.assertEqual(response.data['is_battle_only'], pokemon_form.is_battle_only)
        self.assertEqual(response.data['is_mega'], pokemon_form.is_mega)
        # pokemon params
        self.assertEqual(response.data['pokemon']['name'], pokemon.name)
        self.assertEqual(response.data['pokemon']['url'], '{}{}/pokemon/{}/'.format(test_host, api_v2, pokemon.pk))
        # version group params
        self.assertEqual(response.data['version_group']['name'], pokemon_form.version_group.name)
        self.assertEqual(response.data['version_group']['url'], '{}{}/version-group/{}/'.format(test_host, api_v2, pokemon_form.version_group.pk))
        


class EvolutionTests(EvolutionData, APITestCase):

    def test_evolution_trigger_api(self):

        evolution_trigger = self.setup_evolution_trigger_data(name='base evltn trgr')
        evolution_trigger_name = self.setup_evolution_trigger_name_data(evolution_trigger, name='base evltn trgr name')

        response = self.client.get('{}/evolution-trigger/{}/'.format(api_v2, evolution_trigger.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], evolution_trigger.pk)
        self.assertEqual(response.data['name'], evolution_trigger.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], evolution_trigger_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], evolution_trigger_name.language.name)
        self.assertEqual(response.data['names'][0]['language']['url'], '{}{}/language/{}/'.format(test_host, api_v2, evolution_trigger_name.language.pk))
        
    def test_evolution_chain_api(self):

        baby_trigger_item = self.setup_item_data(name="bby itm for evo chn")
        evolution_chain = self.setup_evolution_chain_data(baby_trigger_item=baby_trigger_item)

        baby = self.setup_pokemon_species_data(name="bby for evo chn", is_baby=True, evolution_chain=evolution_chain)

        basic = self.setup_pokemon_species_data(name="bsc for evo chn", evolves_from_species=baby, evolution_chain=evolution_chain)
        basic_location = self.setup_location_data(name='lctn for bsc evo chn')
        basic_evolution = self.setup_pokemon_evolution_data(evolved_species=basic, min_level=5, location=basic_location)

        stage_one = self.setup_pokemon_species_data(name="stg one for evo chn", evolves_from_species=basic, evolution_chain=evolution_chain)
        stage_one_held_item = self.setup_item_data(name='itm for stg one evo chn')
        stage_one_evolution = self.setup_pokemon_evolution_data(evolved_species=stage_one, min_level=18, held_item=stage_one_held_item)

        stage_two_first = self.setup_pokemon_species_data(name="stg two frst for evo chn", evolves_from_species=stage_one, evolution_chain=evolution_chain)
        stage_two_first_known_move = self.setup_move_data(name="mv for evo chn")
        stage_two_first_evolution = self.setup_pokemon_evolution_data(evolved_species=stage_two_first, min_level=32, known_move=stage_two_first_known_move,)

        stage_two_second = self.setup_pokemon_species_data(name="stg two scnd for evo chn", evolves_from_species=stage_one, evolution_chain=evolution_chain)
        stage_two_second_party_type = self.setup_type_data(name="tp for evo chn")
        stage_two_second_evolution = self.setup_pokemon_evolution_data(evolved_species=stage_two_second, min_level=32, party_type=stage_two_second_party_type)

        response = self.client.get('{}/evolution-chain/{}/'.format(api_v2, evolution_chain.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        baby_data = response.data['chain']
        basic_data = baby_data['evolves_to'][0]
        stage_one_data = basic_data['evolves_to'][0]
        stage_two_first_data = stage_one_data['evolves_to'][0]
        stage_two_second_data = stage_one_data['evolves_to'][1]

        # base params
        self.assertEqual(response.data['id'], evolution_chain.pk)
        # baby trigger params
        self.assertEqual(response.data['baby_trigger_item']['name'], baby_trigger_item.name)
        self.assertEqual(response.data['baby_trigger_item']['url'], '{}{}/item/{}/'.format(test_host, api_v2, baby_trigger_item.pk))
        # baby params
        self.assertEqual(baby_data['is_baby'], baby.is_baby)
        self.assertEqual(baby_data['species']['name'], baby.name)
        self.assertEqual(baby_data['species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, baby.pk))
        # basic params
        self.assertEqual(basic_data['is_baby'], basic.is_baby)
        self.assertEqual(basic_data['species']['name'], basic.name)
        self.assertEqual(basic_data['species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, basic.pk))
        self.assertEqual(basic_data['evolution_details']['min_level'], basic_evolution.min_level)
        self.assertEqual(basic_data['evolution_details']['location']['name'], basic_location.name)
        self.assertEqual(basic_data['evolution_details']['location']['url'], '{}{}/location/{}/'.format(test_host, api_v2, basic_location.pk))
        # stage one params
        self.assertEqual(stage_one_data['is_baby'], stage_one.is_baby)
        self.assertEqual(stage_one_data['species']['name'], stage_one.name)
        self.assertEqual(stage_one_data['species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, stage_one.pk))
        self.assertEqual(stage_one_data['evolution_details']['min_level'], stage_one_evolution.min_level)
        self.assertEqual(stage_one_data['evolution_details']['held_item']['name'], stage_one_held_item.name)
        self.assertEqual(stage_one_data['evolution_details']['held_item']['url'], '{}{}/item/{}/'.format(test_host, api_v2, stage_one_held_item.pk))
        # stage two first params
        self.assertEqual(stage_two_first_data['is_baby'], stage_two_first.is_baby)
        self.assertEqual(stage_two_first_data['species']['name'], stage_two_first.name)
        self.assertEqual(stage_two_first_data['species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, stage_two_first.pk))
        self.assertEqual(stage_two_first_data['evolution_details']['min_level'], stage_two_first_evolution.min_level)
        self.assertEqual(stage_two_first_data['evolution_details']['known_move']['name'], stage_two_first_known_move.name)
        self.assertEqual(stage_two_first_data['evolution_details']['known_move']['url'], '{}{}/move/{}/'.format(test_host, api_v2, stage_two_first_known_move.pk))
        # stage two second params
        self.assertEqual(stage_two_second_data['is_baby'], stage_two_second.is_baby)
        self.assertEqual(stage_two_second_data['species']['name'], stage_two_second.name)
        self.assertEqual(stage_two_second_data['species']['url'], '{}{}/pokemon-species/{}/'.format(test_host, api_v2, stage_two_second.pk))
        self.assertEqual(stage_two_second_data['evolution_details']['min_level'], stage_two_second_evolution.min_level)
        self.assertEqual(stage_two_second_data['evolution_details']['party_type']['name'], stage_two_second_party_type.name)
        self.assertEqual(stage_two_second_data['evolution_details']['party_type']['url'], '{}{}/type/{}/'.format(test_host, api_v2, stage_two_second_party_type.pk))
