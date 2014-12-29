import json

from django.utils.text import slugify
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.factories import UserFactory
from ...tests.factories import ProjectFactory
from ...models import Project


def project_from_json(data):
    return json.loads(data)['project']


def projects_count(data):
    return int(json.loads(data)['meta']['count'])


class ProjectApiTestCase(APITestCase):

    def fake_data(self, project_type=Project.WEBSITE, name='Test project',
                  idea='Test idea', description='Projects description', price_range=Project.ONE_TO_FIVE):
        return {
            'project_type': project_type,
            'name': name,
            'idea': idea,
            'description': description,
            'price_range': price_range
        }

    def test_should_require_auth_for_get_list(self):
        ProjectFactory()
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_require_auth_for_get_object(self):
        user = ProjectFactory()
        url = reverse('project-detail', args=(user.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_create_without_login(self):
        data = self.fake_data()
        url = reverse('project-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_allow_create_with_login(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        data = self.fake_data()
        url = reverse('project-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = project_from_json(response.content)
        self.assertEqual(project['name'], data['name'])
        self.assertEqual(project['project_type'], Project.WEBSITE)
        self.assertEqual(project['idea'], data['idea'])
        self.assertEqual(project['description'], data['description'])
        self.assertEqual(project['price_range'], Project.ONE_TO_FIVE)
        self.assertEqual(project['slug'], slugify(unicode(data['name'])))

    def test_should_have_access_only_to_own_objects(self):
        url = reverse('project-list')
        user = UserFactory()
        self.client.force_authenticate(user=user)
        data = self.fake_data(name='Project1')
        self.client.post(url, data)
        data = self.fake_data(name='Project2')
        self.client.post(url, data)
        self.client.logout()
        user2 = UserFactory()
        self.client.force_authenticate(user=user2)
        data = self.fake_data(name='Project3')
        self.client.post(url, data)
        response = self.client.get(url)
        count = projects_count(response.content)
        self.assertEqual(count, 1)
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        count = projects_count(response.content)
        self.assertEqual(count, 2)
