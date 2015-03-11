from __future__ import unicode_literals
from django.test import TestCase

from pokemon.models import Sprite

from rest_framework import status
from rest_framework.test import APIClient


class HeaderTest(TestCase):

  def test_pokemon(self):

    response = self.client.get(
      '/api/v2/pokemon/1/',
      HTTP_ORIGIN="http://pokemon.com"
    )

    self.assertEqual(response['Access-Control-Allow-Origin'], '*')


class SpriteV2Resource(TestCase):
    """
    All tests for the Sprite V2 resource.
    """

    @classmethod
    def setUpClass(self):
        self.client = APIClient()

    def test_get_sprite(self):
        """
        Get a single sprite.
        """

        sp = Sprite.objects.create(
            name='test_sprite_image',
            image='image_url.jpg'
        )
        sp.save()

        url = '/api/v2/sprites/{}/'.format(sp.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], sp.name)


    def test_get_sprite_not_found(self):
        """
        Get a single sprite that doesn't exist, expects a 404 response
        """


        url = '/api/v2/sprites/{}/'.format(12344556)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_all_sprites(self):
        """
        Try to get all the sprites!
        """

        sp = Sprite.objects.create(
            name='test_sprite_image',
            image='image_url.jpg'
        )
        sp.save()

        sp_2 = Sprite.objects.create(
            name='test_sprite_image_two',
            image='image_url_second.jpg'
        )
        sp_2.save()

        url = '/api/v2/sprites/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
