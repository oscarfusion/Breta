from django.test import TestCase
from django.core.urlresolvers import reverse


class SignUpTestCase(TestCase):
    def test_should_return_page_with_form_on_get(self):
        url = reverse('signup')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)

    def test_should_register_user_on_post(self):
        url = reverse('signup')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@mail.com',
            'phone': '12345',
            'city': 'NY',
            'password': '123456',
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 302)

