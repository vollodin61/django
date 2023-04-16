import json
from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:cookie-get'))
        self.assertContains(response, 'Cookie value')


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse('myauth:foo-bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['content-type'], 'application/json'
        )
        expetced_date = {'spam': 'eggs', 'foo': 'bar'}
        # received_data = json.loads(response.content)
        # self.assertEqual(received_data, expetced_date)
        self.assertJSONEqual(response.content, expetced_date)
