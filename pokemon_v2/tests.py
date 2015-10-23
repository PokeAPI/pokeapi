from __future__ import unicode_literals
# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from pokemon_v2.models import *

#u'http://testserver/api/v2/language/1/'


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

        language_name = LanguageName.objects.create (
            language = language,
            local_language_id = language.pk,
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
            name='lang for '+region.name)

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


class VersionGroupData(GenerationData):

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


class VersionData(VersionGroupData, LanguageData):

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


class AbilityData(GenerationData, VersionGroupData):

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
    def setup_ability_description_data(self, ability, short_effect='ablty shrt efct', effect='ablty efct'):

        language = self.setup_language_data(
            name='lang for '+effect)

        ability_description = AbilityDescription.objects.create (
            ability = ability,
            language = language,
            short_effect = short_effect,
            effect = effect
        )
        ability_description.save()

        return ability_description

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


class ItemAttributeData(LanguageData):

    @classmethod
    def setup_item_attribute_data(self, name="itm attr"):

        item_attribute = ItemAttribute.objects.create (
            name = name,
        )
        item_attribute.save()

        return item_attribute

    def setup_item_attribute_description_data(self, item_attribute, name='itm attr nm', description='itm attr desc'):

        """
        For some reason attribute names are a part of the description model.
        This should be changed to work like the rest of the models.
        """

        language = self.setup_language_data(
            name='lang for '+description)

        item_attribute_description = ItemAttributeDescription.objects.create (
            item_attribute = item_attribute,
            name = name,
            description = description,
            language = language
        )
        item_attribute_description.save()

        return item_attribute_description


class ItemCategoryData(LanguageData):

    @classmethod
    def setup_item_category_data(self, name="itm ctgry"):

        item_category = ItemCategory.objects.create (
            name = name,
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


class ItemFlingEffectData(LanguageData):

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


class ItemPocketData(LanguageData):

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



class ItemData(ItemCategoryData, ItemFlingEffectData, VersionGroupData):

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


class BerryFirmnessData(LanguageData):

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


class BerryData(BerryFirmnessData, ItemData, LanguageData):

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




""" 
Tests
"""

class LanguageTests(LanguageData, APITestCase):

    def test_language_api(self):

        language = self.setup_language_data(name='base lang')
        language_name = self.setup_language_name_data(language, name='base lang name')

        response = self.client.get('/api/v2/language/{}/'.format(language.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], language.pk)
        self.assertEqual(response.data['iso639'], language.iso639)
        self.assertEqual(response.data['iso3166'], language.iso3166)
        self.assertEqual(response.data['name'], language.name)
        self.assertEqual(response.data['official'], language.official)
        #name params
        self.assertEqual(response.data['names'][0]['name'], language_name.name)



class RegionTests(RegionData, APITestCase):

    def test_region_api(self):

        region = self.setup_region_data(name='base reg')
        region_name = self.setup_region_name_data(region, name='base reg name')

        response = self.client.get('/api/v2/region/{}/'.format(region.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], region.pk)
        self.assertEqual(response.data['name'], region.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], region_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], region_name.language.name)



class GenerationTests(GenerationData, APITestCase):

    def test_generation_api(self):

        generation = self.setup_generation_data(name='base gen')
        generation_name = self.setup_generation_name_data(generation, name='base reg name')

        response = self.client.get('/api/v2/generation/{}/'.format(generation.pk))

        # base params
        self.assertEqual(response.data['id'], generation.pk)
        self.assertEqual(response.data['name'], generation.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], generation_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], generation_name.language.name)
        # region params
        self.assertEqual(response.data['region']['name'], generation.region.name)



class VersionTests(VersionData, APITestCase):

    def test_version_api(self):

        version = self.setup_version_data(name='base ver')
        version_name = self.setup_version_name_data(version, name='base ver name')

        response = self.client.get('/api/v2/version/{}/'.format(version.pk))

        # base params
        self.assertEqual(response.data['id'], version.pk)
        self.assertEqual(response.data['name'], version.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], version_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], version_name.language.name)
        # version group params
        self.assertEqual(response.data['version_group']['name'], version.version_group.name)



