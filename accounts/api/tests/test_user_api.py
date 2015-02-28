import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.factories import UserFactory, DeveloperFactory
from accounts.models import User, Developer, Website


class UserApiTestCase(APITestCase):
    def test_should_require_auth_for_get_list(self):
        UserFactory()
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_require_auth_for_get_object(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_object_without_auth_and_set_password(self):
        url = reverse('user-list')
        data = {
            'first_name': 'John',
            'last_name': 'Galt',
            'email': 'johngalt@example.com',
            'phone': '123456789',
            'password': '12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email='johngalt@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Galt')
        self.assertEqual(user.email, 'johngalt@example.com')
        self.assertEqual(user.phone, '123456789')
        self.assertTrue(user.check_password('12345'))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_should_not_allow_update_without_auth(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        data = {
            'first_name': 'John',
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_update_another_profile(self):
        user = UserFactory()
        auth_user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        data = {
            'first_name': 'John',
        }
        self.client.force_authenticate(user=auth_user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_allow_update_own_profile(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        data = {
            'first_name': 'New Name',
        }
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.first_name, 'New Name')

    def _test_should_not_allow_get_another_profile(self):
        user = UserFactory()
        auth_user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        self.client.force_authenticate(user=auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_allow_get_own_profile(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_now_allow_delete_own_profile(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


def get_data_from_resp(type, data):
    return json.loads(data)[type]


class DeveloperAPITestCase(APITestCase):
    def fake_developer_data(self, user=None, dev_type=Developer.DEVELOPER, title='Test title', bio='Test bio', skills='{"js", "py"}', availability=Developer.AVAILABLE_NOW):
        if user is None:
            user = UserFactory()
        return {
            'user': user.pk,
            'type': dev_type,
            'title': title,
            'bio': bio,
            'skills': skills,
            'availability': availability,
            'project_preferences': ['lorem', 'ipsum_dolor'],
        }

    def fake_website_data(self, developer=None, ws_type=Website.WEBSITE, url='http://test.com'):
        if developer is None:
            developer = DeveloperFactory()
        return {
            'developer': developer.pk,
            'type': ws_type,
            'url': url
        }

    def test_should_require_auth_for_get_list(self):
        DeveloperFactory()
        url = reverse('developer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_require_auth_for_get_object(self):
        dev = DeveloperFactory()
        url = reverse('developer-list', args=(dev.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _test_should_allow_create_developer_object(self):
        url = reverse('developer-list')
        user = UserFactory()
        user.save()
        data = self.fake_developer_data(user=user)
        resp = self.client.post(url, data)
        resp_data = get_data_from_resp('developer', resp.content)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data['type'], data['type'])
        self.assertEqual(resp_data['title'], data['title'])
        self.assertEqual(resp_data['bio'], data['bio'])
        self.assertEqual(resp_data['availability'], data['availability'])

    def test_should_allow_create_website_object(self):
        developer = DeveloperFactory()
        developer.save()
        url = reverse('website-list')
        data = self.fake_website_data(developer=developer)
        resp = self.client.post(url, data)
        resp_data = get_data_from_resp('website', resp.content)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data['type'], data['type'])
        self.assertEqual(resp_data['url'], data['url'])
        self.assertEqual(resp_data['developer'], developer.id)
