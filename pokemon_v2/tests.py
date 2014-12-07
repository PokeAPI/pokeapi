from __future__ import unicode_literals
from django.test import TestCase

# Create your tests here.

class HeaderTest(TestCase):

  def test_pokemon(self):

    response = self.client.get(
      '/api/v2/pokemon/1/',
      HTTP_ORIGIN="http://anpeterse.me"
    )
    
    self.assertEqual(response['Access-Control-Allow-Origin'], '*')

