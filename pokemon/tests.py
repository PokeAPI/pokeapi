from __future__ import unicode_literals
from django.test import TestCase


class HeaderTest(TestCase):

    def test_pokemon(self):

        response = self.client.get(
          '/api/v1/pokemon/1/',
          HTTP_ORIGIN="http://pokemon.com"
        )

        self.assertEqual(response['Access-Control-Allow-Origin'], '*')
