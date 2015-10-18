from __future__ import unicode_literals
# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from pokemon_v2.models import *


"""
Data Initializers
"""

class HasLanguage():

    @classmethod
    def setup_language_data(self):

        self.language = Language.objects.create (
            iso639 = 'ts',
            iso3166 = 'tt',
            name = 'test language',
            official = True,
            order = 1,
        )
        self.language.save()

        self.language_name = LanguageName.objects.create (
            language = self.language,
            local_language_id = self.language.pk,
            name = 'tesht lankwage'
        )
        self.language_name.save()


class HasRegion(HasLanguage):

    @classmethod
    def setup_region_data(self):

        self.setup_language_data()

        self.region = Region.objects.create (
            name = 'test region'
        )
        self.region.save()

        self.region_name = RegionName.objects.create (
            region = self.region,
            language = self.language,
            name = 'tesht reejun'
        )
        self.region_name.save()


class HasGeneration(HasRegion, HasLanguage):

    @classmethod
    def setup_generation_data(self):

        self.setup_language_data()
        self.setup_region_data()

        self.generation = Generation.objects.create (
            region = self.region,
            name = 'test generation'
        )
        self.generation.save()

        self.generation_name = GenerationName.objects.create (
            generation = self.generation,
            language = self.language,
            name = 'tesht janerashun'
        )
        self.generation_name.save()


class HasVersionGroup(HasGeneration):

    @classmethod
    def setup_version_group_data(self):

        self.setup_generation_data()

        self.version_group = VersionGroup.objects.create (
            name = 'test version group',
            generation = self.generation,
            order = 1
        )
        self.version_group.save()


class HasVersion(HasVersionGroup, HasLanguage):

    @classmethod
    def setup_version_data(self):

        self.setup_version_group_data()
        self.setup_language_data()

        self.version = Version.objects.create (
            name = 'test version',
            version_group = self.version_group,
        )
        self.version.save()

        self.version_name = VersionName.objects.create (
            version = self.version,
            language = self.language,
            name = 'tesht vershun'
        )
        self.version_name.save()


class HasAbility(HasGeneration, HasVersionGroup):

    @classmethod
    def setup_ability_data(self):

        self.setup_generation_data()
        self.setup_version_group_data()

        self.ability = Ability.objects.create (
            name = 'test ability',
            generation = self.generation,
            is_main_series = False
        )
        self.ability.save()

        self.ability_name = AbilityName.objects.create (
            ability = self.ability,
            language = self.language,
            name = 'tesht uhbility'
        )
        self.ability_name.save()

        self.ability_description = AbilityDescription.objects.create (
            ability = self.ability,
            language = self.language,
            short_effect = 'ability effect',
            effect = 'a longer ability effect'
        )
        self.ability_description.save()

        self.ability_flavor_text = AbilityFlavorText.objects.create (
            ability = self.ability,
            version_group = self.version_group,
            language = self.language,
            flavor_text = 'mmmmmm. ability.'
        )
        self.ability_flavor_text.save()


class HasItemPocket(HasLanguage):

    @classmethod
    def setup_item_pocket_data(self):

        self.setup_language_data()

        self.item_pocket = ItemPocket.objects.create (
            name = 'test item pocket',
        )
        self.item_pocket.save()

        self.item_pocket_name = ItemPocketName.objects.create (
            item_pocket = self.item_pocket,
            name = 'test item pocket',
            language = self.language
        )
        self.item_pocket_name.save()


# class HasItem():

#     @classmethod
#     def setup_item_data(self):

#         self.item = Item.objects.create (
#             name = 'test item',
#             item_category = ItemCategory.objects.get(pk = int(info[2])),
#             cost = int(info[3]),
#             fling_power = int(info[4]) if info[4] != '' else None,
#             item_fling_effect = ItemFlingEffect.objects.get(pk = int(info[5])) if info[5] != '' else None
#         )
#         self.item.save()




""" 
Tests
"""

class LanguageTests(HasLanguage, APITestCase):

    def test_language_api(self):

        self.setup_language_data()

        response = self.client.get('/api/v2/language/{}/'.format(self.language.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], self.language.pk)
        self.assertEqual(response.data['iso639'], self.language.iso639)
        self.assertEqual(response.data['iso3166'], self.language.iso3166)
        self.assertEqual(response.data['name'], self.language.name)
        self.assertEqual(response.data['official'], self.language.official)
        #name params
        self.assertEqual(response.data['names'][0]['name'], self.language_name.name)



class RegionTests(HasRegion, APITestCase):

    def test_region_api(self):

        self.setup_region_data()

        response = self.client.get('/api/v2/region/{}/'.format(self.region.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # base params
        self.assertEqual(response.data['id'], self.region.pk)
        self.assertEqual(response.data['name'], self.region.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], self.region_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], self.language.name)



class GenerationTests(HasGeneration, APITestCase):

    def test_generation_api(self):

        self.setup_generation_data()

        response = self.client.get('/api/v2/generation/{}/'.format(self.generation.pk))

        # base params
        self.assertEqual(response.data['id'], self.generation.pk)
        self.assertEqual(response.data['name'], self.generation.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], self.generation_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], self.language.name)
        # region params
        self.assertEqual(response.data['region']['name'], self.region.name)



class VersionTests(HasVersion, APITestCase):

    def test_version_api(self):

        self.setup_version_data()

        response = self.client.get('/api/v2/version/{}/'.format(self.version.pk))

        # base params
        self.assertEqual(response.data['id'], self.version.pk)
        self.assertEqual(response.data['name'], self.version.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], self.version_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], self.language.name)
        # version group params
        self.assertEqual(response.data['version_group']['name'], self.version.version_group.name)



# class StatTests(HasAbility, APITestCase):

#     def test_stat_api(self):

#         self.setup_ability_data()


class AbilityTests(HasAbility, APITestCase):

    def test_ability_api(self):

        self.setup_ability_data()

        response = self.client.get('/api/v2/ability/{}/'.format(self.ability.pk))
        
        # base params
        self.assertEqual(response.data['id'], self.ability.pk)
        self.assertEqual(response.data['name'], self.ability.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], self.ability_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], self.language.name)
        # description params
        self.assertEqual(response.data['descriptions'][0]['effect'], self.ability_description.effect)
        self.assertEqual(response.data['descriptions'][0]['short_effect'], self.ability_description.short_effect)
        self.assertEqual(response.data['descriptions'][0]['language']['name'], self.language.name)
        # flavor text params
        self.assertEqual(response.data['flavor_text_entries'][0]['text'], self.ability_flavor_text.flavor_text)
        self.assertEqual(response.data['flavor_text_entries'][0]['version_group']['name'], self.version_group.name)
        self.assertEqual(response.data['flavor_text_entries'][0]['language']['name'], self.language.name)
        # generation params
        self.assertEqual(response.data['generation']['name'], self.generation.name)



class ItemPocketTests(HasItemPocket, APITestCase):

    def test_item_pocket_api(self):

        self.setup_item_pocket_data()

        response = self.client.get('/api/v2/item-pocket/{}/'.format(self.item_pocket.pk))

        # base params
        self.assertEqual(response.data['id'], self.item_pocket.pk)
        self.assertEqual(response.data['name'], self.item_pocket.name)
        # name params
        self.assertEqual(response.data['names'][0]['name'], self.item_pocket_name.name)
        self.assertEqual(response.data['names'][0]['language']['name'], self.language.name)



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