class AbilityTests(AbilityData, APITestCase):

    def test_ability_api(self):

        ability = self.setup_ability_data(name='base ablty')
        ability_name = self.setup_ability_name_data(ability, name='base ablty name')
        ability_description = self.setup_ability_description_data(ability, effect='base ablty efct')
        ability_flavor_text = self.setup_ability_flavor_text_data(ability, flavor_text='base flvr txt')

        response = self.client.get('/api/v2/ability/{}/'.format(ability.pk))
        
        # base params
        self.assertEqual(response.data['id'], ability.pk)
        self.assertEqual(response.data['name'], ability.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], ability_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], ability_name.language.name)
        # description params
        self.assertEqual(response.data['descriptions'][0]['effect'], ability_description.effect)
        self.assertEqual(response.data['descriptions'][0]['short_effect'], ability_description.short_effect)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], ability_description.language.name)
        # flavor text params
        self.assertEqual(response.data['flavor_text_entries'][0]['text'], ability_flavor_text.flavor_text)
        self.assertEqual(response.data['flavor_text_entries'][0]['version_group']['name'], ability_flavor_text.version_group.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['name'], ability_flavor_text.language.name)
        # generation params
        self.assertEqual(response.data['generation']['name'], ability.generation.name)



class ItemAttributeTests(ItemAttributeData, APITestCase):

    def test_item_attribute_api(self):

        # item attribute data
        item_attribute = self.setup_item_attribute_data(name='base itm attr')
        # item_attribute_name = self.setup_item_attribute_name_data(item_attribute, name='base itm attr nm')
        item_attribute_description = self.setup_item_attribute_description_data(item_attribute, name='base itm attr desc')

        response = self.client.get('/api/v2/item-attribute/{}/'.format(item_attribute.pk))

        # base params
        self.assertEqual(response.data['id'], item_attribute.pk)
        self.assertEqual(response.data['name'], item_attribute.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_attribute_description.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_attribute_description.language.name)
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], item_attribute_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], item_attribute_description.language.name)



class ItemCategoryTests(ItemCategoryData, APITestCase):

    def test_item_category_api(self):

        # item category data
        item_category = self.setup_item_category_data(name='base itm ctgry')
        item_category_name = self.setup_item_category_name_data(item_category, name='base itm ctgry nm')

        response = self.client.get('/api/v2/item-category/{}/'.format(item_category.pk))

        # base params
        self.assertEqual(response.data['id'], item_category.pk)
        self.assertEqual(response.data['name'], item_category.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_category_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_category_name.language.name)



class ItemFlingEffectTests(ItemFlingEffectData, APITestCase):

    def test_item_fling_effect_api(self):

        # item category data
        item_fling_effect = self.setup_item_fling_effect_data(name='base itm flng efct')
        item_fling_effect_description = self.setup_item_fling_effect_description_data(item_fling_effect, description='base itm flng efct nm')

        response = self.client.get('/api/v2/item-fling-effect/{}/'.format(item_fling_effect.pk))

        # base params
        self.assertEqual(response.data['id'], item_fling_effect.pk)
        self.assertEqual(response.data['name'], item_fling_effect.name)
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], item_fling_effect_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], item_fling_effect_description.language.name)



class ItemPocketTests(ItemPocketData, APITestCase):

    def test_item_pocket_api(self):

        # item pocket data
        item_pocket = self.setup_item_pocket_data(name='base itm pkt')
        item_pocket_name = self.setup_item_pocket_name_data(item_pocket, name='base itm pkt nm')

        response = self.client.get('/api/v2/item-pocket/{}/'.format(item_pocket.pk))

        # base params
        self.assertEqual(response.data['id'], item_pocket.pk)
        self.assertEqual(response.data['name'], item_pocket.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_pocket_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_pocket_name.language.name)



class ItemTests(ItemData, ItemAttributeData, APITestCase):

    def test_item_api(self):

        item_category = self.setup_item_category_data(name='itm ctgry for base itm')
        item_fling_effect = self.setup_item_fling_effect_data(name='itm flng efct for base itm')

        item = self.setup_item_data(item_category, item_fling_effect, name='base itm')
        item_name = self.setup_item_name_data(item, name='base itm name')
        item_flavor_text = self.setup_item_flavor_text_data(item, flavor_text='base itm flvr txt')

        item_attribute = self.setup_item_attribute_data()

        # map item attribute to item
        item_attribute_map = ItemAttributeMap (
            item = item,
            item_attribute = item_attribute
          )
        item_attribute_map.save()

        response = self.client.get('/api/v2/item/{}/'.format(item.pk))
        
        # base params
        self.assertEqual(response.data['id'], item.pk)
        self.assertEqual(response.data['name'], item.name)
        self.assertEqual(response.data['cost'], item.cost)
        self.assertEqual(response.data['fling_power'], item.fling_power)
        # name params
        self.assertEqual(response.data['names'][0]['name'], item_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], item_name.language.name)
        # flavor text params
        self.assertEqual(response.data['flavor_text_entries'][0]['text'], item_flavor_text.flavor_text)
        self.assertEqual(response.data['flavor_text_entries'][0]['version_group']['name'], item_flavor_text.version_group.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['name'], item_flavor_text.language.name)
        # category params
        self.assertEqual(response.data['category']['name'], item_category.name)
        # fling effect params
        self.assertEqual(response.data['fling_effect']['name'], item_fling_effect.name)
        # attribute params
        self.assertEqual(response.data['attributes'][0]['name'], item_attribute.name)



