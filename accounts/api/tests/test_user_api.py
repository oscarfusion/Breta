from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.factories import UserFactory
from accounts.models import User


class UserApiTestCase(APITestCase):
    def test_should_require_auth_for_get_list(self):
        UserFactory()
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_require_auth_for_get_object(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_should_not_allow_update_without_auth(self):
        user = UserFactory()
        url = reverse('user-detail', args=(user.id, ))
        data = {
            'first_name': 'John',
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_should_not_allow_get_another_profile(self):
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
