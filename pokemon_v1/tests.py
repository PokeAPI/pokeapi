from __future__ import unicode_literals
from django.test import TestCase

class HeaderTest(TestCase):

  def test_pokemon(self):

    response = self.client.get(
      '/api/v1/pokemon/1/',
      HTTP_ORIGIN="http://anpeterse.me")
    
    print response.request
    print response.status_code
    print response
    print "checking for Access-Control-Allow-Origin header...";

    self.assertEqual(response['Access-Control-Allow-Origin'], '*')