class BerryFirmnessTests(BerryFirmnessData, APITestCase):

    def test_berry_firmness_api(self):

        berry_firmness = self.setup_berry_firmness_data(name='base bry frmns')
        berry_firmness_name = self.setup_berry_firmness_name_data(berry_firmness, name='base bry frmns nm')

        response = self.client.get('/api/v2/berry-firmness/{}/'.format(berry_firmness.pk))

        # base params
        self.assertEqual(response.data['id'], berry_firmness.pk)
        self.assertEqual(response.data['name'], berry_firmness.name)

        # name params
        self.assertEqual(response.data['names'][0]['name'], berry_firmness_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], berry_firmness_name.language.name)



class BerryTests(BerryData, APITestCase):

    def test_berry_api(self):

        # NEEDS NATURE

        # item pocket data
        berry = self.setup_berry_data(name='base bry')
        
        response = self.client.get('/api/v2/berry/{}/'.format(berry.pk))

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
        # item params
        self.assertEqual(response.data['item']['name'], berry.item.name)



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

        response = self.client.get('/api/v2/growth-rate/{}/'.format(growth_rate.pk))

        # base params
        self.assertEqual(response.data['id'], growth_rate.pk)
        self.assertEqual(response.data['name'], growth_rate.name)
        # description params
        self.assertEqual(response.data['descriptions'][0]['description'], growth_rate_description.description)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], growth_rate_description.language.name)
        # experience params
        self.assertEqual(response.data['levels'][0]['level'], experience.level)
        self.assertEqual(response.data['levels'][0]['experience'], experience.experience)


class LocationTests(LocationData, APITestCase):

    def test_location_api(self):

        location = self.setup_location_data(name='base lctn')
        location_name = self.setup_location_name_data(location, name='base lctn name')

        response = self.client.get('/api/v2/location/{}/'.format(location.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], location.pk)
        self.assertEqual(response.data['name'], location.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], location_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], location_name.language.name)
        # region params
        self.assertEqual(response.data['region']['name'], location.region.name)


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

        response = self.client.get('/api/v2/type/{}/'.format(type.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], type.pk)
        self.assertEqual(response.data['name'], type.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], type_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], type_name.language.name)
        # generation params
        self.assertEqual(response.data['generation']['name'], type.generation.name)
        # damage relations params
        self.assertEqual(response.data['damage_relations']['no_damage_to'][0]['name'], no_damage_to.name)
        self.assertEqual(response.data['damage_relations']['half_damage_to'][0]['name'], half_damage_to.name)
        self.assertEqual(response.data['damage_relations']['double_damage_to'][0]['name'], double_damage_to.name)
        self.assertEqual(response.data['damage_relations']['no_damage_from'][0]['name'], no_damage_from.name)
        self.assertEqual(response.data['damage_relations']['half_damage_from'][0]['name'], half_damage_from.name)
        self.assertEqual(response.data['damage_relations']['double_damage_from'][0]['name'], double_damage_from.name)



# class HeaderTest(TestCase):

#       def test_pokemon(self):

#         response = self.client.get(
#           '/api/v2/pokemon/1/',
#           HTTP_ORIGIN="http://pokemon.com"
#         )

#         self.assertEqual(response['Access-Control-Allow-Origin'], '*')


# class SpriteV2Resource(TestCase):
#     """
#     All tests for the Sprite V2 resource.
#     """

#     @classmethod
#     def setUpClass(self):
#         self.client = APIClient()

#     def test_get_sprite(self):
#         """
#         Get a single sprite.
#         """

#         sp = Sprite.objects.create(
#             name='test_sprite_image',
#             image='image_url.jpg'
#         )
#         sp.save()

#         url = '/api/v2/sprites/{}/'.format(sp.pk)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], sp.name)


#     def test_get_sprite_not_found(self):
#         """
#         Get a single sprite that doesn't exist, expects a 404 response
#         """


#         url = '/api/v2/sprites/{}/'.format(12344556)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_get_all_sprites(self):
#         """
#         Try to get all the sprites!
#         """

#         sp = Sprite.objects.create(
#             name='test_sprite_image',
#             image='image_url.jpg'
#         )
#         sp.save()

#         sp_2 = Sprite.objects.create(
#             name='test_sprite_image_two',
#             image='image_url_second.jpg'
#         )
#         sp_2.save()

#         url = '/api/v2/sprites/'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
