from __future__ import unicode_literals

from json import dumps
from random import randint

from django.test import override_settings, Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from measurement.measures import Weight, Volume, Distance

from .models import Product


@override_settings(ROOT_URLCONF='tests.urls')
class ProductAutoCompleteTests(TestCase):
    query_args = {'q': 'fo'}

    def setUp(self):
        self.client = Client()
        self.prod = Product()
        self.prod.name = 'foo'
        self.prod.weight = Weight(kg=randint(1, 10))
        self.prod.volume = Volume(cubic_meter=randint(1, 3))
        self.prod.width = Distance(centimeter=randint(80, 100))
        self.prod.height = Distance(centimeter=randint(80, 100))
        self.prod.depth = Distance(centimeter=randint(60, 80))
        self.prod.save()

    @property
    def url(self):
        return reverse('product-autocomplete')

    def assertAutoComplete(self, body, results):
        """
        Assert the autocomplete result is correct.
        """
        base_result = {
            'pagination': {'more': False}
        }
        base_result.update({'results': results})
        json_result = dumps(base_result)

        self.assertEqual(body, json_result)

    def test_restricted(self):
        """
        The autocomplete is disabled for non-staff users.
        """
        user = User.objects.create_user('foo', 'foo@bar', 'secret')
        logged_in = self.client.login(username='foo', password='secret')

        response = self.client.get(self.url, self.query_args,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertAutoComplete(response.json(), [])

    def test_staff(self):
        """
        The autocomplete is enabled in the admin for staff users.
        """
        user = User.objects.create_superuser('foo', 'foo@bar', 'secret')
        logged_in = self.client.login(username='foo', password='secret')

        response = self.client.get(self.url, self.query_args,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertAutoComplete(response.json(),
            [{'text': self.prod.name, 'id': self.prod.id}])
