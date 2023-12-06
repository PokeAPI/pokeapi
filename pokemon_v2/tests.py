import json
from rest_framework import status
from rest_framework.test import APITestCase
from pokemon_v2.models import *

# pylint: disable=redefined-builtin

TEST_HOST = "http://testserver"
API_V2 = "/api/v2"


class APIData:
    """Data Initializers"""

    # Gender Data
    @classmethod
    def setup_gender_data(cls, name="gndr"):
        gender = Gender.objects.create(
            name=name,
        )
        gender.save()

        return gender

    # Language Data
    @classmethod
    def setup_language_data(cls, name="lang"):
        language = Language.objects.create(
            iso639="ts",
            iso3166="tt",
            name=name,
            official=True,
            order=1,
        )
        language.save()

        return language

    @classmethod
    def setup_language_name_data(cls, language, name="lang nm"):
        local_language = cls.setup_language_data(name="lang for " + name)

        language_name = LanguageName.objects.create(
            language=language, local_language=local_language, name=name
        )
        language_name.save()

        return language_name

    # Region Data
    @classmethod
    def setup_region_data(cls, name="reg"):
        region = Region.objects.create(name=name)
        region.save()

        return region

    @classmethod
    def setup_region_name_data(cls, region, name="reg nm"):
        language = cls.setup_language_data(name="lang for " + name)

        region_name = RegionName.objects.create(
            region=region, language=language, name=name
        )
        region_name.save()

        return region_name

    # Generation Data
    @classmethod
    def setup_generation_data(cls, region=None, name="gen"):
        region = region or cls.setup_region_data(name="reg for " + name)

        generation = Generation.objects.create(region=region, name=name)
        generation.save()

        return generation

    @classmethod
    def setup_generation_name_data(cls, generation, name="gen nm"):
        language = cls.setup_language_data(name="lang for " + name)

        generation_name = GenerationName.objects.create(
            generation=generation, language=language, name=name
        )
        generation_name.save()

        return generation_name

    # Version Data
    @classmethod
    def setup_version_group_data(cls, name="ver grp", generation=None):
        generation = generation or cls.setup_generation_data(name="gen for " + name)

        version_group = VersionGroup.objects.create(
            name=name, generation=generation, order=1
        )
        version_group.save()

        return version_group

    @classmethod
    def setup_version_group_region_data(cls, version_group=None, region=None):
        version_group_region = VersionGroupRegion.objects.create(
            version_group=version_group, region=region
        )
        version_group_region.save()

        return version_group_region

    @classmethod
    def setup_version_data(cls, version_group=None, name="ver"):
        version = Version.objects.create(
            name=name,
            version_group=version_group,
        )
        version.save()

        return version

    @classmethod
    def setup_version_name_data(cls, version, name="ver nm"):
        language = cls.setup_language_data(name="lang for " + name)

        version_name = VersionName.objects.create(
            version=version, language=language, name=name
        )
        version_name.save()

        return version_name

    # Ability Data
    @classmethod
    def setup_ability_data(cls, name="ablty", generation=None):
        generation = generation or cls.setup_generation_data(name="gen for " + name)

        ability = Ability.objects.create(
            name=name, generation=generation, is_main_series=False
        )
        ability.save()

        return ability

    @classmethod
    def setup_ability_name_data(cls, ability, name="ablty nm"):
        language = cls.setup_language_data(name="lang for " + name)

        ability_name = AbilityName.objects.create(
            ability=ability, language=language, name=name
        )
        ability_name.save()

        return ability_name

    @classmethod
    def setup_ability_effect_text_data(
        cls, ability, short_effect="ablty shrt efct", effect="ablty efct"
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        ability_effect_text = AbilityEffectText.objects.create(
            ability=ability, language=language, short_effect=short_effect, effect=effect
        )
        ability_effect_text.save()

        return ability_effect_text

    @classmethod
    def setup_ability_change_data(cls, ability):
        version_group = cls.setup_version_group_data(name="ver grp for ablty chng")

        ability_change = AbilityChange.objects.create(
            ability=ability, version_group=version_group
        )
        ability_change.save()

        return ability_change

    @classmethod
    def setup_ability_change_effect_text_data(
        cls, ability_change, effect="ablty change efct"
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        ability_change_effect_text = AbilityChangeEffectText.objects.create(
            ability_change=ability_change, language=language, effect=effect
        )
        ability_change_effect_text.save()

        return ability_change_effect_text

    @classmethod
    def setup_ability_flavor_text_data(cls, ability, flavor_text="ablty flvr txt"):
        version_group = cls.setup_version_group_data(name="ver grp for " + flavor_text)

        language = cls.setup_language_data(name="lang for " + flavor_text)

        ability_flavor_text = AbilityFlavorText.objects.create(
            ability=ability,
            version_group=version_group,
            language=language,
            flavor_text=flavor_text,
        )
        ability_flavor_text.save()

        return ability_flavor_text

    # Item Data
    @classmethod
    def setup_item_attribute_data(cls, name="itm attr"):
        item_attribute = ItemAttribute.objects.create(
            name=name,
        )
        item_attribute.save()

        return item_attribute

    @classmethod
    def setup_item_attribute_name_data(cls, item_attribute, name="itm attr nm"):
        language = cls.setup_language_data(name="lang for " + name)

        item_attribute_name = ItemAttributeName.objects.create(
            item_attribute=item_attribute, name=name, language=language
        )
        item_attribute_name.save()

        return item_attribute_name

    @classmethod
    def setup_item_attribute_description_data(
        cls, item_attribute, description="itm attr desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        item_attribute_description = ItemAttributeDescription.objects.create(
            item_attribute=item_attribute, description=description, language=language
        )
        item_attribute_description.save()

        return item_attribute_description

    @classmethod
    def setup_item_attribute_map_data(cls, item, item_attribute):
        item_attribute_map = ItemAttributeMap(item=item, item_attribute=item_attribute)
        item_attribute_map.save()

        return item_attribute_map

    @classmethod
    def setup_item_fling_effect_data(cls, name="itm flng efct"):
        item_fling_effect = ItemFlingEffect.objects.create(
            name=name,
        )
        item_fling_effect.save()

        return item_fling_effect

    @classmethod
    def setup_item_fling_effect_effect_text_data(
        cls, item_fling_effect, effect="itm flng efct efct txt"
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        item_fling_effect_effect_text = ItemFlingEffectEffectText.objects.create(
            item_fling_effect=item_fling_effect, effect=effect, language=language
        )
        item_fling_effect_effect_text.save()

        return item_fling_effect_effect_text

    @classmethod
    def setup_item_pocket_data(cls, name="itm pkt"):
        item_pocket = ItemPocket.objects.create(
            name=name,
        )
        item_pocket.save()

        return item_pocket

    @classmethod
    def setup_item_pocket_name_data(cls, item_pocket, name="itm pkt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        item_pocket_name = ItemPocketName.objects.create(
            item_pocket=item_pocket, name=name, language=language
        )
        item_pocket_name.save()

        return item_pocket_name

    @classmethod
    def setup_item_category_data(cls, name="itm ctgry", item_pocket=None):
        item_pocket = item_pocket or cls.setup_item_pocket_data(
            name="itm pkt for " + name
        )

        item_category = ItemCategory.objects.create(name=name, item_pocket=item_pocket)
        item_category.save()

        return item_category

    @classmethod
    def setup_item_category_name_data(cls, item_category, name="itm ctgry nm"):
        language = cls.setup_language_data(name="lang for " + name)

        item_category_name = ItemCategoryName.objects.create(
            item_category=item_category, name=name, language=language
        )
        item_category_name.save()

        return item_category_name

    @classmethod
    def setup_item_sprites_data(cls, item, default=True):
        sprite_path = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%s.png"

        sprites = {
            "default": sprite_path % item.id if default else None,
        }

        item_sprites = ItemSprites.objects.create(
            item=item, sprites=json.dumps(sprites)
        )
        item_sprites.save()

        return item_sprites

    @classmethod
    def setup_item_data(
        cls,
        item_category=None,
        item_fling_effect=None,
        name="itm",
        cost=100,
        fling_power=100,
    ):
        item = Item.objects.create(
            name=name,
            item_category=item_category,
            cost=cost,
            fling_power=fling_power,
            item_fling_effect=item_fling_effect,
        )
        item.save()

        return item

    @classmethod
    def setup_item_name_data(cls, item, name="itm nm"):
        language = cls.setup_language_data(name="lang for " + name)

        item_name = ItemName.objects.create(item=item, name=name, language=language)
        item_name.save()

        return item_name

    @classmethod
    def setup_item_effect_text_data(
        cls, item, short_effect="ablty shrt efct", effect="ablty efct"
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        item_effect_text = ItemEffectText.objects.create(
            item=item, language=language, short_effect=short_effect, effect=effect
        )
        item_effect_text.save()

        return item_effect_text

    @classmethod
    def setup_item_flavor_text_data(cls, item, flavor_text="itm flvr txt"):
        version_group = cls.setup_version_group_data(name="ver grp for " + flavor_text)

        language = cls.setup_language_data(name="lang for " + flavor_text)

        item_flavor_text = ItemFlavorText.objects.create(
            item=item,
            version_group=version_group,
            language=language,
            flavor_text=flavor_text,
        )
        item_flavor_text.save()

        return item_flavor_text

    @classmethod
    def setup_item_game_index_data(cls, item, game_index=0):
        generation = cls.setup_generation_data(name="gen for itm gm indx")

        item_game_index = ItemGameIndex.objects.create(
            item=item, game_index=game_index, generation=generation
        )
        item_game_index.save()

        return item_game_index

    # Contest Data
    @classmethod
    def setup_contest_type_data(cls, name="cntst tp"):
        contest_type = ContestType.objects.create(
            name=name,
        )
        contest_type.save()

        return contest_type

    @classmethod
    def setup_contest_type_name_data(cls, contest_type, name="cntst tp nm"):
        language = cls.setup_language_data(name="lang for " + name)

        contest_type_name = ContestTypeName.objects.create(
            language=language, name=name, contest_type=contest_type
        )
        contest_type_name.save()

        return contest_type_name

    @classmethod
    def setup_contest_effect_data(cls, appeal=2, jam=0):
        contest_effect = ContestEffect.objects.create(appeal=appeal, jam=jam)
        contest_effect.save()

        return contest_effect

    @classmethod
    def setup_contest_effect_flavor_text_data(
        cls, contest_effect, flavor_text="cntst efct flvr txt"
    ):
        language = cls.setup_language_data(name="lang for " + flavor_text)

        contest_effect_flavor_text = ContestEffectFlavorText.objects.create(
            language=language, flavor_text=flavor_text, contest_effect=contest_effect
        )
        contest_effect_flavor_text.save()

        return contest_effect_flavor_text

    @classmethod
    def setup_contest_effect_effect_text_data(
        cls, contest_effect, effect="cntst efct efct txt"
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        contest_effect_effect_text = ContestEffectEffectText.objects.create(
            language=language, effect=effect, contest_effect=contest_effect
        )
        contest_effect_effect_text.save()

        return contest_effect_effect_text

    @classmethod
    def setup_super_contest_effect_data(cls, appeal=2):
        super_contest_effect = SuperContestEffect.objects.create(
            appeal=appeal,
        )
        super_contest_effect.save()

        return super_contest_effect

    @classmethod
    def setup_super_contest_effect_flavor_text_data(
        cls, super_contest_effect, flavor_text="spr cntst efct flvr txt"
    ):
        language = cls.setup_language_data(name="lang for " + flavor_text)

        super_contest_effect_flavor_text = SuperContestEffectFlavorText.objects.create(
            language=language,
            flavor_text=flavor_text,
            super_contest_effect=super_contest_effect,
        )
        super_contest_effect_flavor_text.save()

        return super_contest_effect_flavor_text

    # Berry Data
    @classmethod
    def setup_berry_flavor_data(cls, contest_type=None, name="bry flvr"):
        contest_type = contest_type or cls.setup_contest_type_data(
            name="cntst tp for bry flvr"
        )

        berry_flavor = BerryFlavor.objects.create(name=name, contest_type=contest_type)
        berry_flavor.save()

        return berry_flavor

    @classmethod
    def setup_berry_flavor_name_data(cls, berry_flavor, name="bry flvr nm"):
        language = cls.setup_language_data(name="lang for " + name)

        berry_flavor_name = BerryFlavorName.objects.create(
            language=language, name=name, berry_flavor=berry_flavor
        )
        berry_flavor_name.save()

        return berry_flavor_name

    @classmethod
    def setup_berry_firmness_data(cls, name="bry frmns"):
        berry_firmness = BerryFirmness.objects.create(
            name=name,
        )
        berry_firmness.save()

        return berry_firmness

    @classmethod
    def setup_berry_firmness_name_data(cls, berry_firmness, name="bry frmns nm"):
        language = cls.setup_language_data(name="lang for " + name)

        berry_firmness_name = BerryFirmnessName.objects.create(
            language=language, name=name, berry_firmness=berry_firmness
        )
        berry_firmness_name.save()

        return berry_firmness_name

    @classmethod
    def setup_berry_flavor_map_data(cls, berry, berry_flavor, potency=20):
        berry_flavor_map = BerryFlavorMap(
            berry=berry, berry_flavor=berry_flavor, potency=potency
        )
        berry_flavor_map.save()

        return berry_flavor_map

    @classmethod
    def setup_berry_data(
        cls,
        berry_firmness=None,
        item=None,
        natural_gift_type=None,
        name="bry",
        natural_gift_power=50,
        size=20,
        max_harvest=5,
        growth_time=2,
        soil_dryness=15,
        smoothness=25,
    ):
        item = item or cls.setup_item_data(name="itm for " + name)

        berry_firmness = berry_firmness or cls.setup_berry_firmness_data(
            name="bry frmns for " + name
        )

        berry = Berry.objects.create(
            name=name,
            item=item,
            berry_firmness=berry_firmness,
            natural_gift_power=natural_gift_power,
            natural_gift_type=natural_gift_type,
            size=size,
            max_harvest=max_harvest,
            growth_time=growth_time,
            soil_dryness=soil_dryness,
            smoothness=smoothness,
        )
        berry.save()

        return berry

    # Egg Group Data
    @classmethod
    def setup_egg_group_data(cls, name="egg grp"):
        egg_group = EggGroup.objects.create(
            name=name,
        )
        egg_group.save()

        return egg_group

    @classmethod
    def setup_egg_group_name_data(cls, egg_group, name="ntr nm"):
        language = cls.setup_language_data(name="lang for " + name)

        egg_group_name = EggGroupName.objects.create(
            egg_group=egg_group, language=language, name=name
        )
        egg_group_name.save()

        return egg_group_name

    # Growth Rate Data
    @classmethod
    def setup_growth_rate_data(cls, name="grth rt", formula="pie*1000"):
        growth_rate = GrowthRate(name=name, formula=formula)
        growth_rate.save()

        return growth_rate

    @classmethod
    def setup_growth_rate_description_data(
        cls, growth_rate, description="grth rt desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        growth_rate_description = GrowthRateDescription.objects.create(
            growth_rate=growth_rate, description=description, language=language
        )
        growth_rate_description.save()

        return growth_rate_description

    # Location Data
    @classmethod
    def setup_location_data(cls, region=None, name="lctn"):
        region = region or cls.setup_region_data(name="rgn for " + name)

        location = Location(name=name, region=region)
        location.save()

        return location

    @classmethod
    def setup_location_game_index_data(cls, location, game_index=0):
        generation = cls.setup_generation_data(name="gen for itm gm indx")

        location_game_index = LocationGameIndex.objects.create(
            location=location, game_index=game_index, generation=generation
        )
        location_game_index.save()

        return location_game_index

    @classmethod
    def setup_location_name_data(cls, location, name="lctn nm"):
        language = cls.setup_language_data(name="lang for " + name)

        location_name = LocationName.objects.create(
            language=language, name=name, location=location
        )
        location_name.save()

        return location_name

    @classmethod
    def setup_location_area_data(cls, location=None, name="lctn area", game_index=0):
        location = location or cls.setup_location_data(name="lctn for " + name)

        location_area = LocationArea(
            location=location, name=name, game_index=game_index
        )
        location_area.save()

        return location_area

    @classmethod
    def setup_location_area_name_data(cls, location_area, name="lctn area nm"):
        language = cls.setup_language_data(name="lang for " + name)

        location_area_name = LocationAreaName.objects.create(
            language=language, name=name, location_area=location_area
        )
        location_area_name.save()

        return location_area_name

    # Type Data
    @classmethod
    def setup_type_data(cls, name="tp", move_damage_class=None, generation=None):
        move_damage_class = move_damage_class or cls.setup_move_damage_class_data(
            name="mv dmg cls for " + name
        )

        generation = generation or cls.setup_generation_data(name="rgn for " + name)

        type = Type(
            name=name, generation=generation, move_damage_class=move_damage_class
        )
        type.save()

        return type

    @classmethod
    def setup_type_name_data(cls, type, name="tp nm"):
        language = cls.setup_language_data(name="lang for " + name)

        type_name = TypeName.objects.create(language=language, name=name, type=type)
        type_name.save()

        return type_name

    @classmethod
    def setup_type_game_index_data(cls, type, game_index=0):
        generation = cls.setup_generation_data(name="gen for tp gm indx")

        type_game_index = TypeGameIndex.objects.create(
            type=type, game_index=game_index, generation=generation
        )
        type_game_index.save()

        return type_game_index

    # Move Data
    @classmethod
    def setup_move_ailment_data(cls, name="mv almnt"):
        move_ailment = MoveMetaAilment.objects.create(name=name)
        move_ailment.save()

        return move_ailment

    @classmethod
    def setup_move_ailment_name_data(cls, move_ailment, name="mv almnt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        move_ailment_name = MoveMetaAilmentName.objects.create(
            move_meta_ailment=move_ailment, language=language, name=name
        )
        move_ailment_name.save()

        return move_ailment_name

    @classmethod
    def setup_move_battle_style_data(cls, name="mv btl stl"):
        move_battle_style = MoveBattleStyle.objects.create(name=name)
        move_battle_style.save()

        return move_battle_style

    @classmethod
    def setup_move_battle_style_name_data(cls, move_battle_style, name="mv almnt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        move_battle_style_name = MoveBattleStyleName.objects.create(
            move_battle_style=move_battle_style, language=language, name=name
        )
        move_battle_style_name.save()

        return move_battle_style_name

    @classmethod
    def setup_move_category_data(cls, name="mv ctgry"):
        move_category = MoveMetaCategory.objects.create(name=name)
        move_category.save()

        return move_category

    @classmethod
    def setup_move_category_description_data(
        cls, move_category, description="mv ctgry desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        move_category_description = MoveMetaCategoryDescription.objects.create(
            move_meta_category=move_category, language=language, description=description
        )
        move_category_description.save()

        return move_category_description

    @classmethod
    def setup_move_effect_data(cls):
        move_effect = MoveEffect.objects.create()
        move_effect.save()

        return move_effect

    @classmethod
    def setup_move_effect_effect_text_data(
        cls,
        move_effect,
        effect="mv efct efct txt",
        short_effect="mv efct shrt efct txt",
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        effect_effect_text = MoveEffectEffectText.objects.create(
            effect=effect,
            short_effect=short_effect,
            move_effect=move_effect,
            language=language,
        )
        effect_effect_text.save()

        return effect_effect_text

    @classmethod
    def setup_move_damage_class_data(cls, name="mv dmg cls"):
        move_damage_class = MoveDamageClass.objects.create(name=name)
        move_damage_class.save()

        return move_damage_class

    @classmethod
    def setup_move_damage_class_name_data(cls, move_damage_class, name="mv dmg cls nm"):
        language = cls.setup_language_data(name="lang for " + name)

        move_damage_class_name = MoveDamageClassName.objects.create(
            move_damage_class=move_damage_class, language=language, name=name
        )
        move_damage_class_name.save()

        return move_damage_class_name

    @classmethod
    def setup_move_damage_class_description_data(
        cls, move_damage_class, description="mv dmg cls desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        move_damage_class_description = MoveDamageClassDescription.objects.create(
            move_damage_class=move_damage_class,
            language=language,
            description=description,
        )
        move_damage_class_description.save()

        return move_damage_class_description

    @classmethod
    def setup_move_learn_method_data(cls, name="mv lrn mthd"):
        move_learn_method = MoveLearnMethod.objects.create(name=name)
        move_learn_method.save()

        return move_learn_method

    @classmethod
    def setup_move_learn_method_name_data(
        cls, move_learn_method, name="mv lrn mthd nm"
    ):
        language = cls.setup_language_data(name="lang for " + name)

        move_learn_method_name = MoveLearnMethodName.objects.create(
            move_learn_method=move_learn_method, language=language, name=name
        )
        move_learn_method_name.save()

        return move_learn_method_name

    @classmethod
    def setup_move_learn_method_description_data(
        cls, move_learn_method, description="mv lrn mthd desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        move_learn_method_description = MoveLearnMethodDescription.objects.create(
            move_learn_method=move_learn_method,
            language=language,
            description=description,
        )
        move_learn_method_description.save()

        return move_learn_method_description

    @classmethod
    def setup_move_target_data(cls, name="mv trgt"):
        move_target = MoveTarget.objects.create(name=name)
        move_target.save()

        return move_target

    @classmethod
    def setup_move_target_name_data(cls, move_target, name="mv trgt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        move_target_name = MoveTargetName.objects.create(
            move_target=move_target, language=language, name=name
        )
        move_target_name.save()

        return move_target_name

    @classmethod
    def setup_move_target_description_data(
        cls, move_target, description="mv trgt desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        move_target_description = MoveTargetDescription.objects.create(
            move_target=move_target, language=language, description=description
        )
        move_target_description.save()

        return move_target_description

    @classmethod
    def setup_contest_combo_data(cls, first_move, second_move):
        contest_combo = ContestCombo.objects.create(
            first_move=first_move, second_move=second_move
        )
        contest_combo.save()

        return contest_combo

    @classmethod
    def setup_version_group_move_learn_method_data(
        cls, version_group=None, move_learn_method=None
    ):
        version_group_move_learn_method = VersionGroupMoveLearnMethod.objects.create(
            version_group=version_group, move_learn_method=move_learn_method
        )
        version_group_move_learn_method.save()

        return version_group_move_learn_method

    @classmethod
    def setup_super_contest_combo_data(cls, first_move, second_move):
        super_contest_combo = SuperContestCombo.objects.create(
            first_move=first_move, second_move=second_move
        )
        super_contest_combo.save()

        return super_contest_combo

    @classmethod
    def setup_move_flavor_text_data(cls, move, flavor_text="move flvr txt"):
        version_group = cls.setup_version_group_data(name="ver grp for " + flavor_text)

        language = cls.setup_language_data(name="lang for " + flavor_text)

        move_flavor_text = MoveFlavorText.objects.create(
            move=move,
            version_group=version_group,
            language=language,
            flavor_text=flavor_text,
        )
        move_flavor_text.save()

        return move_flavor_text

    @classmethod
    def setup_move_data(
        cls,
        contest_type=None,
        contest_effect=None,
        super_contest_effect=None,
        generation=None,
        move_damage_class=None,
        move_effect=None,
        move_target=None,
        type=None,
        name="mv",
        power=20,
        pp=20,
        accuracy=80,
        priority=0,
        effect_chance=50,
    ):
        contest_type = contest_type or cls.setup_contest_type_data(
            name="cntst tp for " + name
        )

        contest_effect = contest_effect or cls.setup_contest_effect_data()

        super_contest_effect = (
            super_contest_effect or cls.setup_super_contest_effect_data()
        )

        generation = generation or cls.setup_generation_data(name="gen for " + name)

        type = type or cls.setup_type_data(name="tp for " + name)

        move_target = move_target or cls.setup_move_target_data(
            name="mv trgt for " + name
        )

        move_damage_class = move_damage_class or cls.setup_move_damage_class_data(
            name="mv dmg cls for " + name
        )

        move = Move.objects.create(
            name=name,
            generation=generation,
            type=type,
            power=power,
            pp=pp,
            accuracy=accuracy,
            priority=priority,
            move_target=move_target,
            move_damage_class=move_damage_class,
            move_effect=move_effect,
            move_effect_chance=effect_chance,
            contest_type=contest_type,
            contest_effect=contest_effect,
            super_contest_effect=super_contest_effect,
        )
        move.save()

        return move

    @classmethod
    def setup_move_name_data(cls, move, name="mv nm"):
        language = cls.setup_language_data(name="lang for " + name)

        move_name = MoveName.objects.create(move=move, language=language, name=name)
        move_name.save()

        return move_name

    @classmethod
    def setup_move_meta_data(
        cls,
        move,
        move_ailment=None,
        move_category=None,
        min_hits=1,
        max_hits=1,
        min_turns=1,
        max_turns=1,
        drain=0,
        healing=0,
        crit_rate=0,
        ailment_chance=0,
        flinch_chance=0,
        stat_chance=0,
    ):
        move_ailment = move_ailment or cls.setup_move_ailment_data()

        move_category = move_category or cls.setup_move_category_data()

        move_meta = MoveMeta(
            move=move,
            move_meta_category=move_category,
            move_meta_ailment=move_ailment,
            min_hits=min_hits,
            max_hits=max_hits,
            min_turns=min_turns,
            max_turns=max_turns,
            drain=drain,
            healing=healing,
            crit_rate=crit_rate,
            ailment_chance=ailment_chance,
            flinch_chance=flinch_chance,
            stat_chance=stat_chance,
        )
        move_meta.save()

        return move_meta

    @classmethod
    def setup_move_change_data(
        cls,
        move=None,
        type=None,
        move_effect=None,
        version_group=None,
        power=20,
        pp=20,
        accuracy=80,
        effect_chance=50,
    ):
        version_group = version_group or cls.setup_version_group_data(
            name="ver grp for mv chng"
        )

        move_change = MoveChange.objects.create(
            move=move,
            version_group=version_group,
            type=type,
            power=power,
            pp=pp,
            accuracy=accuracy,
            move_effect=move_effect,
            move_effect_chance=effect_chance,
        )
        move_change.save()

        return move_change

    @classmethod
    def setup_move_effect_change_data(cls, move_effect=None):
        version_group = cls.setup_version_group_data(name="ver grp for mv chng")

        move_effect_change = MoveEffectChange.objects.create(
            move_effect=move_effect, version_group=version_group
        )
        move_effect_change.save()

        return move_effect_change

    @classmethod
    def setup_move_effect_change_effect_text_data(
        cls, move_effect_change=None, effect="mv efct chng efct txt"
    ):
        language = cls.setup_language_data(name="lang for " + effect)

        move_effect_change_effect_text = MoveEffectChangeEffectText.objects.create(
            move_effect_change=move_effect_change, language=language, effect=effect
        )
        move_effect_change_effect_text.save()

        return move_effect_change_effect_text

    # Stat Data
    @classmethod
    def setup_stat_data(cls, name="stt", is_battle_only=True, game_index=1):
        move_damage_class = cls.setup_move_damage_class_data(
            name="mv dmg cls for " + name
        )

        stat = Stat.objects.create(
            name=name,
            is_battle_only=is_battle_only,
            move_damage_class=move_damage_class,
            game_index=game_index,
        )
        stat.save()

        return stat

    @classmethod
    def setup_stat_name_data(cls, stat, name="stt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        stat_name = StatName.objects.create(stat=stat, language=language, name=name)
        stat_name.save()

        return stat_name

    @classmethod
    def setup_move_stat_change_data(cls, move, stat=None, change=1):
        stat = stat or cls.setup_stat_data(name="stt for mv")

        move_stat_change = MoveMetaStatChange.objects.create(
            move=move, stat=stat, change=change
        )
        move_stat_change.save()

        return move_stat_change

    @classmethod
    def setup_pokeathlon_stat_data(cls, name="pkathln stt"):
        pokeathlon_stat = PokeathlonStat.objects.create(name=name)
        pokeathlon_stat.save()

        return pokeathlon_stat

    @classmethod
    def setup_pokeathlon_stat_name_data(cls, pokeathlon_stat, name="pkathln stt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        pokeathlon_stat_name = PokeathlonStatName.objects.create(
            pokeathlon_stat=pokeathlon_stat, language=language, name=name
        )
        pokeathlon_stat_name.save()

        return pokeathlon_stat_name

    # Characteristic Data
    @classmethod
    def setup_characteristic_data(cls, gene_mod_5=0, stat=None):
        stat = stat or cls.setup_stat_data(name="stt for char")

        characteristic = Characteristic.objects.create(stat=stat, gene_mod_5=gene_mod_5)
        characteristic.save()

        return characteristic

    @classmethod
    def setup_characteristic_description_data(
        cls, characteristic, description="char desc"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        characteristic_description = CharacteristicDescription.objects.create(
            characteristic=characteristic, language=language, description=description
        )
        characteristic_description.save()

        return characteristic_description

    # Nature Data
    @classmethod
    def setup_nature_data(
        cls,
        decreased_stat=None,
        increased_stat=None,
        likes_flavor=None,
        hates_flavor=None,
        name="ntr",
        game_index=1,
    ):
        nature = Nature.objects.create(
            name=name,
            decreased_stat=decreased_stat,
            increased_stat=increased_stat,
            hates_flavor=hates_flavor,
            likes_flavor=likes_flavor,
            game_index=game_index,
        )
        nature.save()

        return nature

    @classmethod
    def setup_nature_name_data(cls, nature, name="ntr nm"):
        language = cls.setup_language_data(name="lang for " + name)

        nature_name = NatureName.objects.create(
            nature=nature, language=language, name=name
        )
        nature_name.save()

        return nature_name

    @classmethod
    def setup_nature_pokeathlon_stat_data(
        cls, nature=None, pokeathlon_stat=None, max_change=1
    ):
        nature_pokeathlon_stat = NaturePokeathlonStat.objects.create(
            nature=nature,
            pokeathlon_stat=pokeathlon_stat,
            max_change=max_change,
        )
        nature_pokeathlon_stat.save()

        return nature_pokeathlon_stat

    @classmethod
    def setup_nature_battle_style_preference_data(
        cls,
        nature=None,
        move_battle_style=None,
        low_hp_preference=10,
        high_hp_preference=20,
    ):
        nature_battle_style_preference = NatureBattleStylePreference.objects.create(
            nature=nature,
            move_battle_style=move_battle_style,
            low_hp_preference=low_hp_preference,
            high_hp_preference=high_hp_preference,
        )
        nature_battle_style_preference.save()

        return nature_battle_style_preference

    # Pokedex Data
    @classmethod
    def setup_pokedex_data(cls, region=None, name="pkdx"):
        region = region or cls.setup_region_data(name="rgn for " + name)

        pokedex = Pokedex.objects.create(
            name=name,
            region=region,
        )
        pokedex.save()

        return pokedex

    @classmethod
    def setup_pokedex_name_data(cls, pokedex, name="pkdx nm"):
        language = cls.setup_language_data(name="lang for " + name)

        pokedex_name = PokedexName.objects.create(
            pokedex=pokedex, language=language, name=name
        )
        pokedex_name.save()

        return pokedex_name

    @classmethod
    def setup_pokedex_description_data(cls, pokedex, description="pkdx desc"):
        language = cls.setup_language_data(name="lang for " + description)

        pokedex_description = PokedexDescription.objects.create(
            pokedex=pokedex, language=language, description=description
        )
        pokedex_description.save()

        return pokedex_description

    @classmethod
    def setup_pokedex_version_group_data(cls, pokedex, version_group=None):
        version_group = version_group or cls.setup_language_data(
            name="ver grp for pkdx"
        )

        pokedex_version_group = PokedexVersionGroup.objects.create(
            pokedex=pokedex, version_group=version_group
        )
        pokedex_version_group.save()

        return pokedex_version_group

    # Pokemon Data
    @classmethod
    def setup_pokemon_habitat_data(cls, name="pkm hbtt"):
        pokemon_habitat = PokemonHabitat.objects.create(
            name=name,
        )
        pokemon_habitat.save()

        return pokemon_habitat

    @classmethod
    def setup_pokemon_habitat_name_data(cls, pokemon_habitat, name="pkm hbtt nm"):
        language = cls.setup_language_data(name="lang for " + name)

        pokemon_habitat_name = PokemonHabitatName.objects.create(
            pokemon_habitat=pokemon_habitat, language=language, name=name
        )
        pokemon_habitat_name.save()

        return pokemon_habitat_name

    @classmethod
    def setup_pokemon_color_data(cls, name="pkm clr"):
        pokemon_color = PokemonColor.objects.create(
            name=name,
        )
        pokemon_color.save()

        return pokemon_color

    @classmethod
    def setup_pokemon_color_name_data(cls, pokemon_color, name="pkm clr nm"):
        language = cls.setup_language_data(name="lang for " + name)

        pokemon_color_name = PokemonColorName.objects.create(
            pokemon_color=pokemon_color, language=language, name=name
        )
        pokemon_color_name.save()

        return pokemon_color_name

    @classmethod
    def setup_pokemon_shape_data(cls, name="pkm shp"):
        pokemon_shape = PokemonShape.objects.create(
            name=name,
        )
        pokemon_shape.save()

        return pokemon_shape

    @classmethod
    def setup_pokemon_shape_name_data(
        cls, pokemon_shape, name="pkm shp nm", awesome_name="pkm shp awsm nm"
    ):
        language = cls.setup_language_data(name="lang for " + name)

        pokemon_shape_name = PokemonShapeName.objects.create(
            pokemon_shape=pokemon_shape,
            language=language,
            name=name,
            awesome_name=awesome_name,
        )
        pokemon_shape_name.save()

        return pokemon_shape_name

    @classmethod
    def setup_pokemon_species_form_description_data(
        cls, pokemon_species=None, description="pkm spcs frm dscr"
    ):
        language = cls.setup_language_data(name="lang for " + description)

        pokemon_species_form_description = PokemonSpeciesDescription.objects.create(
            pokemon_species=pokemon_species, language=language, description=description
        )
        pokemon_species_form_description.save()

        return pokemon_species_form_description

    @classmethod
    def setup_pokemon_species_flavor_text_data(
        cls, pokemon_species, flavor_text="pkmn spcs flvr txt"
    ):
        version = cls.setup_version_data(name="ver for " + flavor_text)

        language = cls.setup_language_data(name="lang for " + flavor_text)

        pokemon_species_flavor_text = PokemonSpeciesFlavorText.objects.create(
            pokemon_species=pokemon_species,
            version=version,
            language=language,
            flavor_text=flavor_text,
        )
        pokemon_species_flavor_text.save()

        return pokemon_species_flavor_text

    @classmethod
    def setup_pokemon_species_data(
        cls,
        generation=None,
        evolves_from_species=None,
        evolution_chain=None,
        growth_rate=None,
        pokemon_color=None,
        pokemon_habitat=None,
        pokemon_shape=None,
        name="pkm spcs",
        gender_rate=50,
        capture_rate=20,
        base_happiness=20,
        is_baby=False,
        hatch_counter=10,
        has_gender_differences=True,
        forms_switchable=False,
        is_legendary=False,
        is_mythical=False,
        order=1,
    ):
        generation = generation or cls.setup_generation_data(name="gen for " + name)

        growth_rate = growth_rate or cls.setup_growth_rate_data(
            name="grth rt for " + name
        )

        pokemon_shape = pokemon_shape or cls.setup_pokemon_shape_data(
            name="pkmn shp for " + name
        )

        pokemon_color = pokemon_color or cls.setup_pokemon_color_data(
            name="pkmn clr for " + name
        )

        pokemon_habitat = pokemon_habitat or cls.setup_pokemon_habitat_data(
            name="pkm hbtt for " + name
        )

        pokemon_species = PokemonSpecies.objects.create(
            name=name,
            generation=generation,
            evolves_from_species=evolves_from_species,
            evolution_chain=evolution_chain,
            pokemon_color=pokemon_color,
            pokemon_shape=pokemon_shape,
            pokemon_habitat=pokemon_habitat,
            gender_rate=gender_rate,
            capture_rate=capture_rate,
            base_happiness=base_happiness,
            is_baby=is_baby,
            hatch_counter=hatch_counter,
            has_gender_differences=has_gender_differences,
            growth_rate=growth_rate,
            forms_switchable=forms_switchable,
            is_legendary=is_legendary,
            is_mythical=is_mythical,
            order=order,
        )
        pokemon_species.save()

        return pokemon_species

    @classmethod
    def setup_pokemon_species_name_data(
        cls, pokemon_species, name="pkmn spcs nm", genus="pkmn spcs gns"
    ):
        language = cls.setup_language_data(name="lang for " + name)

        pokemon_species_name = PokemonSpeciesName.objects.create(
            pokemon_species=pokemon_species, language=language, name=name, genus=genus
        )
        pokemon_species_name.save()

        return pokemon_species_name

    @classmethod
    def setup_pokemon_dex_entry_data(cls, pokemon_species, pokedex, entry_number=100):
        dex_number = PokemonDexNumber(
            pokemon_species=pokemon_species,
            pokedex=pokedex,
            pokedex_number=entry_number,
        )
        dex_number.save()

        return dex_number

    @classmethod
    def setup_pokemon_egg_group_data(cls, pokemon_species, egg_group):
        pokemon_egg_group = PokemonEggGroup(
            pokemon_species=pokemon_species, egg_group=egg_group
        )
        pokemon_egg_group.save()

        return pokemon_egg_group

    @classmethod
    def setup_pokemon_data(
        cls,
        pokemon_species=None,
        name="pkmn",
        height=100,
        weight=100,
        base_experience=0,
        order=1,
        is_default=False,
    ):
        pokemon_species = pokemon_species or cls.setup_pokemon_species_data(
            name="pkmn spcs for " + name
        )

        pokemon = Pokemon.objects.create(
            name=name,
            pokemon_species=pokemon_species,
            height=height,
            weight=weight,
            base_experience=base_experience,
            order=order,
            is_default=is_default,
        )
        pokemon.save()

        return pokemon

    @classmethod
    def setup_pokemon_game_index_data(cls, pokemon, game_index=0):
        version = cls.setup_version_data(name="ver for pkmn gm indx")

        pokemon_game_index = PokemonGameIndex.objects.create(
            pokemon=pokemon, game_index=game_index, version=version
        )
        pokemon_game_index.save()

        return pokemon_game_index

    @classmethod
    def setup_pokemon_form_sprites_data(
        cls,
        pokemon_form,
        front_default=True,
        front_shiny=False,
        back_default=False,
        back_shiny=False,
    ):
        sprite_path = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%s.png"

        sprites = {
            "front_default": sprite_path % pokemon_form.id if front_default else None,
            "front_shiny": sprite_path % pokemon_form.id if front_shiny else None,
            "back_default": sprite_path % pokemon_form.id if back_default else None,
            "back_shiny": sprite_path % pokemon_form.id if back_shiny else None,
        }

        pokemon_form_sprites = PokemonFormSprites.objects.create(
            pokemon_form=pokemon_form, sprites=json.dumps(sprites)
        )
        pokemon_form_sprites.save()

        return pokemon_form_sprites

    @classmethod
    def setup_pokemon_form_type_data(cls, pokemon_form, type=None, slot=1):
        type = type or cls.setup_type_data(name="tp for pkmn frm")

        form_type = PokemonFormType(pokemon_form=pokemon_form, type=type, slot=slot)
        form_type.save()

        return form_type

    @classmethod
    def setup_pokemon_form_data(
        cls,
        pokemon,
        name="pkmn nrml frm",
        form_name="nrml",
        order=1,
        is_default=True,
        is_battle_only=True,
        form_order=1,
        is_mega=False,
    ):
        version_group = cls.setup_version_group_data(name="ver grp for " + name)

        pokemon_form = PokemonForm(
            name=name,
            form_name=form_name,
            pokemon=pokemon,
            version_group=version_group,
            is_default=is_default,
            is_battle_only=is_battle_only,
            is_mega=is_mega,
            form_order=form_order,
            order=order,
        )
        pokemon_form.save()

        return pokemon_form

    @classmethod
    def setup_pokemon_ability_data(cls, pokemon, ability=None, is_hidden=False, slot=1):
        ability = ability or cls.setup_ability_data(name="ablty for pkmn")

        pokemon_ability = PokemonAbility(
            pokemon=pokemon, ability=ability, is_hidden=is_hidden, slot=slot
        )
        pokemon_ability.save()

        return pokemon_ability

    @classmethod
    def setup_pokemon_past_ability_data(
        cls, pokemon, generation, ability=None, is_hidden=False, slot=1
    ):
        ability = ability or cls.setup_ability_data(name="ablty for pkmn")

        pokemon_ability_past = PokemonAbilityPast(
            pokemon=pokemon,
            generation=generation,
            ability=ability,
            is_hidden=is_hidden,
            slot=slot,
        )
        pokemon_ability_past.save()

        return pokemon_ability_past

    @classmethod
    def setup_pokemon_stat_data(cls, pokemon, base_stat=10, effort=10):
        stat = cls.setup_stat_data(name="stt for pkmn")

        pokemon_stat = PokemonStat(
            pokemon=pokemon, stat=stat, base_stat=base_stat, effort=effort
        )
        pokemon_stat.save()

        return pokemon_stat

    @classmethod
    def setup_pokemon_type_data(cls, pokemon, type=None, slot=1):
        type = type or cls.setup_type_data(name="tp for pkmn")

        pokemon_type = PokemonType(pokemon=pokemon, type=type, slot=slot)
        pokemon_type.save()

        return pokemon_type

    @classmethod
    def setup_pokemon_past_type_data(cls, pokemon, generation, type=None, slot=1):
        type = type or cls.setup_type_data(name="tp for pkmn")

        pokemon_type_past = PokemonTypePast(
            pokemon=pokemon, generation=generation, type=type, slot=slot
        )
        pokemon_type_past.save()

        return pokemon_type_past

    @classmethod
    def setup_pokemon_item_data(cls, pokemon=None, item=None, version=None, rarity=50):
        item = item or cls.setup_item_data(name="itm for pkmn")

        pokemon = pokemon or cls.setup_pokemon_data(name="pkmn for pkmn")

        version = version or cls.setup_version_data(name="ver grp for pkmn itm")

        pokemon_item = PokemonItem(
            pokemon=pokemon, version=version, item=item, rarity=rarity
        )
        pokemon_item.save()

        return pokemon_item

    @classmethod
    def setup_pokemon_move_data(cls, pokemon, move, version_group, level=0, order=1):
        move_learn_method = cls.setup_move_learn_method_data(
            name="mv lrn mthd for pkmn"
        )

        pokemon_move = PokemonMove.objects.create(
            pokemon=pokemon,
            version_group=version_group,
            move=move,
            move_learn_method=move_learn_method,
            level=level,
            order=order,
        )
        pokemon_move.save()

        return pokemon_move

    @classmethod
    def setup_pokemon_sprites_data(
        cls,
        pokemon,
        front_default=True,
        front_female=False,
        front_shiny=False,
        front_shiny_female=False,
        back_default=False,
        back_female=False,
        back_shiny=False,
        back_shiny_female=False,
    ):
        sprite_path = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%s.png"

        sprites = {
            "front_default": sprite_path % pokemon.id if front_default else None,
            "front_female": sprite_path % pokemon.id if front_female else None,
            "front_shiny": sprite_path % pokemon.id if front_shiny else None,
            "front_shiny_female": sprite_path % pokemon.id
            if front_shiny_female
            else None,
            "back_default": sprite_path % pokemon.id if back_default else None,
            "back_female": sprite_path % pokemon.id if back_female else None,
            "back_shiny": sprite_path % pokemon.id if back_shiny else None,
            "back_shiny_female": sprite_path % pokemon.id
            if back_shiny_female
            else None,
        }

        pokemon_sprites = PokemonSprites.objects.create(
            pokemon=pokemon, sprites=json.dumps(sprites)
        )
        pokemon_sprites.save()

        return pokemon_sprites

    # Evolution Data
    @classmethod
    def setup_evolution_trigger_data(cls, name="evltn trgr"):
        evolution_trigger = EvolutionTrigger.objects.create(
            name=name,
        )
        evolution_trigger.save()

        return evolution_trigger

    @classmethod
    def setup_evolution_trigger_name_data(cls, evolution_trigger, name="evltn trgr nm"):
        language = cls.setup_language_data(name="lang for " + name)

        evolution_trigger_name = EvolutionTriggerName.objects.create(
            evolution_trigger=evolution_trigger, language=language, name=name
        )
        evolution_trigger_name.save()

        return evolution_trigger_name

    @classmethod
    def setup_evolution_chain_data(cls, baby_trigger_item=None):
        evolution_chain = EvolutionChain.objects.create(
            baby_trigger_item=baby_trigger_item,
        )
        evolution_chain.save()

        return evolution_chain

    @classmethod
    def setup_pokemon_evolution_data(
        cls,
        evolved_species=None,
        evolution_trigger=None,
        party_species=None,
        trade_species=None,
        evolution_item=None,
        party_type=None,
        min_level=0,
        gender=None,
        location=None,
        held_item=None,
        time_of_day="",
        known_move=None,
        known_move_type=None,
        min_happiness=0,
        min_beauty=0,
        min_affection=0,
        relative_physical_stats=0,
        needs_overworld_rain=False,
        turn_upside_down=False,
    ):
        evolved_species = evolved_species or cls.setup_pokemon_species_data(
            name="pkmn spcs for pkmn evltn"
        )

        evolution_trigger = evolution_trigger or cls.setup_evolution_trigger_data(
            name="evltn trgr for pkmn evltn"
        )

        pokemon_evolution = PokemonEvolution.objects.create(
            evolved_species=evolved_species,
            evolution_trigger=evolution_trigger,
            evolution_item=evolution_item,
            min_level=min_level,
            gender=gender,
            location=location,
            held_item=held_item,
            time_of_day=time_of_day,
            known_move=known_move,
            known_move_type=known_move_type,
            min_happiness=min_happiness,
            min_beauty=min_beauty,
            min_affection=min_affection,
            relative_physical_stats=relative_physical_stats,
            party_species=party_species,
            party_type=party_type,
            trade_species=trade_species,
            needs_overworld_rain=needs_overworld_rain,
            turn_upside_down=turn_upside_down,
        )
        pokemon_evolution.save()

        return pokemon_evolution

    # Encounter Data
    @classmethod
    def setup_encounter_method_data(cls, name="encntr mthd", order=0):
        encounter_method = EncounterMethod.objects.create(name=name, order=order)
        encounter_method.save()

        return encounter_method

    @classmethod
    def setup_encounter_method_name_data(cls, encounter_method, name="encntr mthd nm"):
        language = cls.setup_language_data(name="lang for " + name)

        encounter_method_name = EncounterMethodName.objects.create(
            encounter_method=encounter_method, language=language, name=name
        )
        encounter_method_name.save()

        return encounter_method_name

    @classmethod
    def setup_encounter_condition_data(cls, name="encntr cndtn"):
        encounter_condition = EncounterCondition.objects.create(name=name)
        encounter_condition.save()

        return encounter_condition

    @classmethod
    def setup_encounter_condition_name_data(
        cls, encounter_condition, name="encntr cndtn nm"
    ):
        language = cls.setup_language_data(name="lang for " + name)

        encounter_condition_name = EncounterConditionName.objects.create(
            encounter_condition=encounter_condition, language=language, name=name
        )
        encounter_condition_name.save()

        return encounter_condition_name

    @classmethod
    def setup_encounter_condition_value_data(
        cls, encounter_condition, name="encntr cndtn vlu", is_default=False
    ):
        encounter_condition_value = EncounterConditionValue.objects.create(
            encounter_condition=encounter_condition, name=name, is_default=is_default
        )
        encounter_condition_value.save()

        return encounter_condition_value

    @classmethod
    def setup_encounter_condition_value_name_data(
        cls, encounter_condition_value, name="encntr cndtn vlu nm"
    ):
        language = cls.setup_language_data(name="lang for " + name)

        encounter_condition_value_name = EncounterConditionValueName.objects.create(
            encounter_condition_value=encounter_condition_value,
            language=language,
            name=name,
        )
        encounter_condition_value_name.save()

        return encounter_condition_value_name

    @classmethod
    def setup_encounter_condition_value_map_data(
        cls, encounter, encounter_condition_value
    ):
        encounter_condition_value_map = EncounterConditionValue.objects.create(
            encounter=encounter, encounter_condition_value=encounter_condition_value
        )
        encounter_condition_value_map.save()

        return encounter_condition_value_map

    @classmethod
    def setup_encounter_slot_data(cls, encounter_method=None, slot=0, rarity=0):
        encounter_method = encounter_method or cls.setup_encounter_method_data(
            name="encntr mthd for encntr slt"
        )

        version_group = cls.setup_version_group_data(name="ver grp for encntr slt")

        encounter_slot = EncounterSlot.objects.create(
            encounter_method=encounter_method,
            version_group=version_group,
            slot=slot,
            rarity=rarity,
        )
        encounter_slot.save()

        return encounter_slot

    @classmethod
    def setup_location_area_encounter_rate_data(
        cls, location_area, encounter_method, rate=0
    ):
        version = cls.setup_version_data(name="ver for lctn area")

        location_area_encounter_rate = LocationAreaEncounterRate.objects.create(
            encounter_method=encounter_method,
            version=version,
            location_area=location_area,
            rate=rate,
        )
        location_area_encounter_rate.save()

        return location_area_encounter_rate

    @classmethod
    def setup_encounter_data(
        cls,
        location_area=None,
        encounter_slot=None,
        pokemon=None,
        version=None,
        min_level=10,
        max_level=15,
    ):
        location_area = location_area or cls.setup_location_area_data(
            name="ver for encntr"
        )

        encounter_slot = encounter_slot or cls.setup_encounter_slot_data()

        pokemon = pokemon or cls.setup_pokemon_data(name="pkmn for encntr")

        version = version or cls.setup_version_data(name="ver for encntr")

        encounter = Encounter.objects.create(
            version=version,
            location_area=location_area,
            encounter_slot=encounter_slot,
            pokemon=pokemon,
            min_level=min_level,
            max_level=max_level,
        )
        encounter.save()

        return encounter

    # Pal Park Data
    @classmethod
    def setup_pal_park_area_data(cls, name="pl prk area"):
        pal_park_area = PalParkArea.objects.create(name=name)
        pal_park_area.save()

        return pal_park_area

    @classmethod
    def setup_pal_park_area_name_data(cls, pal_park_area, name="pl prk area nm"):
        language = cls.setup_language_data(name="lang for " + name)

        pal_park_area_name = PalParkAreaName.objects.create(
            pal_park_area=pal_park_area, language=language, name=name
        )
        pal_park_area_name.save()

        return pal_park_area_name

    @classmethod
    def setup_pal_park_data(
        cls, pokemon_species=None, pal_park_area=None, base_score=10, rate=10
    ):
        pal_park_area = pal_park_area or cls.setup_pal_park_area_data(
            name="pl prk area"
        )

        pal_park = PalPark.objects.create(
            base_score=base_score,
            pokemon_species=pokemon_species,
            pal_park_area=pal_park_area,
            rate=rate,
        )
        pal_park.save()

        return pal_park


# Tests
class APITests(APIData, APITestCase):
    # Gender Tests
    def test_gender_api(self):
        gender = self.setup_gender_data(name="female")
        pokemon_species = self.setup_pokemon_species_data(
            name="pkmn spcs for gndr", gender_rate=8
        )
        evolved_species = self.setup_pokemon_species_data(
            name="evlvd pkmn spcs for gndr"
        )
        self.setup_pokemon_evolution_data(
            evolved_species=evolved_species, gender=gender
        )

        response = self.client.get("{}/gender/{}/".format(API_V2, gender.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], gender.pk)
        self.assertEqual(response.data["name"], gender.name)
        # species params
        self.assertEqual(
            response.data["pokemon_species_details"][0]["rate"],
            pokemon_species.gender_rate,
        )
        self.assertEqual(
            response.data["pokemon_species_details"][0]["pokemon_species"]["name"],
            pokemon_species.name,
        )
        self.assertEqual(
            response.data["pokemon_species_details"][0]["pokemon_species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )
        self.assertEqual(
            response.data["required_for_evolution"][0]["name"], evolved_species.name
        )
        self.assertEqual(
            response.data["required_for_evolution"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, evolved_species.pk),
        )

    # Language Tests
    def test_language_api(self):
        language = self.setup_language_data(name="base lang")
        language_name = self.setup_language_name_data(language, name="base lang name")

        response = self.client.get("{}/language/{}/".format(API_V2, language.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], language.pk)
        self.assertEqual(response.data["iso639"], language.iso639)
        self.assertEqual(response.data["iso3166"], language.iso3166)
        self.assertEqual(response.data["name"], language.name)
        self.assertEqual(response.data["official"], language.official)
        # name params
        self.assertEqual(response.data["names"][0]["name"], language_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            language_name.local_language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, language_name.local_language.pk
            ),
        )

    # Region Tests
    def test_region_api(self):
        region = self.setup_region_data(name="base reg")
        region_name = self.setup_region_name_data(region, name="base reg name")
        location = self.setup_location_data(region=region, name="lctn for base rgn")
        generation = self.setup_generation_data(
            region=region, name="gnrtn for base rgn"
        )
        pokedex = self.setup_pokedex_data(region=region, name="pkdx for base rgn")
        version_group = self.setup_version_group_data(name="ver grp for base rgn")
        self.setup_version_group_region_data(region=region, version_group=version_group)

        response = self.client.get("{}/region/{}/".format(API_V2, region.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], region.pk)
        self.assertEqual(response.data["name"], region.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], region_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], region_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, region_name.language.pk),
        )
        # location params
        self.assertEqual(response.data["locations"][0]["name"], location.name)
        self.assertEqual(
            response.data["locations"][0]["url"],
            "{}{}/location/{}/".format(TEST_HOST, API_V2, location.pk),
        )
        # generation params
        self.assertEqual(response.data["main_generation"]["name"], generation.name)
        self.assertEqual(
            response.data["main_generation"]["url"],
            "{}{}/generation/{}/".format(TEST_HOST, API_V2, generation.pk),
        )
        # pokedex params
        self.assertEqual(response.data["pokedexes"][0]["name"], pokedex.name)
        self.assertEqual(
            response.data["pokedexes"][0]["url"],
            "{}{}/pokedex/{}/".format(TEST_HOST, API_V2, pokedex.pk),
        )
        # version group params
        self.assertEqual(response.data["version_groups"][0]["name"], version_group.name)
        self.assertEqual(
            response.data["version_groups"][0]["url"],
            "{}{}/version-group/{}/".format(TEST_HOST, API_V2, version_group.pk),
        )

    # Generation Tests
    def test_generation_api(self):
        generation = self.setup_generation_data(name="base gen")
        generation_name = self.setup_generation_name_data(
            generation, name="base reg name"
        )
        ability = self.setup_ability_data(
            name="ablty for base gen", generation=generation
        )
        move = self.setup_move_data(name="mv for base gen", generation=generation)
        pokemon_species = self.setup_pokemon_species_data(
            name="pkmn spcs for base gen", generation=generation
        )
        type = self.setup_type_data(name="tp for base gen", generation=generation)
        version_group = self.setup_version_group_data(
            name="ver grp for base gen", generation=generation
        )

        response = self.client.get("{}/generation/{}/".format(API_V2, generation.pk))

        # base params
        self.assertEqual(response.data["id"], generation.pk)
        self.assertEqual(response.data["name"], generation.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], generation_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], generation_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, generation_name.language.pk),
        )
        # region params
        self.assertEqual(response.data["main_region"]["name"], generation.region.name)
        self.assertEqual(
            response.data["main_region"]["url"],
            "{}{}/region/{}/".format(TEST_HOST, API_V2, generation.region.pk),
        )
        # ability params
        self.assertEqual(response.data["abilities"][0]["name"], ability.name)
        self.assertEqual(
            response.data["abilities"][0]["url"],
            "{}{}/ability/{}/".format(TEST_HOST, API_V2, ability.pk),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )
        # type params
        self.assertEqual(response.data["types"][0]["name"], type.name)
        self.assertEqual(
            response.data["types"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, type.pk),
        )
        # species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )
        # version group params
        self.assertEqual(response.data["version_groups"][0]["name"], version_group.name)
        self.assertEqual(
            response.data["version_groups"][0]["url"],
            "{}{}/version-group/{}/".format(TEST_HOST, API_V2, version_group.pk),
        )

    # Version Tests
    def test_version_api(self):
        version_group = self.setup_version_group_data(name="ver grp for ver")
        version = self.setup_version_data(name="base ver", version_group=version_group)
        version_name = self.setup_version_name_data(version, name="base ver name")

        response = self.client.get("{}/version/{}/".format(API_V2, version.pk))

        # base params
        self.assertEqual(response.data["id"], version.pk)
        self.assertEqual(response.data["name"], version.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], version_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], version_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, version_name.language.pk),
        )
        # version group params
        self.assertEqual(
            response.data["version_group"]["name"], version.version_group.name
        )
        self.assertEqual(
            response.data["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, version.version_group.pk
            ),
        )

    def test_version_group_api(self):
        version_group = self.setup_version_group_data(name="base ver grp")
        move_learn_method = self.setup_move_learn_method_data(name="mv lrn mthd for ")
        self.setup_version_group_move_learn_method_data(
            version_group=version_group, move_learn_method=move_learn_method
        )
        region = self.setup_region_data(name="rgn for ver grp")
        version = self.setup_version_data(
            name="ver for base ver grp", version_group=version_group
        )
        self.setup_version_group_region_data(version_group=version_group, region=region)
        pokedex = self.setup_pokedex_data(name="pkdx for base ver group")
        self.setup_pokedex_version_group_data(
            pokedex=pokedex, version_group=version_group
        )

        response = self.client.get(
            "{}/version-group/{}/".format(API_V2, version_group.pk)
        )

        # base params
        self.assertEqual(response.data["id"], version_group.pk)
        self.assertEqual(response.data["name"], version_group.name)
        self.assertEqual(response.data["order"], version_group.order)
        # version params
        self.assertEqual(response.data["versions"][0]["name"], version.name)
        self.assertEqual(
            response.data["versions"][0]["url"],
            "{}{}/version/{}/".format(TEST_HOST, API_V2, version.pk),
        )
        # generation params
        self.assertEqual(
            response.data["generation"]["name"], version_group.generation.name
        )
        self.assertEqual(
            response.data["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, version_group.generation.pk
            ),
        )
        # region params
        self.assertEqual(response.data["regions"][0]["name"], region.name)
        self.assertEqual(
            response.data["regions"][0]["url"],
            "{}{}/region/{}/".format(TEST_HOST, API_V2, region.pk),
        )
        # move learn method params
        self.assertEqual(
            response.data["move_learn_methods"][0]["name"], move_learn_method.name
        )
        self.assertEqual(
            response.data["move_learn_methods"][0]["url"],
            "{}{}/move-learn-method/{}/".format(
                TEST_HOST, API_V2, move_learn_method.pk
            ),
        )
        # pokedex group
        self.assertEqual(response.data["pokedexes"][0]["name"], pokedex.name)
        self.assertEqual(
            response.data["pokedexes"][0]["url"],
            "{}{}/pokedex/{}/".format(TEST_HOST, API_V2, pokedex.pk),
        )

    # Egg Group Tests
    def test_egg_group_api(self):
        egg_group = self.setup_egg_group_data(name="base egg grp")
        egg_group_name = self.setup_egg_group_name_data(
            egg_group, name="base egg grp name"
        )
        pokemon_species = self.setup_pokemon_species_data()
        self.setup_pokemon_egg_group_data(
            pokemon_species=pokemon_species, egg_group=egg_group
        )

        response = self.client.get("{}/egg-group/{}/".format(API_V2, egg_group.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], egg_group.pk)
        self.assertEqual(response.data["name"], egg_group.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], egg_group_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], egg_group_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, egg_group_name.language.pk),
        )
        # species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    # Ability Tests
    def test_ability_api(self):
        ability = self.setup_ability_data(name="base ablty")
        ability_name = self.setup_ability_name_data(ability, name="base ablty name")
        ability_effect_text = self.setup_ability_effect_text_data(
            ability, effect="base ablty efct"
        )
        ability_flavor_text = self.setup_ability_flavor_text_data(
            ability, flavor_text="base flvr txt"
        )
        ability_change = self.setup_ability_change_data(ability)
        ability_change_effect_text = self.setup_ability_change_effect_text_data(
            ability_change, effect="base ablty chng efct"
        )
        pokemon = self.setup_pokemon_data(name="pkmn for ablty")
        pokemon_ability = self.setup_pokemon_ability_data(
            ability=ability, pokemon=pokemon
        )

        response = self.client.get("{}/ability/{}/".format(API_V2, ability.pk))

        # base params
        self.assertEqual(response.data["id"], ability.pk)
        self.assertEqual(response.data["name"], ability.name)
        self.assertEqual(response.data["is_main_series"], ability.is_main_series)
        # name params
        self.assertEqual(response.data["names"][0]["name"], ability_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], ability_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, ability_name.language.pk),
        )
        # description params
        self.assertEqual(
            response.data["effect_entries"][0]["effect"], ability_effect_text.effect
        )
        self.assertEqual(
            response.data["effect_entries"][0]["short_effect"],
            ability_effect_text.short_effect,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["name"],
            ability_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, ability_effect_text.language.pk
            ),
        )
        # flavor text params
        self.assertEqual(
            response.data["flavor_text_entries"][0]["flavor_text"],
            ability_flavor_text.flavor_text,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version_group"]["name"],
            ability_flavor_text.version_group.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["name"],
            ability_flavor_text.language.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, ability_flavor_text.language.pk
            ),
        )
        # generation params
        self.assertEqual(response.data["generation"]["name"], ability.generation.name)
        self.assertEqual(
            response.data["generation"]["url"],
            "{}{}/generation/{}/".format(TEST_HOST, API_V2, ability.generation.pk),
        )
        # change params
        self.assertEqual(
            response.data["effect_changes"][0]["version_group"]["name"],
            ability_change.version_group.name,
        )
        self.assertEqual(
            response.data["effect_changes"][0]["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, ability_change.version_group.pk
            ),
        )
        self.assertEqual(
            response.data["effect_changes"][0]["effect_entries"][0]["effect"],
            ability_change_effect_text.effect,
        )
        self.assertEqual(
            response.data["effect_changes"][0]["effect_entries"][0]["language"]["name"],
            ability_change_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_changes"][0]["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, ability_change_effect_text.language.pk
            ),
        )
        # pokemon params
        self.assertEqual(
            response.data["pokemon"][0]["is_hidden"], pokemon_ability.is_hidden
        )
        self.assertEqual(response.data["pokemon"][0]["slot"], pokemon_ability.slot)
        self.assertEqual(response.data["pokemon"][0]["pokemon"]["name"], pokemon.name)
        self.assertEqual(
            response.data["pokemon"][0]["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon.pk),
        )

    # Item Tests
    def test_item_attribute_api(self):
        # item attribute data
        item_attribute = self.setup_item_attribute_data(name="base itm attr")
        item_attribute_name = self.setup_item_attribute_name_data(
            item_attribute, name="base itm attr nm"
        )
        item_attribute_description = self.setup_item_attribute_description_data(
            item_attribute, description="base itm attr desc"
        )
        item = self.setup_item_data(name="itm fr base itm attr")
        self.setup_item_attribute_map_data(item_attribute=item_attribute, item=item)

        response = self.client.get(
            "{}/item-attribute/{}/".format(API_V2, item_attribute.pk)
        )

        # base params
        self.assertEqual(response.data["id"], item_attribute.pk)
        self.assertEqual(response.data["name"], item_attribute.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], item_attribute_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            item_attribute_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, item_attribute_name.language.pk
            ),
        )
        # description params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            item_attribute_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            item_attribute_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, item_attribute_description.language.pk
            ),
        )
        # item params
        self.assertEqual(response.data["items"][0]["name"], item.name)
        self.assertEqual(
            response.data["items"][0]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, item.pk),
        )

    def test_item_category_api(self):
        # item category data
        item_category = self.setup_item_category_data(name="base itm ctgry")
        item_category_name = self.setup_item_category_name_data(
            item_category, name="base itm ctgry nm"
        )
        item = self.setup_item_data(
            item_category=item_category, name="itm fr base itm ctgry"
        )

        response = self.client.get(
            "{}/item-category/{}/".format(API_V2, item_category.pk)
        )

        # base params
        self.assertEqual(response.data["id"], item_category.pk)
        self.assertEqual(response.data["name"], item_category.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], item_category_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            item_category_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, item_category_name.language.pk
            ),
        )
        # pocket params
        self.assertEqual(
            response.data["pocket"]["name"], item_category.item_pocket.name
        )
        self.assertEqual(
            response.data["pocket"]["url"],
            "{}{}/item-pocket/{}/".format(
                TEST_HOST, API_V2, item_category.item_pocket.pk
            ),
        )
        # item params
        self.assertEqual(response.data["items"][0]["name"], item.name)
        self.assertEqual(
            response.data["items"][0]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, item.pk),
        )

    def test_item_fling_effect_api(self):
        # item category data
        item_fling_effect = self.setup_item_fling_effect_data(name="base itm flng efct")
        item_fling_effect_effect_text = self.setup_item_fling_effect_effect_text_data(
            item_fling_effect, effect="base itm flng efct nm"
        )
        item = self.setup_item_data(
            item_fling_effect=item_fling_effect, name="itm fr base itm attr"
        )

        response = self.client.get(
            "{}/item-fling-effect/{}/".format(API_V2, item_fling_effect.pk)
        )

        # base params
        self.assertEqual(response.data["id"], item_fling_effect.pk)
        self.assertEqual(response.data["name"], item_fling_effect.name)
        # description params
        self.assertEqual(
            response.data["effect_entries"][0]["effect"],
            item_fling_effect_effect_text.effect,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["name"],
            item_fling_effect_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, item_fling_effect_effect_text.language.pk
            ),
        )
        # item params
        self.assertEqual(response.data["items"][0]["name"], item.name)
        self.assertEqual(
            response.data["items"][0]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, item.pk),
        )

    def test_item_pocket_api(self):
        # item pocket data
        item_pocket = self.setup_item_pocket_data(name="base itm pkt")
        item_pocket_name = self.setup_item_pocket_name_data(
            item_pocket, name="base itm pkt nm"
        )

        response = self.client.get("{}/item-pocket/{}/".format(API_V2, item_pocket.pk))

        # base params
        self.assertEqual(response.data["id"], item_pocket.pk)
        self.assertEqual(response.data["name"], item_pocket.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], item_pocket_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            item_pocket_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, item_pocket_name.language.pk),
        )

    def test_item_api(self):
        item_category = self.setup_item_category_data(name="itm ctgry for base itm")
        item_fling_effect = self.setup_item_fling_effect_data(
            name="itm flng efct for base itm"
        )
        item = self.setup_item_data(item_category, item_fling_effect, name="base itm")
        item_name = self.setup_item_name_data(item, name="base itm name")
        item_flavor_text = self.setup_item_flavor_text_data(
            item, flavor_text="base itm flvr txt"
        )
        item_effect_text = self.setup_item_effect_text_data(
            item, effect="base nrml efct", short_effect="base shrt efct"
        )
        item_attribute = self.setup_item_attribute_data()
        item_game_index = self.setup_item_game_index_data(item, game_index=10)
        item_sprites = self.setup_item_sprites_data(item)
        pokemon = self.setup_pokemon_data(name="pkmn for base itm")
        pokemon_item = self.setup_pokemon_item_data(pokemon=pokemon, item=item)
        evolution_chain = self.setup_evolution_chain_data(baby_trigger_item=item)

        # map item attribute to item
        item_attribute_map = ItemAttributeMap(item=item, item_attribute=item_attribute)
        item_attribute_map.save()

        response = self.client.get(
            "{}/item/{}/".format(API_V2, item.pk), HTTP_HOST="testserver"
        )

        # base params
        self.assertEqual(response.data["id"], item.pk)
        self.assertEqual(response.data["name"], item.name)
        self.assertEqual(response.data["cost"], item.cost)
        self.assertEqual(response.data["fling_power"], item.fling_power)
        # name params
        self.assertEqual(response.data["names"][0]["name"], item_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], item_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, item_name.language.pk),
        )
        # flavor text params
        self.assertEqual(
            response.data["flavor_text_entries"][0]["text"],
            item_flavor_text.flavor_text,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version_group"]["name"],
            item_flavor_text.version_group.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, item_flavor_text.version_group.pk
            ),
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["name"],
            item_flavor_text.language.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, item_flavor_text.language.pk),
        )
        # effect text params
        self.assertEqual(
            response.data["effect_entries"][0]["effect"], item_effect_text.effect
        )
        self.assertEqual(
            response.data["effect_entries"][0]["short_effect"],
            item_effect_text.short_effect,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["name"],
            item_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, item_effect_text.language.pk),
        )
        # category params
        self.assertEqual(response.data["category"]["name"], item_category.name)
        self.assertEqual(
            response.data["category"]["url"],
            "{}{}/item-category/{}/".format(TEST_HOST, API_V2, item_category.pk),
        )
        # fling effect params
        self.assertEqual(response.data["fling_effect"]["name"], item_fling_effect.name)
        self.assertEqual(
            response.data["fling_effect"]["url"],
            "{}{}/item-fling-effect/{}/".format(
                TEST_HOST, API_V2, item_fling_effect.pk
            ),
        )
        # attribute params
        self.assertEqual(response.data["attributes"][0]["name"], item_attribute.name)
        self.assertEqual(
            response.data["attributes"][0]["url"],
            "{}{}/item-attribute/{}/".format(TEST_HOST, API_V2, item_attribute.pk),
        )
        # game indices params
        self.assertEqual(
            response.data["game_indices"][0]["game_index"], item_game_index.game_index
        )
        self.assertEqual(
            response.data["game_indices"][0]["generation"]["name"],
            item_game_index.generation.name,
        )
        self.assertEqual(
            response.data["game_indices"][0]["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, item_game_index.generation.pk
            ),
        )
        # held by params
        self.assertEqual(
            response.data["held_by_pokemon"][0]["pokemon"]["name"], pokemon.name
        )
        self.assertEqual(
            response.data["held_by_pokemon"][0]["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon.pk),
        )
        self.assertEqual(
            response.data["held_by_pokemon"][0]["version_details"][0]["rarity"],
            pokemon_item.rarity,
        )
        self.assertEqual(
            response.data["held_by_pokemon"][0]["version_details"][0]["version"][
                "name"
            ],
            pokemon_item.version.name,
        )
        self.assertEqual(
            response.data["held_by_pokemon"][0]["version_details"][0]["version"]["url"],
            "{}{}/version/{}/".format(TEST_HOST, API_V2, pokemon_item.version.pk),
        )
        # baby trigger params
        self.assertEqual(
            response.data["baby_trigger_for"]["url"],
            "{}{}/evolution-chain/{}/".format(TEST_HOST, API_V2, evolution_chain.pk),
        )

        sprites_data = json.loads(response.data["sprites"])

        # sprites
        self.assertEqual(
            sprites_data["default"],
            "{}".format(sprites_data["default"]),
        )

    # Berry Tests
    def test_berry_firmness_api(self):
        berry_firmness = self.setup_berry_firmness_data(name="base bry frmns")
        berry_firmness_name = self.setup_berry_firmness_name_data(
            berry_firmness, name="base bry frmns nm"
        )
        berry = self.setup_berry_data(
            berry_firmness=berry_firmness, name="bry for base frmns"
        )

        response = self.client.get(
            "{}/berry-firmness/{}/".format(API_V2, berry_firmness.pk)
        )

        # base params
        self.assertEqual(response.data["id"], berry_firmness.pk)
        self.assertEqual(response.data["name"], berry_firmness.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], berry_firmness_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            berry_firmness_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, berry_firmness_name.language.pk
            ),
        )
        # berry params
        self.assertEqual(response.data["berries"][0]["name"], berry.name)
        self.assertEqual(
            response.data["berries"][0]["url"],
            "{}{}/berry/{}/".format(TEST_HOST, API_V2, berry.pk),
        )

    def test_berry_flavor_api(self):
        berry_flavor = self.setup_berry_flavor_data(name="base bry flvr")
        berry_flavor_name = self.setup_berry_flavor_name_data(
            berry_flavor, name="base bry flvr nm"
        )
        berry = self.setup_berry_data(name="bry for base bry flvr")
        berry_flavor_map = self.setup_berry_flavor_map_data(
            berry=berry, berry_flavor=berry_flavor, potency=50
        )

        response = self.client.get(
            "{}/berry-flavor/{}/".format(API_V2, berry_flavor.pk)
        )

        # base params
        self.assertEqual(response.data["id"], berry_flavor.pk)
        self.assertEqual(response.data["name"], berry_flavor.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], berry_flavor_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            berry_flavor_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, berry_flavor_name.language.pk
            ),
        )
        # contest type params
        self.assertEqual(
            response.data["contest_type"]["name"], berry_flavor.contest_type.name
        )
        self.assertEqual(
            response.data["contest_type"]["url"],
            "{}{}/contest-type/{}/".format(
                TEST_HOST, API_V2, berry_flavor.contest_type.pk
            ),
        )
        # berry params
        self.assertEqual(
            response.data["berries"][0]["potency"], berry_flavor_map.potency
        )
        self.assertEqual(response.data["berries"][0]["berry"]["name"], berry.name)
        self.assertEqual(
            response.data["berries"][0]["berry"]["url"],
            "{}{}/berry/{}/".format(TEST_HOST, API_V2, berry.pk),
        )

    def test_berry_api(self):
        type = self.setup_type_data(name="tp fr base bry")
        berry = self.setup_berry_data(name="base bry", natural_gift_type=type)
        berry_flavor = self.setup_berry_flavor_data(name="bry flvr for base bry")
        berry_flavor_map = self.setup_berry_flavor_map_data(
            berry=berry, berry_flavor=berry_flavor
        )

        response = self.client.get("{}/berry/{}/".format(API_V2, berry.pk))

        # base params
        self.assertEqual(response.data["id"], berry.pk)
        self.assertEqual(response.data["name"], berry.name)
        self.assertEqual(response.data["growth_time"], berry.growth_time)
        self.assertEqual(response.data["max_harvest"], berry.max_harvest)
        self.assertEqual(response.data["natural_gift_power"], berry.natural_gift_power)
        self.assertEqual(response.data["size"], berry.size)
        self.assertEqual(response.data["smoothness"], berry.smoothness)
        self.assertEqual(response.data["soil_dryness"], berry.soil_dryness)
        # firmness params
        self.assertEqual(response.data["firmness"]["name"], berry.berry_firmness.name)
        self.assertEqual(
            response.data["firmness"]["url"],
            "{}{}/berry-firmness/{}/".format(
                TEST_HOST, API_V2, berry.berry_firmness.pk
            ),
        )
        # item params
        self.assertEqual(response.data["item"]["name"], berry.item.name)
        self.assertEqual(
            response.data["item"]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, berry.item.pk),
        )
        # flavor params
        self.assertEqual(
            response.data["flavors"][0]["potency"], berry_flavor_map.potency
        )
        self.assertEqual(
            response.data["flavors"][0]["flavor"]["name"], berry_flavor.name
        )
        self.assertEqual(
            response.data["flavors"][0]["flavor"]["url"],
            "{}{}/berry-flavor/{}/".format(TEST_HOST, API_V2, berry_flavor.pk),
        )
        # natural gift type
        self.assertEqual(response.data["natural_gift_type"]["name"], type.name)
        self.assertEqual(
            response.data["natural_gift_type"]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, type.pk),
        )

    # Growth Rate Tests
    def test_growth_rate_api(self):
        # item pocket data
        growth_rate = self.setup_growth_rate_data(name="base grth rt")
        growth_rate_description = self.setup_growth_rate_description_data(
            growth_rate, description="base grth rt desc"
        )
        pokemon_species = self.setup_pokemon_species_data(
            name="pkmn spcs for grth rt", growth_rate=growth_rate
        )

        # map item attribute to item
        experience = Experience(growth_rate=growth_rate, level=10, experience=3000)
        experience.save()

        response = self.client.get("{}/growth-rate/{}/".format(API_V2, growth_rate.pk))

        # base params
        self.assertEqual(response.data["id"], growth_rate.pk)
        self.assertEqual(response.data["name"], growth_rate.name)
        self.assertEqual(response.data["formula"], growth_rate.formula)
        # description params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            growth_rate_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            growth_rate_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, growth_rate_description.language.pk
            ),
        )
        # experience params
        self.assertEqual(response.data["levels"][0]["level"], experience.level)
        self.assertEqual(
            response.data["levels"][0]["experience"], experience.experience
        )
        # species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    # Location Tests
    def test_location_api(self):
        location = self.setup_location_data(name="base lctn")
        location_name = self.setup_location_name_data(location, name="base lctn name")
        location_game_index = self.setup_location_game_index_data(
            location, game_index=10
        )

        response = self.client.get("{}/location/{}/".format(API_V2, location.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], location.pk)
        self.assertEqual(response.data["name"], location.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], location_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], location_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, location_name.language.pk),
        )
        # region params
        self.assertEqual(response.data["region"]["name"], location.region.name)
        self.assertEqual(
            response.data["region"]["url"],
            "{}{}/region/{}/".format(TEST_HOST, API_V2, location.region.pk),
        )
        # game indices params
        self.assertEqual(
            response.data["game_indices"][0]["game_index"],
            location_game_index.game_index,
        )
        self.assertEqual(
            response.data["game_indices"][0]["generation"]["name"],
            location_game_index.generation.name,
        )
        self.assertEqual(
            response.data["game_indices"][0]["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, location_game_index.generation.pk
            ),
        )

    def test_location_area_api(self):
        location = self.setup_location_data(name="lctn for base lctn area")
        location_area = self.setup_location_area_data(location, name="base lctn area")
        location_area_name = self.setup_location_area_name_data(
            location_area, name="base lctn area name"
        )

        encounter_method = self.setup_encounter_method_data(
            name="encntr mthd for lctn area"
        )
        location_area_encounter_rate = self.setup_location_area_encounter_rate_data(
            location_area, encounter_method, rate=20
        )

        pokemon_species1 = self.setup_pokemon_species_data(name="spcs for pkmn1")
        pokemon1 = self.setup_pokemon_data(
            name="pkmn1 for base encntr", pokemon_species=pokemon_species1
        )
        encounter_slot1 = self.setup_encounter_slot_data(
            encounter_method, slot=1, rarity=30
        )
        encounter1 = self.setup_encounter_data(
            pokemon=pokemon1,
            location_area=location_area,
            encounter_slot=encounter_slot1,
            min_level=30,
            max_level=35,
        )

        pokemon_species2 = self.setup_pokemon_species_data(name="spcs for pkmn2")
        pokemon2 = self.setup_pokemon_data(
            name="pkmn2 for base encntr", pokemon_species=pokemon_species2
        )
        encounter_slot2 = self.setup_encounter_slot_data(
            encounter_method, slot=2, rarity=40
        )
        encounter2 = self.setup_encounter_data(
            pokemon=pokemon2,
            location_area=location_area,
            encounter_slot=encounter_slot2,
            min_level=32,
            max_level=36,
        )

        response = self.client.get(
            "{}/location-area/{}/".format(API_V2, location_area.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], location_area.pk)
        self.assertEqual(response.data["name"], location_area.name)
        self.assertEqual(response.data["game_index"], location_area.game_index)
        # name params
        self.assertEqual(response.data["names"][0]["name"], location_area_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            location_area_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, location_area_name.language.pk
            ),
        )
        # location params
        self.assertEqual(response.data["location"]["name"], location.name)
        self.assertEqual(
            response.data["location"]["url"],
            "{}{}/location/{}/".format(TEST_HOST, API_V2, location.pk),
        )
        # encounter method params
        self.assertEqual(
            response.data["encounter_method_rates"][0]["encounter_method"]["name"],
            encounter_method.name,
        )
        self.assertEqual(
            response.data["encounter_method_rates"][0]["encounter_method"]["url"],
            "{}{}/encounter-method/{}/".format(TEST_HOST, API_V2, encounter_method.pk),
        )
        self.assertEqual(
            response.data["encounter_method_rates"][0]["version_details"][0]["rate"],
            location_area_encounter_rate.rate,
        )
        self.assertEqual(
            response.data["encounter_method_rates"][0]["version_details"][0]["version"][
                "name"
            ],
            location_area_encounter_rate.version.name,
        )
        self.assertEqual(
            response.data["encounter_method_rates"][0]["version_details"][0]["version"][
                "url"
            ],
            "{}{}/version/{}/".format(
                TEST_HOST, API_V2, location_area_encounter_rate.version.pk
            ),
        )
        # encounter params
        self.assertEqual(
            response.data["pokemon_encounters"][0]["pokemon"]["name"], pokemon1.name
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0]["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon1.pk),
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0]["version_details"][0]["max_chance"],
            encounter_slot1.rarity,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0]["version_details"][0]["version"][
                "name"
            ],
            encounter1.version.name,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0]["version_details"][0]["version"][
                "url"
            ],
            "{}{}/version/{}/".format(TEST_HOST, API_V2, encounter1.version.pk),
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0].get("version_details")[0][
                "encounter_details"
            ][0]["chance"],
            encounter_slot1.rarity,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0].get("version_details")[0][
                "encounter_details"
            ][0]["method"]["name"],
            encounter_slot1.encounter_method.name,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0]["version_details"][0].get(
                "encounter_details"
            )[0]["method"]["url"],
            "{}{}/encounter-method/{}/".format(
                TEST_HOST, API_V2, encounter_slot1.encounter_method.pk
            ),
        )

        self.assertEqual(
            response.data["pokemon_encounters"][1]["pokemon"]["name"], pokemon2.name
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1]["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon2.pk),
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1]["version_details"][0]["max_chance"],
            encounter_slot2.rarity,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1]["version_details"][0]["version"][
                "name"
            ],
            encounter2.version.name,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1]["version_details"][0]["version"][
                "url"
            ],
            "{}{}/version/{}/".format(TEST_HOST, API_V2, encounter2.version.pk),
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1].get("version_details")[0][
                "encounter_details"
            ][0]["chance"],
            encounter_slot2.rarity,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1]["version_details"][0].get(
                "encounter_details"
            )[0]["method"]["name"],
            encounter_slot2.encounter_method.name,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][1]["version_details"][0].get(
                "encounter_details"
            )[0]["method"]["url"],
            "{}{}/encounter-method/{}/".format(
                TEST_HOST, API_V2, encounter_slot2.encounter_method.pk
            ),
        )

    # Contest Tests
    def test_contest_type_api(self):
        contest_type = self.setup_contest_type_data(name="base cntst tp")
        contest_type_name = self.setup_contest_type_name_data(
            contest_type, name="base cntst tp name"
        )
        berry_flavor = self.setup_berry_flavor_data(
            name="bry for base cntst tp", contest_type=contest_type
        )

        response = self.client.get(
            "{}/contest-type/{}/".format(API_V2, contest_type.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], contest_type.pk)
        self.assertEqual(response.data["name"], contest_type.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], contest_type_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            contest_type_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, contest_type_name.language.pk
            ),
        )
        # berry params
        self.assertEqual(response.data["berry_flavor"]["name"], berry_flavor.name)
        self.assertEqual(
            response.data["berry_flavor"]["url"],
            "{}{}/berry-flavor/{}/".format(TEST_HOST, API_V2, berry_flavor.pk),
        )

    def test_contest_effect_api(self):
        contest_effect = self.setup_contest_effect_data(appeal=10, jam=20)
        contest_effect_flavor_text = self.setup_contest_effect_flavor_text_data(
            contest_effect, flavor_text="base cntst efct flvr txt"
        )
        contest_effect_effect_text = self.setup_contest_effect_effect_text_data(
            contest_effect, effect="base cntst efct eftc txt"
        )

        response = self.client.get(
            "{}/contest-effect/{}/".format(API_V2, contest_effect.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], contest_effect.pk)
        self.assertEqual(response.data["appeal"], contest_effect.appeal)
        self.assertEqual(response.data["jam"], contest_effect.jam)
        # effect text params
        self.assertEqual(
            response.data["effect_entries"][0]["effect"],
            contest_effect_effect_text.effect,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["name"],
            contest_effect_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, contest_effect_effect_text.language.pk
            ),
        )
        # flavor text params
        self.assertEqual(
            response.data["flavor_text_entries"][0]["flavor_text"],
            contest_effect_flavor_text.flavor_text,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["name"],
            contest_effect_flavor_text.language.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, contest_effect_flavor_text.language.pk
            ),
        )

    def test_super_contest_effect_api(self):
        super_contest_effect = self.setup_super_contest_effect_data(appeal=10)
        super_contest_effect_flavor_text = (
            self.setup_super_contest_effect_flavor_text_data(
                super_contest_effect, flavor_text="base spr cntst efct flvr txt"
            )
        )
        move = self.setup_move_data(
            name="mv for base spr cntst efct", super_contest_effect=super_contest_effect
        )

        response = self.client.get(
            "{}/super-contest-effect/{}/".format(API_V2, super_contest_effect.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], super_contest_effect.pk)
        self.assertEqual(response.data["appeal"], super_contest_effect.appeal)
        # flavor text params
        self.assertEqual(
            response.data["flavor_text_entries"][0]["flavor_text"],
            super_contest_effect_flavor_text.flavor_text,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["name"],
            super_contest_effect_flavor_text.language.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, super_contest_effect_flavor_text.language.pk
            ),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )

    # Type Tests
    def test_type_api(self):
        type = self.setup_type_data(name="base tp")
        type_name = self.setup_type_name_data(type, name="base tp nm")
        type_game_index = self.setup_type_game_index_data(type, game_index=10)
        move = self.setup_move_data(name="mv for base tp", type=type)
        pokemon = self.setup_pokemon_data(name="pkmn for base tp")
        pokemon_type = self.setup_pokemon_type_data(pokemon=pokemon, type=type)

        generation = self.setup_generation_data(name="past gen")

        no_damage_to = self.setup_type_data(
            name="no damage to tp", generation=generation
        )
        half_damage_to = self.setup_type_data(
            name="half damage to tp", generation=generation
        )
        double_damage_to = self.setup_type_data(
            name="double damage to tp", generation=generation
        )
        no_damage_from = self.setup_type_data(
            name="no damage from tp", generation=generation
        )
        half_damage_from = self.setup_type_data(
            name="half damage from tp", generation=generation
        )
        double_damage_from = self.setup_type_data(
            name="double damage from tp", generation=generation
        )

        newer_generation = self.setup_generation_data(name="newer_generation")

        newer_type = self.setup_type_data(name="newer tp", generation=newer_generation)

        # type relations
        no_damage_to_relation = TypeEfficacy(
            damage_type=type, target_type=no_damage_to, damage_factor=0
        )
        no_damage_to_relation.save()

        half_damage_to_type_relation = TypeEfficacy(
            damage_type=type, target_type=half_damage_to, damage_factor=50
        )
        half_damage_to_type_relation.save()

        double_damage_to_type_relation = TypeEfficacy(
            damage_type=type, target_type=double_damage_to, damage_factor=200
        )
        double_damage_to_type_relation.save()

        no_damage_from_relation = TypeEfficacy(
            damage_type=no_damage_from, target_type=type, damage_factor=0
        )
        no_damage_from_relation.save()

        half_damage_from_type_relation = TypeEfficacy(
            damage_type=half_damage_from, target_type=type, damage_factor=50
        )
        half_damage_from_type_relation.save()

        double_damage_from_type_relation = TypeEfficacy(
            damage_type=double_damage_from, target_type=type, damage_factor=200
        )
        double_damage_from_type_relation.save()

        double_damage_from_newer_type_relation = TypeEfficacy(
            damage_type=newer_type, target_type=type, damage_factor=200
        )
        double_damage_from_newer_type_relation.save()

        # past type relations

        # type used to deal half damage rather than no damage
        past_no_damage_to_relation = TypeEfficacyPast(
            damage_type=type,
            target_type=no_damage_to,
            damage_factor=50,
            generation=generation,
        )
        past_no_damage_to_relation.save()

        response = self.client.get("{}/type/{}/".format(API_V2, type.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], type.pk)
        self.assertEqual(response.data["name"], type.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], type_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], type_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, type_name.language.pk),
        )
        # generation params
        self.assertEqual(response.data["generation"]["name"], type.generation.name)
        self.assertEqual(
            response.data["generation"]["url"],
            "{}{}/generation/{}/".format(TEST_HOST, API_V2, type.generation.pk),
        )
        # damage class params
        self.assertEqual(
            response.data["move_damage_class"]["name"], type.move_damage_class.name
        )
        self.assertEqual(
            response.data["move_damage_class"]["url"],
            "{}{}/move-damage-class/{}/".format(
                TEST_HOST, API_V2, type.move_damage_class.pk
            ),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )
        # pokemon params
        self.assertEqual(response.data["pokemon"][0]["slot"], pokemon_type.slot)
        self.assertEqual(response.data["pokemon"][0]["pokemon"]["name"], pokemon.name)
        self.assertEqual(
            response.data["pokemon"][0]["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon.pk),
        )
        # damage relations params
        self.assertEqual(
            response.data["damage_relations"]["no_damage_to"][0]["name"],
            no_damage_to.name,
        )
        self.assertEqual(
            response.data["damage_relations"]["no_damage_to"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, no_damage_to.pk),
        )
        self.assertEqual(
            response.data["damage_relations"]["half_damage_to"][0]["name"],
            half_damage_to.name,
        )
        self.assertEqual(
            response.data["damage_relations"]["half_damage_to"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, half_damage_to.pk),
        )
        self.assertEqual(
            response.data["damage_relations"]["double_damage_to"][0]["name"],
            double_damage_to.name,
        )
        self.assertEqual(
            response.data["damage_relations"]["double_damage_to"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, double_damage_to.pk),
        )
        self.assertEqual(
            response.data["damage_relations"]["no_damage_from"][0]["name"],
            no_damage_from.name,
        )
        self.assertEqual(
            response.data["damage_relations"]["no_damage_from"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, no_damage_from.pk),
        )
        self.assertEqual(
            response.data["damage_relations"]["half_damage_from"][0]["name"],
            half_damage_from.name,
        )
        self.assertEqual(
            response.data["damage_relations"]["half_damage_from"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, half_damage_from.pk),
        )
        self.assertEqual(
            response.data["damage_relations"]["double_damage_from"][0]["name"],
            double_damage_from.name,
        )
        self.assertEqual(
            response.data["damage_relations"]["double_damage_from"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, double_damage_from.pk),
        )

        # past damage relations params

        # generation
        past_damage_relations = response.data["past_damage_relations"]
        gen_data = past_damage_relations[0]["generation"]
        self.assertEqual(gen_data["name"], generation.name)
        self.assertEqual(
            gen_data["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, past_no_damage_to_relation.generation.pk
            ),
        )

        # relations
        gen_relations = past_damage_relations[0]["damage_relations"]

        # type that currently receives no damage used to receive half damage, so is no longer in
        # this list...
        self.assertEqual(len(gen_relations["no_damage_to"]), 0)

        self.assertEqual(
            gen_relations["half_damage_to"][0]["name"], half_damage_to.name
        )
        self.assertEqual(
            gen_relations["half_damage_to"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, half_damage_to.pk),
        )

        # ...it's in this list instead
        self.assertEqual(gen_relations["half_damage_to"][1]["name"], no_damage_to.name)
        self.assertEqual(
            gen_relations["half_damage_to"][1]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, no_damage_to.pk),
        )

        self.assertEqual(
            gen_relations["double_damage_to"][0]["name"], double_damage_to.name
        )
        self.assertEqual(
            gen_relations["double_damage_to"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, double_damage_to.pk),
        )
        self.assertEqual(
            gen_relations["no_damage_from"][0]["name"], no_damage_from.name
        )
        self.assertEqual(
            gen_relations["no_damage_from"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, no_damage_from.pk),
        )
        self.assertEqual(
            gen_relations["half_damage_from"][0]["name"], half_damage_from.name
        )
        self.assertEqual(
            gen_relations["half_damage_from"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, half_damage_from.pk),
        )
        self.assertEqual(
            gen_relations["double_damage_from"][0]["name"], double_damage_from.name
        )
        self.assertEqual(
            gen_relations["double_damage_from"][0]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, double_damage_from.pk),
        )

        # second double-damage-from type is absent because it's from a newer generation than the
        # generation of this set of relations
        self.assertEqual(len(gen_relations["double_damage_from"]), 1)

        # game indices params
        self.assertEqual(
            response.data["game_indices"][0]["game_index"], type_game_index.game_index
        )
        self.assertEqual(
            response.data["game_indices"][0]["generation"]["name"],
            type_game_index.generation.name,
        )
        self.assertEqual(
            response.data["game_indices"][0]["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, type_game_index.generation.pk
            ),
        )

    # Pokedex Tests
    def test_pokedex_api(self):
        pokedex = self.setup_pokedex_data(name="base pkdx")
        pokedex_name = self.setup_pokedex_name_data(pokedex, name="base pkdx name")
        pokedex_description = self.setup_pokedex_description_data(
            pokedex, description="base pkdx desc"
        )
        pokemon_species = self.setup_pokemon_species_data(
            name="pkmn spcs for base pkdx"
        )
        dex_entry = self.setup_pokemon_dex_entry_data(
            pokedex=pokedex, pokemon_species=pokemon_species
        )

        response = self.client.get("{}/pokedex/{}/".format(API_V2, pokedex.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokedex.pk)
        self.assertEqual(response.data["name"], pokedex.name)
        self.assertEqual(response.data["is_main_series"], pokedex.is_main_series)
        # name params
        self.assertEqual(response.data["names"][0]["name"], pokedex_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], pokedex_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, pokedex_name.language.pk),
        )
        # descriptions params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            pokedex_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            pokedex_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokedex_description.language.pk
            ),
        )
        # region params
        self.assertEqual(response.data["region"]["name"], pokedex.region.name)
        self.assertEqual(
            response.data["region"]["url"],
            "{}{}/region/{}/".format(TEST_HOST, API_V2, pokedex.region.pk),
        )
        # species params
        self.assertEqual(
            response.data["pokemon_entries"][0]["entry_number"],
            dex_entry.pokedex_number,
        )
        self.assertEqual(
            response.data["pokemon_entries"][0]["pokemon_species"]["name"],
            pokemon_species.name,
        )
        self.assertEqual(
            response.data["pokemon_entries"][0]["pokemon_species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    # Move Tests
    def test_move_ailment_api(self):
        move_ailment = self.setup_move_ailment_data(name="base mv almnt")
        move_ailment_name = self.setup_move_ailment_name_data(
            move_ailment, name="base mv almnt name"
        )
        move = self.setup_move_data(name="mv for base mv almnt")
        self.setup_move_meta_data(move=move, move_ailment=move_ailment)

        response = self.client.get(
            "{}/move-ailment/{}/".format(API_V2, move_ailment.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move_ailment.pk)
        self.assertEqual(response.data["name"], move_ailment.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], move_ailment_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            move_ailment_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_ailment_name.language.pk
            ),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )

    def test_move_battle_style_api(self):
        move_battle_style = self.setup_move_battle_style_data(name="base mv btl stl")
        move_battle_style_name = self.setup_move_battle_style_name_data(
            move_battle_style, name="base mv btl stl name"
        )

        response = self.client.get(
            "{}/move-battle-style/{}/".format(API_V2, move_battle_style.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move_battle_style.pk)
        self.assertEqual(response.data["name"], move_battle_style.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], move_battle_style_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            move_battle_style_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_battle_style_name.language.pk
            ),
        )

    def test_move_category_api(self):
        move_category = self.setup_move_category_data(name="base mv ctgry")
        move_category_description = self.setup_move_category_description_data(
            move_category, description="base mv ctgry description"
        )
        move = self.setup_move_data(name="mv for base mv ctgry")
        self.setup_move_meta_data(move=move, move_category=move_category)

        response = self.client.get(
            "{}/move-category/{}/".format(API_V2, move_category.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move_category.pk)
        self.assertEqual(response.data["name"], move_category.name)
        # name params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            move_category_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            move_category_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_category_description.language.pk
            ),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )

    def test_move_damage_class_api(self):
        move_damage_class = self.setup_move_damage_class_data(name="base mv dmg cls")
        move_damage_class_name = self.setup_move_damage_class_name_data(
            move_damage_class, name="base mv dmg cls nm"
        )
        move_damage_class_description = self.setup_move_damage_class_description_data(
            move_damage_class, description="base mv dmg cls desc"
        )
        move = self.setup_move_data(
            name="mv for base mv dmg cls", move_damage_class=move_damage_class
        )

        response = self.client.get(
            "{}/move-damage-class/{}/".format(API_V2, move_damage_class.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move_damage_class.pk)
        self.assertEqual(response.data["name"], move_damage_class.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], move_damage_class_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            move_damage_class_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_damage_class_name.language.pk
            ),
        )
        # description params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            move_damage_class_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            move_damage_class_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_damage_class_description.language.pk
            ),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )

    def test_move_learn_method_api(self):
        move_learn_method = self.setup_move_learn_method_data(name="base mv lrn mthd")
        move_learn_method_name = self.setup_move_learn_method_name_data(
            move_learn_method, name="base mv lrn mthd nm"
        )
        move_learn_method_description = self.setup_move_learn_method_description_data(
            move_learn_method, description="base mv lrn mthd desc"
        )
        version_group = self.setup_version_group_data(
            name="ver grp for base mv lrn mthd"
        )
        self.setup_version_group_move_learn_method_data(
            version_group=version_group, move_learn_method=move_learn_method
        )

        response = self.client.get(
            "{}/move-learn-method/{}/".format(API_V2, move_learn_method.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move_learn_method.pk)
        self.assertEqual(response.data["name"], move_learn_method.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], move_learn_method_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            move_learn_method_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_learn_method_name.language.pk
            ),
        )
        # description params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            move_learn_method_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            move_learn_method_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_learn_method_description.language.pk
            ),
        )
        # version group params
        self.assertEqual(response.data["version_groups"][0]["name"], version_group.name)
        self.assertEqual(
            response.data["version_groups"][0]["url"],
            "{}{}/version-group/{}/".format(TEST_HOST, API_V2, version_group.pk),
        )

    def test_move_target_api(self):
        move_target = self.setup_move_target_data(name="base mv trgt")
        move_target_name = self.setup_move_target_name_data(
            move_target, name="base mv trgt nm"
        )
        move_target_description = self.setup_move_target_description_data(
            move_target, description="base mv trgt desc"
        )
        move = self.setup_move_data(name="mv for base mv trgt", move_target=move_target)

        response = self.client.get("{}/move-target/{}/".format(API_V2, move_target.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move_target.pk)
        self.assertEqual(response.data["name"], move_target.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], move_target_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            move_target_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, move_target_name.language.pk),
        )
        # description params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            move_target_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            move_target_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_target_description.language.pk
            ),
        )
        # move params
        self.assertEqual(response.data["moves"][0]["name"], move.name)
        self.assertEqual(
            response.data["moves"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, move.pk),
        )

    def test_move_api(self):
        move_effect = self.setup_move_effect_data()
        move_effect_effect_text = self.setup_move_effect_effect_text_data(move_effect)
        move = self.setup_move_data(name="base mv", move_effect=move_effect)
        move_name = self.setup_move_name_data(move, name="base mv nm")
        move_meta = self.setup_move_meta_data(move)
        move_stat_change = self.setup_move_stat_change_data(move=move, change=2)
        move_change = self.setup_move_change_data(move, power=10, pp=20, accuracy=30)
        move_effect_change = self.setup_move_effect_change_data(move_effect)
        move_effect_change_effect_text = self.setup_move_effect_change_effect_text_data(
            move_effect_change=move_effect_change, effect="efct tx for mv efct chng"
        )
        pokemon = self.setup_pokemon_data()
        version_group = self.setup_version_group_data()

        self.setup_pokemon_move_data(pokemon, move, version_group)

        after_move = self.setup_move_data(name="after mv")
        before_move = self.setup_move_data(name="before mv")

        self.setup_contest_combo_data(move, after_move)
        self.setup_contest_combo_data(before_move, move)
        self.setup_super_contest_combo_data(move, after_move)
        self.setup_super_contest_combo_data(before_move, move)
        move_flavor_text = self.setup_move_flavor_text_data(
            move, flavor_text="flvr text for move"
        )

        response = self.client.get("{}/move/{}/".format(API_V2, move.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], move.pk)
        self.assertEqual(response.data["name"], move.name)
        self.assertEqual(response.data["accuracy"], move.accuracy)
        self.assertEqual(response.data["effect_chance"], move.move_effect_chance)
        self.assertEqual(response.data["power"], move.power)
        self.assertEqual(response.data["pp"], move.pp)
        self.assertEqual(response.data["priority"], move.priority)
        # name params
        self.assertEqual(response.data["names"][0]["name"], move_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], move_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, move_name.language.pk),
        )
        # damage class params
        self.assertEqual(
            response.data["damage_class"]["name"], move.move_damage_class.name
        )
        self.assertEqual(
            response.data["damage_class"]["url"],
            "{}{}/move-damage-class/{}/".format(
                TEST_HOST, API_V2, move.move_damage_class.pk
            ),
        )
        # contest type params
        self.assertEqual(response.data["contest_type"]["name"], move.contest_type.name)
        self.assertEqual(
            response.data["contest_type"]["url"],
            "{}{}/contest-type/{}/".format(TEST_HOST, API_V2, move.contest_type.pk),
        )
        # contest effect params
        self.assertEqual(
            response.data["contest_effect"]["url"],
            "{}{}/contest-effect/{}/".format(TEST_HOST, API_V2, move.contest_effect.pk),
        )
        # super contest effect params
        self.assertEqual(
            response.data["super_contest_effect"]["url"],
            "{}{}/super-contest-effect/{}/".format(
                TEST_HOST, API_V2, move.super_contest_effect.pk
            ),
        )
        # generation params
        self.assertEqual(response.data["generation"]["name"], move.generation.name)
        self.assertEqual(
            response.data["generation"]["url"],
            "{}{}/generation/{}/".format(TEST_HOST, API_V2, move.generation.pk),
        )
        # target params
        self.assertEqual(response.data["target"]["name"], move.move_target.name)
        self.assertEqual(
            response.data["target"]["url"],
            "{}{}/move-target/{}/".format(TEST_HOST, API_V2, move.move_target.pk),
        )
        # type params
        self.assertEqual(response.data["type"]["name"], move.type.name)
        self.assertEqual(
            response.data["type"]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, move.type.pk),
        )
        # stat change params
        self.assertEqual(
            response.data["stat_changes"][0]["change"], move_stat_change.change
        )
        self.assertEqual(
            response.data["stat_changes"][0]["stat"]["name"], move_stat_change.stat.name
        )
        self.assertEqual(
            response.data["stat_changes"][0]["stat"]["url"],
            "{}{}/stat/{}/".format(TEST_HOST, API_V2, move_stat_change.stat.pk),
        )
        # effect entries params
        self.assertEqual(
            response.data["effect_entries"][0]["effect"], move_effect_effect_text.effect
        )
        self.assertEqual(
            response.data["effect_entries"][0]["short_effect"],
            move_effect_effect_text.short_effect,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["name"],
            move_effect_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_effect_effect_text.language.pk
            ),
        )
        # meta data
        self.assertEqual(response.data["meta"]["min_hits"], move_meta.min_hits)
        self.assertEqual(response.data["meta"]["max_hits"], move_meta.max_hits)
        self.assertEqual(response.data["meta"]["min_turns"], move_meta.min_turns)
        self.assertEqual(response.data["meta"]["max_turns"], move_meta.max_turns)
        self.assertEqual(response.data["meta"]["drain"], move_meta.drain)
        self.assertEqual(response.data["meta"]["healing"], move_meta.healing)
        self.assertEqual(response.data["meta"]["crit_rate"], move_meta.crit_rate)
        self.assertEqual(
            response.data["meta"]["ailment_chance"], move_meta.ailment_chance
        )
        self.assertEqual(
            response.data["meta"]["flinch_chance"], move_meta.flinch_chance
        )
        self.assertEqual(response.data["meta"]["stat_chance"], move_meta.stat_chance)
        # ailment params
        self.assertEqual(
            response.data["meta"]["ailment"]["name"], move_meta.move_meta_ailment.name
        )
        self.assertEqual(
            response.data["meta"]["ailment"]["url"],
            "{}{}/move-ailment/{}/".format(
                TEST_HOST, API_V2, move_meta.move_meta_ailment.pk
            ),
        )
        # category params
        self.assertEqual(
            response.data["meta"]["category"]["name"], move_meta.move_meta_category.name
        )
        self.assertEqual(
            response.data["meta"]["category"]["url"],
            "{}{}/move-category/{}/".format(
                TEST_HOST, API_V2, move_meta.move_meta_category.pk
            ),
        )
        # combo params
        self.assertEqual(
            response.data["contest_combos"]["normal"]["use_before"][0]["name"],
            after_move.name,
        )
        self.assertEqual(
            response.data["contest_combos"]["normal"]["use_before"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, after_move.pk),
        )
        self.assertEqual(
            response.data["contest_combos"]["normal"]["use_after"][0]["name"],
            before_move.name,
        )
        self.assertEqual(
            response.data["contest_combos"]["normal"]["use_after"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, before_move.pk),
        )
        self.assertEqual(
            response.data["contest_combos"]["super"]["use_before"][0]["name"],
            after_move.name,
        )
        self.assertEqual(
            response.data["contest_combos"]["super"]["use_before"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, after_move.pk),
        )
        self.assertEqual(
            response.data["contest_combos"]["super"]["use_after"][0]["name"],
            before_move.name,
        )
        self.assertEqual(
            response.data["contest_combos"]["super"]["use_after"][0]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, before_move.pk),
        )
        # change params
        self.assertEqual(
            response.data["past_values"][0]["accuracy"], move_change.accuracy
        )
        self.assertEqual(response.data["past_values"][0]["power"], move_change.power)
        self.assertEqual(response.data["past_values"][0]["pp"], move_change.pp)
        self.assertEqual(
            response.data["past_values"][0]["effect_chance"],
            move_change.move_effect_chance,
        )
        self.assertEqual(
            response.data["past_values"][0]["version_group"]["name"],
            move_change.version_group.name,
        )
        self.assertEqual(
            response.data["past_values"][0]["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, move_change.version_group.pk
            ),
        )
        # effect changes
        self.assertEqual(
            response.data["effect_changes"][0]["version_group"]["name"],
            move_effect_change.version_group.name,
        )
        self.assertEqual(
            response.data["effect_changes"][0]["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, move_effect_change.version_group.pk
            ),
        )
        self.assertEqual(
            response.data["effect_changes"][0]["effect_entries"][0]["effect"],
            move_effect_change_effect_text.effect,
        )
        self.assertEqual(
            response.data["effect_changes"][0]["effect_entries"][0]["language"]["name"],
            move_effect_change_effect_text.language.name,
        )
        self.assertEqual(
            response.data["effect_changes"][0]["effect_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, move_effect_change_effect_text.language.pk
            ),
        )
        # flavor text params
        self.assertEqual(
            response.data["flavor_text_entries"][0]["flavor_text"],
            move_flavor_text.flavor_text,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["name"],
            move_flavor_text.language.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, move_flavor_text.language.pk),
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version_group"]["name"],
            move_flavor_text.version_group.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, move_flavor_text.version_group.pk
            ),
        )
        # pokemon
        self.assertEqual(response.data["learned_by_pokemon"][0]["name"], pokemon.name)

    # Stat Tests
    def test_stat_api(self):
        stat = self.setup_stat_data(name="base stt")
        stat_name = self.setup_stat_name_data(stat, name="base stt name")
        increase_move = self.setup_move_data(name="incrs mv for base stt")
        increase_move_stat_change = self.setup_move_stat_change_data(
            move=increase_move, stat=stat, change=2
        )
        decrease_move = self.setup_move_data(name="dcrs mv for base stt")
        decrease_move_stat_change = self.setup_move_stat_change_data(
            move=decrease_move, stat=stat, change=(-2)
        )
        increase_nature = self.setup_nature_data(
            name="incrs ntr for base stt", increased_stat=stat
        )
        decrease_nature = self.setup_nature_data(
            name="dcrs ntr for base stt", decreased_stat=stat
        )
        characteristic = self.setup_characteristic_data(stat=stat)

        response = self.client.get("{}/stat/{}/".format(API_V2, stat.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], stat.pk)
        self.assertEqual(response.data["name"], stat.name)
        self.assertEqual(response.data["game_index"], stat.game_index)
        self.assertEqual(response.data["is_battle_only"], stat.is_battle_only)
        # name params
        self.assertEqual(response.data["names"][0]["name"], stat_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], stat_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, stat_name.language.pk),
        )
        # move damage class params
        self.assertEqual(
            response.data["move_damage_class"]["name"], stat.move_damage_class.name
        )
        self.assertEqual(
            response.data["move_damage_class"]["url"],
            "{}{}/move-damage-class/{}/".format(
                TEST_HOST, API_V2, stat.move_damage_class.pk
            ),
        )
        # nature params
        self.assertEqual(
            response.data["affecting_natures"]["increase"][0]["name"],
            increase_nature.name,
        )
        self.assertEqual(
            response.data["affecting_natures"]["increase"][0]["url"],
            "{}{}/nature/{}/".format(TEST_HOST, API_V2, increase_nature.pk),
        )
        self.assertEqual(
            response.data["affecting_natures"]["decrease"][0]["name"],
            decrease_nature.name,
        )
        self.assertEqual(
            response.data["affecting_natures"]["decrease"][0]["url"],
            "{}{}/nature/{}/".format(TEST_HOST, API_V2, decrease_nature.pk),
        )
        # move params
        self.assertEqual(
            response.data["affecting_moves"]["increase"][0]["change"],
            increase_move_stat_change.change,
        )
        self.assertEqual(
            response.data["affecting_moves"]["increase"][0]["move"]["name"],
            increase_move.name,
        )
        self.assertEqual(
            response.data["affecting_moves"]["increase"][0]["move"]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, increase_move.pk),
        )
        self.assertEqual(
            response.data["affecting_moves"]["decrease"][0]["change"],
            decrease_move_stat_change.change,
        )
        self.assertEqual(
            response.data["affecting_moves"]["decrease"][0]["move"]["name"],
            decrease_move.name,
        )
        self.assertEqual(
            response.data["affecting_moves"]["decrease"][0]["move"]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, decrease_move.pk),
        )
        # characteristics params
        self.assertEqual(
            response.data["characteristics"][0]["url"],
            "{}{}/characteristic/{}/".format(TEST_HOST, API_V2, characteristic.pk),
        )

    def test_pokeathlon_stat_api(self):
        pokeathlon_stat = self.setup_pokeathlon_stat_data(name="base pkathln stt")
        pokeathlon_stat_name = self.setup_pokeathlon_stat_name_data(
            pokeathlon_stat, name="base pkathln stt name"
        )

        response = self.client.get(
            "{}/pokeathlon-stat/{}/".format(API_V2, pokeathlon_stat.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokeathlon_stat.pk)
        self.assertEqual(response.data["name"], pokeathlon_stat.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], pokeathlon_stat_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            pokeathlon_stat_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokeathlon_stat_name.language.pk
            ),
        )

    # Characteristic Tests
    def test_characteristic_api(self):
        characteristic = self.setup_characteristic_data(gene_mod_5=5)
        characteristic_description = self.setup_characteristic_description_data(
            characteristic, description="base char desc"
        )

        response = self.client.get(
            "{}/characteristic/{}/".format(API_V2, characteristic.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], characteristic.pk)
        self.assertEqual(response.data["gene_modulo"], characteristic.gene_mod_5)
        # name params
        self.assertEqual(
            response.data["descriptions"][0]["description"],
            characteristic_description.description,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["name"],
            characteristic_description.language.name,
        )
        self.assertEqual(
            response.data["descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, characteristic_description.language.pk
            ),
        )
        # stat params
        self.assertEqual(
            response.data["highest_stat"]["name"], characteristic.stat.name
        )
        self.assertEqual(
            response.data["highest_stat"]["url"],
            "{}{}/stat/{}/".format(TEST_HOST, API_V2, characteristic.stat.pk),
        )

    def test_characteristic_values(self):
        # check for all 5 possible values of gene_modulo
        for modulo in range(5):
            characteristic = self.setup_characteristic_data(gene_mod_5=modulo)
            # note that 'possible_values' is computed solely from gene_modulo
            # thus it is fine that our test characteristics are indexed 1-5
            result = self.client.get(
                "{}/characteristic/{}/".format(API_V2, characteristic.pk)
            )
            for i in range(len(result.data["possible_values"])):
                self.assertEqual(
                    result.data["possible_values"][i], characteristic.gene_mod_5 + i * 5
                )

    # Nature Tests
    def test_nature_api(self):
        hates_flavor = self.setup_berry_flavor_data(name="hts flvr for base ntr")
        likes_flavor = self.setup_berry_flavor_data(name="lks flvr for base ntr")
        decreased_stat = self.setup_stat_data(name="dcrs stt for base ntr")
        increased_stat = self.setup_stat_data(name="ncrs stt for base ntr")
        nature = self.setup_nature_data(
            name="base ntr",
            hates_flavor=hates_flavor,
            likes_flavor=likes_flavor,
            decreased_stat=decreased_stat,
            increased_stat=increased_stat,
        )
        nature_name = self.setup_nature_name_data(nature, name="base ntr name")

        pokeathlon_stat = self.setup_pokeathlon_stat_data(
            name="pkeathln stt for ntr stt"
        )
        nature_pokeathlon_stat = self.setup_nature_pokeathlon_stat_data(
            nature=nature, pokeathlon_stat=pokeathlon_stat, max_change=1
        )

        move_battle_style = self.setup_move_battle_style_data(
            name="mv btl stl for ntr stt"
        )
        nature_battle_style_preference = self.setup_nature_battle_style_preference_data(
            nature=nature, move_battle_style=move_battle_style
        )

        response = self.client.get("{}/nature/{}/".format(API_V2, nature.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], nature.pk)
        self.assertEqual(response.data["name"], nature.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], nature_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"], nature_name.language.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(TEST_HOST, API_V2, nature_name.language.pk),
        )
        # stat params
        self.assertEqual(response.data["decreased_stat"]["name"], decreased_stat.name)
        self.assertEqual(
            response.data["decreased_stat"]["url"],
            "{}{}/stat/{}/".format(TEST_HOST, API_V2, decreased_stat.pk),
        )
        self.assertEqual(response.data["increased_stat"]["name"], increased_stat.name)
        self.assertEqual(
            response.data["increased_stat"]["url"],
            "{}{}/stat/{}/".format(TEST_HOST, API_V2, increased_stat.pk),
        )
        # flavor params
        self.assertEqual(response.data["hates_flavor"]["name"], hates_flavor.name)
        self.assertEqual(
            response.data["hates_flavor"]["url"],
            "{}{}/berry-flavor/{}/".format(TEST_HOST, API_V2, hates_flavor.pk),
        )
        self.assertEqual(response.data["likes_flavor"]["name"], likes_flavor.name)
        self.assertEqual(
            response.data["likes_flavor"]["url"],
            "{}{}/berry-flavor/{}/".format(TEST_HOST, API_V2, likes_flavor.pk),
        )
        # pokeathlon stat params
        self.assertEqual(
            response.data["pokeathlon_stat_changes"][0]["max_change"],
            nature_pokeathlon_stat.max_change,
        )
        self.assertEqual(
            response.data["pokeathlon_stat_changes"][0]["pokeathlon_stat"]["name"],
            pokeathlon_stat.name,
        )
        self.assertEqual(
            response.data["pokeathlon_stat_changes"][0]["pokeathlon_stat"]["url"],
            "{}{}/pokeathlon-stat/{}/".format(TEST_HOST, API_V2, pokeathlon_stat.pk),
        )
        # pokeathlon stat params
        self.assertEqual(
            response.data["move_battle_style_preferences"][0]["low_hp_preference"],
            nature_battle_style_preference.low_hp_preference,
        )
        self.assertEqual(
            response.data["move_battle_style_preferences"][0]["high_hp_preference"],
            nature_battle_style_preference.high_hp_preference,
        )
        self.assertEqual(
            response.data["move_battle_style_preferences"][0]["move_battle_style"][
                "name"
            ],
            move_battle_style.name,
        )
        self.assertEqual(
            response.data["move_battle_style_preferences"][0]["move_battle_style"][
                "url"
            ],
            "{}{}/move-battle-style/{}/".format(
                TEST_HOST, API_V2, move_battle_style.pk
            ),
        )

    # Pokemon Tests
    def test_pokemon_habitat_api(self):
        pokemon_habitat = self.setup_pokemon_habitat_data(name="base pkmn hbtt trgr")
        pokemon_habitat_name = self.setup_pokemon_habitat_name_data(
            pokemon_habitat, name="base pkmn hbtt name"
        )
        pokemon_species = self.setup_pokemon_species_data(
            pokemon_habitat=pokemon_habitat, name="pkmn spcs for pkmn hbtt"
        )

        response = self.client.get(
            "{}/pokemon-habitat/{}/".format(API_V2, pokemon_habitat.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokemon_habitat.pk)
        self.assertEqual(response.data["name"], pokemon_habitat.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], pokemon_habitat_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            pokemon_habitat_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_habitat_name.language.pk
            ),
        )
        # species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    def test_pokemon_color_api(self):
        pokemon_color = self.setup_pokemon_color_data(name="base pkmn clr trgr")
        pokemon_color_name = self.setup_pokemon_color_name_data(
            pokemon_color, name="base pkmn clr name"
        )
        pokemon_species = self.setup_pokemon_species_data(
            pokemon_color=pokemon_color, name="pkmn spcs for pkmn clr"
        )

        response = self.client.get(
            "{}/pokemon-color/{}/".format(API_V2, pokemon_color.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokemon_color.pk)
        self.assertEqual(response.data["name"], pokemon_color.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], pokemon_color_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            pokemon_color_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_color_name.language.pk
            ),
        )
        # species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    def test_pokemon_shape_api(self):
        pokemon_shape = self.setup_pokemon_shape_data(name="base pkmn shp trgr")
        pokemon_shape_name = self.setup_pokemon_shape_name_data(
            pokemon_shape, name="base pkmn shp name"
        )
        pokemon_species = self.setup_pokemon_species_data(
            pokemon_shape=pokemon_shape, name="pkmn spcs for pkmn shp"
        )

        response = self.client.get(
            "{}/pokemon-shape/{}/".format(API_V2, pokemon_shape.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokemon_shape.pk)
        self.assertEqual(response.data["name"], pokemon_shape.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], pokemon_shape_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            pokemon_shape_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_shape_name.language.pk
            ),
        )
        # awesome name params
        self.assertEqual(
            response.data["awesome_names"][0]["awesome_name"],
            pokemon_shape_name.awesome_name,
        )
        self.assertEqual(
            response.data["awesome_names"][0]["language"]["name"],
            pokemon_shape_name.language.name,
        )
        self.assertEqual(
            response.data["awesome_names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_shape_name.language.pk
            ),
        )
        # species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    def test_pokemon_species_api(self):
        evolves_from_species = self.setup_pokemon_species_data(
            name="evolves from pkmn spcs"
        )
        pokemon_species = self.setup_pokemon_species_data(
            evolves_from_species=evolves_from_species, name="base pkmn spcs"
        )
        pokemon_species_name = self.setup_pokemon_species_name_data(
            pokemon_species, name="base pkmn shp name"
        )
        pokemon_species_form_description = (
            self.setup_pokemon_species_form_description_data(
                pokemon_species, description="frm dscr for pkmn spcs"
            )
        )
        pokemon_species_flavor_text = self.setup_pokemon_species_flavor_text_data(
            pokemon_species, flavor_text="flvr txt for pkmn spcs"
        )
        pokedex = self.setup_pokedex_data(name="pkdx for pkmn spcs")

        pal_park = self.setup_pal_park_data(pokemon_species=pokemon_species)

        dex_number = self.setup_pokemon_dex_entry_data(
            pokemon_species=pokemon_species, pokedex=pokedex, entry_number=44
        )

        egg_group = self.setup_egg_group_data(name="egg grp for pkmn spcs")
        self.setup_pokemon_egg_group_data(
            pokemon_species=pokemon_species, egg_group=egg_group
        )

        pokemon = self.setup_pokemon_data(
            pokemon_species=pokemon_species, name="pkm for base pkmn spcs"
        )
        self.setup_pokemon_sprites_data(pokemon)

        response = self.client.get(
            "{}/pokemon-species/{}/".format(API_V2, pokemon_species.pk),
            HTTP_HOST="testserver",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokemon_species.pk)
        self.assertEqual(response.data["name"], pokemon_species.name)
        self.assertEqual(response.data["order"], pokemon_species.order)
        self.assertEqual(response.data["capture_rate"], pokemon_species.capture_rate)
        self.assertEqual(response.data["gender_rate"], pokemon_species.gender_rate)
        self.assertEqual(
            response.data["base_happiness"], pokemon_species.base_happiness
        )
        self.assertEqual(response.data["is_baby"], pokemon_species.is_baby)
        self.assertEqual(response.data["is_legendary"], pokemon_species.is_legendary)
        self.assertEqual(response.data["is_mythical"], pokemon_species.is_mythical)

        self.assertEqual(response.data["hatch_counter"], pokemon_species.hatch_counter)
        self.assertEqual(
            response.data["has_gender_differences"],
            pokemon_species.has_gender_differences,
        )
        self.assertEqual(
            response.data["forms_switchable"], pokemon_species.forms_switchable
        )
        # name params
        self.assertEqual(response.data["names"][0]["name"], pokemon_species_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            pokemon_species_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_species_name.language.pk
            ),
        )
        # growth rate params
        self.assertEqual(
            response.data["growth_rate"]["name"], pokemon_species.growth_rate.name
        )
        self.assertEqual(
            response.data["growth_rate"]["url"],
            "{}{}/growth-rate/{}/".format(
                TEST_HOST, API_V2, pokemon_species.growth_rate.pk
            ),
        )
        # dex number params
        self.assertEqual(
            response.data["pokedex_numbers"][0]["entry_number"],
            dex_number.pokedex_number,
        )
        self.assertEqual(
            response.data["pokedex_numbers"][0]["pokedex"]["name"], pokedex.name
        )
        self.assertEqual(
            response.data["pokedex_numbers"][0]["pokedex"]["url"],
            "{}{}/pokedex/{}/".format(TEST_HOST, API_V2, pokedex.pk),
        )
        # egg group params
        self.assertEqual(response.data["egg_groups"][0]["name"], egg_group.name)
        self.assertEqual(
            response.data["egg_groups"][0]["url"],
            "{}{}/egg-group/{}/".format(TEST_HOST, API_V2, egg_group.pk),
        )
        # generation params
        self.assertEqual(
            response.data["generation"]["name"], pokemon_species.generation.name
        )
        self.assertEqual(
            response.data["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, pokemon_species.generation.pk
            ),
        )
        # color params
        self.assertEqual(
            response.data["color"]["name"], pokemon_species.pokemon_color.name
        )
        self.assertEqual(
            response.data["color"]["url"],
            "{}{}/pokemon-color/{}/".format(
                TEST_HOST, API_V2, pokemon_species.pokemon_color.pk
            ),
        )
        # shape params
        self.assertEqual(
            response.data["shape"]["name"], pokemon_species.pokemon_shape.name
        )
        self.assertEqual(
            response.data["shape"]["url"],
            "{}{}/pokemon-shape/{}/".format(
                TEST_HOST, API_V2, pokemon_species.pokemon_shape.pk
            ),
        )
        # habitat params
        self.assertEqual(
            response.data["habitat"]["name"], pokemon_species.pokemon_habitat.name
        )
        self.assertEqual(
            response.data["habitat"]["url"],
            "{}{}/pokemon-habitat/{}/".format(
                TEST_HOST, API_V2, pokemon_species.pokemon_habitat.pk
            ),
        )
        # evolves from params
        self.assertEqual(
            response.data["evolves_from_species"]["name"], evolves_from_species.name
        )
        self.assertEqual(
            response.data["evolves_from_species"]["url"],
            "{}{}/pokemon-species/{}/".format(
                TEST_HOST, API_V2, evolves_from_species.pk
            ),
        )
        # genus params
        self.assertEqual(
            response.data["genera"][0]["genus"], pokemon_species_name.genus
        )
        self.assertEqual(
            response.data["genera"][0]["language"]["name"],
            pokemon_species_name.language.name,
        )
        self.assertEqual(
            response.data["genera"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_species_name.language.pk
            ),
        )
        # pokemon varieties params
        self.assertEqual(
            response.data["varieties"][0]["is_default"], pokemon.is_default
        )
        self.assertEqual(response.data["varieties"][0]["pokemon"]["name"], pokemon.name)
        self.assertEqual(
            response.data["varieties"][0]["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon.pk),
        )
        # form descriptions params
        self.assertEqual(
            response.data["form_descriptions"][0]["description"],
            pokemon_species_form_description.description,
        )
        self.assertEqual(
            response.data["form_descriptions"][0]["language"]["name"],
            pokemon_species_form_description.language.name,
        )
        self.assertEqual(
            response.data["form_descriptions"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_species_form_description.language.pk
            ),
        )
        # flavor text params
        self.assertEqual(
            response.data["flavor_text_entries"][0]["flavor_text"],
            pokemon_species_flavor_text.flavor_text,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["name"],
            pokemon_species_flavor_text.language.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pokemon_species_flavor_text.language.pk
            ),
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version"]["name"],
            pokemon_species_flavor_text.version.name,
        )
        self.assertEqual(
            response.data["flavor_text_entries"][0]["version"]["url"],
            "{}{}/version/{}/".format(
                TEST_HOST, API_V2, pokemon_species_flavor_text.version.pk
            ),
        )
        # pal park params
        self.assertEqual(
            response.data["pal_park_encounters"][0]["base_score"], pal_park.base_score
        )
        self.assertEqual(response.data["pal_park_encounters"][0]["rate"], pal_park.rate)
        self.assertEqual(
            response.data["pal_park_encounters"][0]["area"]["name"],
            pal_park.pal_park_area.name,
        )
        self.assertEqual(
            response.data["pal_park_encounters"][0]["area"]["url"],
            "{}{}/pal-park-area/{}/".format(
                TEST_HOST, API_V2, pal_park.pal_park_area.pk
            ),
        )

    def test_pokemon_api(self):
        pokemon_species = self.setup_pokemon_species_data(
            name="pkmn spcs for base pkmn"
        )
        pokemon = self.setup_pokemon_data(
            pokemon_species=pokemon_species, name="base pkm"
        )
        pokemon_form = self.setup_pokemon_form_data(
            pokemon=pokemon, name="pkm form for base pkmn"
        )
        generation = self.setup_generation_data(name="base gen")
        pokemon_ability = self.setup_pokemon_ability_data(pokemon=pokemon)
        pokemon_past_ability = self.setup_pokemon_past_ability_data(
            pokemon=pokemon, generation=generation
        )
        pokemon_stat = self.setup_pokemon_stat_data(pokemon=pokemon)
        pokemon_type = self.setup_pokemon_type_data(pokemon=pokemon)
        pokemon_past_type = self.setup_pokemon_past_type_data(
            pokemon=pokemon, generation=generation
        )
        pokemon_item = self.setup_pokemon_item_data(pokemon=pokemon)
        pokemon_sprites = self.setup_pokemon_sprites_data(pokemon=pokemon)
        pokemon_game_index = self.setup_pokemon_game_index_data(
            pokemon=pokemon, game_index=10
        )
        # To test issue #85, we will create one move that has multiple
        # learn levels in different version groups.  Later, we'll
        # assert that we only got one move record back.
        pokemon_move = self.setup_move_data(name="mv for pkmn")
        pokemon_moves = []
        for move in range(0, 4):
            version_group = self.setup_version_group_data(
                name="ver grp " + str(move) + " for pkmn"
            )
            new_move = self.setup_pokemon_move_data(
                pokemon=pokemon,
                move=pokemon_move,
                version_group=version_group,
                level=move,
            )
            pokemon_moves.append(new_move)

        encounter_method = self.setup_encounter_method_data(
            name="encntr mthd for lctn area"
        )
        location_area1 = self.setup_location_area_data(name="lctn1 area for base pkmn")
        encounter_slot1 = self.setup_encounter_slot_data(
            encounter_method, slot=1, rarity=30
        )
        self.setup_encounter_data(
            location_area=location_area1,
            pokemon=pokemon,
            encounter_slot=encounter_slot1,
            min_level=30,
            max_level=35,
        )
        location_area2 = self.setup_location_area_data(name="lctn2 area for base pkmn")
        encounter_slot2 = self.setup_encounter_slot_data(
            encounter_method, slot=2, rarity=40
        )
        self.setup_encounter_data(
            location_area=location_area2,
            pokemon=pokemon,
            encounter_slot=encounter_slot2,
            min_level=32,
            max_level=36,
        )
        response = self.client.get(
            "{}/pokemon/{}/".format(API_V2, pokemon.pk), HTTP_HOST="testserver"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokemon.pk)
        self.assertEqual(response.data["name"], pokemon.name)
        self.assertEqual(response.data["order"], pokemon.order)
        self.assertEqual(response.data["is_default"], pokemon.is_default)
        self.assertEqual(response.data["height"], pokemon.height)
        self.assertEqual(response.data["weight"], pokemon.weight)
        self.assertEqual(response.data["base_experience"], pokemon.base_experience)
        # species params
        self.assertEqual(response.data["species"]["name"], pokemon_species.name)
        self.assertEqual(
            response.data["species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )
        # abilities params
        self.assertEqual(
            response.data["abilities"][0]["is_hidden"], pokemon_ability.is_hidden
        )
        self.assertEqual(response.data["abilities"][0]["slot"], pokemon_ability.slot)
        self.assertEqual(
            response.data["abilities"][0]["ability"]["name"],
            pokemon_ability.ability.name,
        )
        self.assertEqual(
            response.data["abilities"][0]["ability"]["url"],
            "{}{}/ability/{}/".format(TEST_HOST, API_V2, pokemon_ability.ability.pk),
        )
        # past abilities params
        past_abilities_obj = response.data["past_abilities"][0]
        self.assertEqual(
            past_abilities_obj["generation"]["name"],
            pokemon_past_ability.generation.name,
        )
        self.assertEqual(
            past_abilities_obj["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, pokemon_past_ability.generation.pk
            ),
        )

        past_abilities_abilities_obj = past_abilities_obj["abilities"][0]
        self.assertEqual(
            past_abilities_abilities_obj["is_hidden"], pokemon_past_ability.is_hidden
        )
        self.assertEqual(
            past_abilities_abilities_obj["slot"], pokemon_past_ability.slot
        )
        self.assertEqual(
            past_abilities_abilities_obj["ability"]["name"],
            pokemon_past_ability.ability.name,
        )
        self.assertEqual(
            past_abilities_abilities_obj["ability"]["url"],
            "{}{}/ability/{}/".format(
                TEST_HOST, API_V2, pokemon_past_ability.ability.pk
            ),
        )
        # stat params
        self.assertEqual(response.data["stats"][0]["base_stat"], pokemon_stat.base_stat)
        self.assertEqual(response.data["stats"][0]["effort"], pokemon_stat.effort)
        self.assertEqual(
            response.data["stats"][0]["stat"]["name"], pokemon_stat.stat.name
        )
        self.assertEqual(
            response.data["stats"][0]["stat"]["url"],
            "{}{}/stat/{}/".format(TEST_HOST, API_V2, pokemon_stat.stat.pk),
        )
        # type params
        self.assertEqual(response.data["types"][0]["slot"], pokemon_type.slot)
        self.assertEqual(
            response.data["types"][0]["type"]["name"], pokemon_type.type.name
        )
        self.assertEqual(
            response.data["types"][0]["type"]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, pokemon_type.type.pk),
        )
        # past type params
        past_types_obj = response.data["past_types"][0]
        self.assertEqual(
            past_types_obj["generation"]["name"], pokemon_past_type.generation.name
        )
        self.assertEqual(
            past_types_obj["generation"]["url"],
            "{}{}/generation/{}/".format(
                TEST_HOST, API_V2, pokemon_past_type.generation.pk
            ),
        )

        past_types_types_obj = past_types_obj["types"][0]
        self.assertEqual(past_types_types_obj["slot"], pokemon_past_type.slot)
        self.assertEqual(
            past_types_types_obj["type"]["name"], pokemon_past_type.type.name
        )
        self.assertEqual(
            past_types_types_obj["type"]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, pokemon_past_type.type.pk),
        )

        # items params
        self.assertEqual(
            response.data["held_items"][0]["item"]["name"], pokemon_item.item.name
        )
        self.assertEqual(
            response.data["held_items"][0]["item"]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, pokemon_item.item.pk),
        )
        self.assertEqual(
            response.data["held_items"][0]["version_details"][0]["rarity"],
            pokemon_item.rarity,
        )
        self.assertEqual(
            response.data["held_items"][0]["version_details"][0]["version"]["name"],
            pokemon_item.version.name,
        )
        self.assertEqual(
            response.data["held_items"][0]["version_details"][0]["version"]["url"],
            "{}{}/version/{}/".format(TEST_HOST, API_V2, pokemon_item.version.pk),
        )
        # move params -- Make sure that we only got one move back,
        # but that we got all of the distinct version group and learn
        # level values. (See issue #85)
        # Number of Moves
        expected = 1
        actual = len(response.data["moves"])
        self.assertEqual(expected, actual)
        # Move name
        expected = pokemon_moves[0].move.name
        actual = response.data["moves"][0]["move"]["name"]
        self.assertEqual(expected, actual)
        # Move URL
        expected = "{}{}/move/{}/".format(TEST_HOST, API_V2, pokemon_moves[0].move.pk)
        actual = response.data["moves"][0]["move"]["url"]
        self.assertEqual(expected, actual)
        # Numbver of version groups
        expected = len(pokemon_moves)
        actual = len(response.data["moves"][0]["version_group_details"])
        self.assertEqual(expected, actual)

        for i, val in enumerate(pokemon_moves):  # pylint: disable=unused-variable
            version = response.data["moves"][0]["version_group_details"][i]
            # Learn Level
            expected = pokemon_moves[i].level
            actual = version["level_learned_at"]
            self.assertEqual(expected, actual)
            # Version Group Name
            expected = pokemon_moves[i].version_group.name
            actual = version["version_group"]["name"]
            self.assertEqual(expected, actual)
            # Version Group URL
            expected = "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, pokemon_moves[i].version_group.pk
            )
            actual = version["version_group"]["url"]
            self.assertEqual(expected, actual)
            # Learn Method Name
            expected = pokemon_moves[i].move_learn_method.name
            actual = version["move_learn_method"]["name"]
            self.assertEqual(expected, actual)
            # Learn Method URL
            expected = "{}{}/move-learn-method/{}/".format(
                TEST_HOST, API_V2, pokemon_moves[i].move_learn_method.pk
            )
            actual = version["move_learn_method"]["url"]
            self.assertEqual(expected, actual)
        # game indices params
        self.assertEqual(
            response.data["game_indices"][0]["game_index"],
            pokemon_game_index.game_index,
        )
        self.assertEqual(
            response.data["game_indices"][0]["version"]["name"],
            pokemon_game_index.version.name,
        )
        self.assertEqual(
            response.data["game_indices"][0]["version"]["url"],
            "{}{}/version/{}/".format(TEST_HOST, API_V2, pokemon_game_index.version.pk),
        )
        # form params
        self.assertEqual(response.data["forms"][0]["name"], pokemon_form.name)
        self.assertEqual(
            response.data["forms"][0]["url"],
            "{}{}/pokemon-form/{}/".format(TEST_HOST, API_V2, pokemon_form.pk),
        )

        sprites_data = json.loads(pokemon_sprites.sprites)

        # sprite params
        self.assertEqual(
            sprites_data["front_default"],
            "{}".format(sprites_data["front_default"]),
        )
        self.assertEqual(sprites_data["back_default"], None)

    def test_pokemon_form_api(self):
        pokemon_species = self.setup_pokemon_species_data()
        pokemon = self.setup_pokemon_data(pokemon_species=pokemon_species)
        pokemon_form = self.setup_pokemon_form_data(
            pokemon=pokemon, name="pkm form for base pkmn"
        )
        pokemon_form_sprites = self.setup_pokemon_form_sprites_data(pokemon_form)
        pokemon_form_type = self.setup_pokemon_form_type_data(pokemon_form)

        response = self.client.get(
            "{}/pokemon-form/{}/".format(API_V2, pokemon_form.pk),
            HTTP_HOST="testserver",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pokemon_form.pk)
        self.assertEqual(response.data["name"], pokemon_form.name)
        self.assertEqual(response.data["form_name"], pokemon_form.form_name)
        self.assertEqual(response.data["order"], pokemon_form.order)
        self.assertEqual(response.data["form_order"], pokemon_form.form_order)
        self.assertEqual(response.data["is_default"], pokemon_form.is_default)
        self.assertEqual(response.data["is_battle_only"], pokemon_form.is_battle_only)
        self.assertEqual(response.data["is_mega"], pokemon_form.is_mega)
        # pokemon params
        self.assertEqual(response.data["pokemon"]["name"], pokemon.name)
        self.assertEqual(
            response.data["pokemon"]["url"],
            "{}{}/pokemon/{}/".format(TEST_HOST, API_V2, pokemon.pk),
        )
        # version group params
        self.assertEqual(
            response.data["version_group"]["name"], pokemon_form.version_group.name
        )
        self.assertEqual(
            response.data["version_group"]["url"],
            "{}{}/version-group/{}/".format(
                TEST_HOST, API_V2, pokemon_form.version_group.pk
            ),
        )

        sprites_data = json.loads(pokemon_form_sprites.sprites)

        # sprite params
        self.assertEqual(
            sprites_data["front_default"],
            "{}".format(sprites_data["front_default"]),
        )
        self.assertEqual(sprites_data["back_default"], None)
        # type params
        self.assertEqual(response.data["types"][0]["slot"], pokemon_form_type.slot)
        self.assertEqual(
            response.data["types"][0]["type"]["name"], pokemon_form_type.type.name
        )
        self.assertEqual(
            response.data["types"][0]["type"]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, pokemon_form_type.type.pk),
        )

    # Evolution test
    def test_evolution_trigger_api(self):
        evolution_trigger = self.setup_evolution_trigger_data(name="base evltn trgr")
        evolution_trigger_name = self.setup_evolution_trigger_name_data(
            evolution_trigger, name="base evltn trgr name"
        )
        pokemon_species = self.setup_pokemon_species_data(
            name="pkmn spcs for base evltn trgr"
        )
        self.setup_pokemon_evolution_data(
            evolved_species=pokemon_species, evolution_trigger=evolution_trigger
        )

        response = self.client.get(
            "{}/evolution-trigger/{}/".format(API_V2, evolution_trigger.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], evolution_trigger.pk)
        self.assertEqual(response.data["name"], evolution_trigger.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], evolution_trigger_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            evolution_trigger_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, evolution_trigger_name.language.pk
            ),
        )
        # pokemon species params
        self.assertEqual(
            response.data["pokemon_species"][0]["name"], pokemon_species.name
        )
        self.assertEqual(
            response.data["pokemon_species"][0]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    def test_evolution_chain_api(self):
        baby_trigger_item = self.setup_item_data(name="bby itm for evo chn")
        evolution_chain = self.setup_evolution_chain_data(
            baby_trigger_item=baby_trigger_item
        )

        baby = self.setup_pokemon_species_data(
            name="bby for evo chn", is_baby=True, evolution_chain=evolution_chain
        )

        basic = self.setup_pokemon_species_data(
            name="bsc for evo chn",
            evolves_from_species=baby,
            evolution_chain=evolution_chain,
        )
        basic_location = self.setup_location_data(name="lctn for bsc evo chn")
        basic_evolution = self.setup_pokemon_evolution_data(
            evolved_species=basic, min_level=5, location=basic_location
        )

        stage_one = self.setup_pokemon_species_data(
            name="stg one for evo chn",
            evolves_from_species=basic,
            evolution_chain=evolution_chain,
        )
        stage_one_held_item = self.setup_item_data(name="itm for stg one evo chn")
        stage_one_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_one, min_level=18, held_item=stage_one_held_item
        )

        stage_two_first = self.setup_pokemon_species_data(
            name="stg two frst for evo chn",
            evolves_from_species=stage_one,
            evolution_chain=evolution_chain,
        )
        stage_two_first_known_move = self.setup_move_data(name="mv for evo chn")
        stage_two_first_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_two_first,
            min_level=32,
            known_move=stage_two_first_known_move,
        )

        stage_two_second = self.setup_pokemon_species_data(
            name="stg two scnd for evo chn",
            evolves_from_species=stage_one,
            evolution_chain=evolution_chain,
        )
        stage_two_second_party_type = self.setup_type_data(name="tp for evo chn")
        stage_two_second_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_two_second,
            min_level=32,
            party_type=stage_two_second_party_type,
        )

        response = self.client.get(
            "{}/evolution-chain/{}/".format(API_V2, evolution_chain.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        baby_data = response.data["chain"]
        basic_data = baby_data["evolves_to"][0]
        stage_one_data = basic_data["evolves_to"][0]
        stage_two_first_data = stage_one_data["evolves_to"][0]
        stage_two_second_data = stage_one_data["evolves_to"][1]

        # base params
        self.assertEqual(response.data["id"], evolution_chain.pk)
        # baby trigger params
        self.assertEqual(
            response.data["baby_trigger_item"]["name"], baby_trigger_item.name
        )
        self.assertEqual(
            response.data["baby_trigger_item"]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, baby_trigger_item.pk),
        )
        # baby params
        self.assertEqual(baby_data["is_baby"], baby.is_baby)
        self.assertEqual(baby_data["species"]["name"], baby.name)
        self.assertEqual(
            baby_data["species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, baby.pk),
        )
        # basic params
        self.assertEqual(basic_data["is_baby"], basic.is_baby)
        self.assertEqual(basic_data["species"]["name"], basic.name)
        self.assertEqual(
            basic_data["species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, basic.pk),
        )
        self.assertEqual(
            basic_data["evolution_details"][0]["min_level"], basic_evolution.min_level
        )
        self.assertEqual(
            basic_data["evolution_details"][0]["location"]["name"], basic_location.name
        )
        self.assertEqual(
            basic_data["evolution_details"][0]["location"]["url"],
            "{}{}/location/{}/".format(TEST_HOST, API_V2, basic_location.pk),
        )
        # stage one params
        self.assertEqual(stage_one_data["is_baby"], stage_one.is_baby)
        self.assertEqual(stage_one_data["species"]["name"], stage_one.name)
        self.assertEqual(
            stage_one_data["species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, stage_one.pk),
        )
        self.assertEqual(
            stage_one_data["evolution_details"][0]["min_level"],
            stage_one_evolution.min_level,
        )
        self.assertEqual(
            stage_one_data["evolution_details"][0]["held_item"]["name"],
            stage_one_held_item.name,
        )
        self.assertEqual(
            stage_one_data["evolution_details"][0]["held_item"]["url"],
            "{}{}/item/{}/".format(TEST_HOST, API_V2, stage_one_held_item.pk),
        )
        # stage two first params
        self.assertEqual(stage_two_first_data["is_baby"], stage_two_first.is_baby)
        self.assertEqual(stage_two_first_data["species"]["name"], stage_two_first.name)
        self.assertEqual(
            stage_two_first_data["species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, stage_two_first.pk),
        )
        self.assertEqual(
            stage_two_first_data["evolution_details"][0]["min_level"],
            stage_two_first_evolution.min_level,
        )
        self.assertEqual(
            stage_two_first_data["evolution_details"][0]["known_move"]["name"],
            stage_two_first_known_move.name,
        )
        self.assertEqual(
            stage_two_first_data["evolution_details"][0]["known_move"]["url"],
            "{}{}/move/{}/".format(TEST_HOST, API_V2, stage_two_first_known_move.pk),
        )
        # stage two second params
        self.assertEqual(stage_two_second_data["is_baby"], stage_two_second.is_baby)
        self.assertEqual(
            stage_two_second_data["species"]["name"], stage_two_second.name
        )
        self.assertEqual(
            stage_two_second_data["species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, stage_two_second.pk),
        )
        self.assertEqual(
            stage_two_second_data["evolution_details"][0]["min_level"],
            stage_two_second_evolution.min_level,
        )
        self.assertEqual(
            stage_two_second_data["evolution_details"][0]["party_type"]["name"],
            stage_two_second_party_type.name,
        )
        self.assertEqual(
            stage_two_second_data["evolution_details"][0]["party_type"]["url"],
            "{}{}/type/{}/".format(TEST_HOST, API_V2, stage_two_second_party_type.pk),
        )

    # verifies that the wurmple evolution chain is serialized correctly
    def test_evolution_chain_api_wurmple_bugfix(self):
        # set up wurmple-like evolution chain
        evolution_chain = self.setup_evolution_chain_data()

        basic = self.setup_pokemon_species_data(
            name="wurmple",
            evolution_chain=evolution_chain,
        )

        stage_one_first = self.setup_pokemon_species_data(
            name="silcoon",
            evolves_from_species=basic,
            evolution_chain=evolution_chain,
        )
        stage_one_first_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_one_first, min_level=7
        )

        stage_two_first = self.setup_pokemon_species_data(
            name="beautifly",
            evolves_from_species=stage_one_first,
            evolution_chain=evolution_chain,
        )
        stage_two_first_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_two_first, min_level=10
        )

        stage_one_second = self.setup_pokemon_species_data(
            name="cascoon",
            evolves_from_species=basic,
            evolution_chain=evolution_chain,
        )
        stage_one_second_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_one_second, min_level=7
        )

        stage_two_second = self.setup_pokemon_species_data(
            name="dustox",
            evolves_from_species=stage_one_second,
            evolution_chain=evolution_chain,
        )
        stage_two_second_evolution = self.setup_pokemon_evolution_data(
            evolved_species=stage_two_second, min_level=10
        )

        response = self.client.get(
            "{}/evolution-chain/{}/".format(API_V2, evolution_chain.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], evolution_chain.pk)

        # assert tree has been serialized correctly
        basic_data = response.data["chain"]
        self.assertEqual(len(basic_data["evolves_to"]), 2)

        stage_one_first_data = basic_data["evolves_to"][0]
        self.assertEqual(len(stage_one_first_data["evolves_to"]), 1)

        stage_one_second_data = basic_data["evolves_to"][1]
        self.assertEqual(len(stage_one_second_data["evolves_to"]), 1)

    # Encounter Tests
    def test_encounter_method_api(self):
        encounter_method = self.setup_encounter_method_data(name="base encntr mthd")
        encounter_method_name = self.setup_encounter_method_name_data(
            encounter_method, name="base encntr mthd name"
        )

        response = self.client.get(
            "{}/encounter-method/{}/".format(API_V2, encounter_method.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], encounter_method.pk)
        self.assertEqual(response.data["name"], encounter_method.name)
        self.assertEqual(response.data["order"], encounter_method.order)
        # name params
        self.assertEqual(response.data["names"][0]["name"], encounter_method_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            encounter_method_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, encounter_method_name.language.pk
            ),
        )

    def test_encounter_condition_value_api(self):
        encounter_condition = self.setup_encounter_condition_data(
            name="encntr cndtn for base encntr cndtn vlu"
        )
        encounter_condition_value = self.setup_encounter_condition_value_data(
            encounter_condition, name="base encntr cndtn vlu"
        )
        encounter_condition_value_name = self.setup_encounter_condition_value_name_data(
            encounter_condition_value, name="base encntr cndtn vlu name"
        )

        response = self.client.get(
            "{}/encounter-condition-value/{}/".format(
                API_V2, encounter_condition_value.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], encounter_condition_value.pk)
        self.assertEqual(response.data["name"], encounter_condition_value.name)
        # name params
        self.assertEqual(
            response.data["names"][0]["name"], encounter_condition_value_name.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            encounter_condition_value_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, encounter_condition_value_name.language.pk
            ),
        )
        # condition params
        self.assertEqual(response.data["condition"]["name"], encounter_condition.name)
        self.assertEqual(
            response.data["condition"]["url"],
            "{}{}/encounter-condition/{}/".format(
                TEST_HOST, API_V2, encounter_condition.pk
            ),
        )

    def test_encounter_condition_api(self):
        encounter_condition = self.setup_encounter_condition_data(
            name="base encntr cndtn"
        )
        encounter_condition_name = self.setup_encounter_condition_name_data(
            encounter_condition, name="base encntr cndtn name"
        )
        encounter_condition_value = self.setup_encounter_condition_value_data(
            encounter_condition,
            name="encntr cndtn vlu for base encntr",
            is_default=True,
        )

        response = self.client.get(
            "{}/encounter-condition/{}/".format(API_V2, encounter_condition.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], encounter_condition.pk)
        self.assertEqual(response.data["name"], encounter_condition.name)
        # name params
        self.assertEqual(
            response.data["names"][0]["name"], encounter_condition_name.name
        )
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            encounter_condition_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, encounter_condition_name.language.pk
            ),
        )
        # value params
        self.assertEqual(
            response.data["values"][0]["name"], encounter_condition_value.name
        )
        self.assertEqual(
            response.data["values"][0]["url"],
            "{}{}/encounter-condition-value/{}/".format(
                TEST_HOST, API_V2, encounter_condition_value.pk
            ),
        )

    # Pal Park Tests
    def test_pal_park_area_api(self):
        pal_park_area = self.setup_pal_park_area_data(name="base pl prk area")
        pal_park_area_name = self.setup_pal_park_area_name_data(
            pal_park_area, name="base pl prk area nm"
        )
        pokemon_species = self.setup_pokemon_species_data(name="pkmn spcs for pl prk")
        pal_park = self.setup_pal_park_data(
            pal_park_area=pal_park_area,
            pokemon_species=pokemon_species,
            base_score=10,
            rate=20,
        )

        response = self.client.get(
            "{}/pal-park-area/{}/".format(API_V2, pal_park_area.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data["id"], pal_park_area.pk)
        self.assertEqual(response.data["name"], pal_park_area.name)
        # name params
        self.assertEqual(response.data["names"][0]["name"], pal_park_area_name.name)
        self.assertEqual(
            response.data["names"][0]["language"]["name"],
            pal_park_area_name.language.name,
        )
        self.assertEqual(
            response.data["names"][0]["language"]["url"],
            "{}{}/language/{}/".format(
                TEST_HOST, API_V2, pal_park_area_name.language.pk
            ),
        )
        # encounter params
        self.assertEqual(
            response.data["pokemon_encounters"][0]["base_score"], pal_park.base_score
        )
        self.assertEqual(response.data["pokemon_encounters"][0]["rate"], pal_park.rate)
        self.assertEqual(
            response.data["pokemon_encounters"][0]["pokemon_species"]["name"],
            pokemon_species.name,
        )
        self.assertEqual(
            response.data["pokemon_encounters"][0]["pokemon_species"]["url"],
            "{}{}/pokemon-species/{}/".format(TEST_HOST, API_V2, pokemon_species.pk),
        )

    # ID Range Tests
    def test_id_range_api(self):
        response = self.client.get("{}/pokemon/{}/".format(API_V2, 2147483648))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
