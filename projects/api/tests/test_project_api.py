import json

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.factories import UserFactory

from ...tests.factories import ProjectFactory, MilestoneFactory, TaskFactory
from ...models import Project, Milestone, Task


def data_from_json(type, data):
    return json.loads(data)[type]


def data_count(data):
    return int(json.loads(data)['meta']['count'])


class ProjectApiTestCase(APITestCase):
    def fake_data(self, project_type=Project.WEBSITE, name='Test project',
                  idea='Test idea', description='Projects description', price_range='1000,5000'):
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
        project = data_from_json('project', response.content)
        self.assertEqual(project['name'], data['name'])
        self.assertEqual(project['project_type'], Project.WEBSITE)
        self.assertEqual(project['idea'], data['idea'])
        self.assertEqual(project['description'], data['description'])
        self.assertEqual(project['price_range'], '1000,5000')
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
        count = data_count(response.content)
        self.assertEqual(count, 1)
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        count = data_count(response.content)
        self.assertEqual(count, 2)


class MilestonesAPITestCase(APITestCase):
    def fake_data(self, project=None, name='Test milestone', description='Milestone description',
                  amount=123.45, status=Milestone.STATUS_IN_PROGRESS, paid_status=Milestone.PAID_STATUS_DUE,
                  due_date=timezone.now().date()):
        if project is None:
            project = ProjectFactory()
        return {
            'project': project.id,
            'name': name,
            'description': description,
            'amount': amount,
            'status': status,
            'paid_status': paid_status,
            'due_date': due_date
        }

    def test_should_require_auth_for_get_list(self):
        MilestoneFactory()
        url = reverse('milestone-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_require_auth_for_get_object(self):
        ms = MilestoneFactory()
        url = reverse('milestone-detail', args=(ms.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_create_without_login(self):
        data = self.fake_data()
        url = reverse('milestone-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_allow_create_with_login(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        project = ProjectFactory(user=user)
        project.save()
        data = self.fake_data(project=project)
        url = reverse('milestone-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        milestone = data_from_json('milestone', response.content)
        self.assertEqual(milestone['name'], data['name'])
        self.assertEqual(milestone['description'], data['description'])
        self.assertEqual(milestone['status'], Milestone.STATUS_IN_PROGRESS)
        self.assertEqual(milestone['paid_status'], data['paid_status'])
        self.assertEqual(milestone['amount'], str(data['amount']))
        self.assertEqual(milestone['project'], data['project'])
        url = reverse('activity-list')
        response = self.client.get(url, {'project': project.id})
        count = data_count(response.content)
        self.assertEqual(count, 1)


class TasksAPITestCase(APITestCase):
    def fake_data(self, milestone=None, status=Task.STATUS_DEFAULT, name='Test name',
                  description='Test description', due_date=timezone.now().date()):
        if milestone is None:
            milestone = MilestoneFactory()
        return {
            'milestone': milestone.id,
            'status': status,
            'name': name,
            'description': description,
            'due_date': due_date
        }

    def test_should_require_auth_for_get_list(self):
        TaskFactory()
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_require_auth_for_get_object(self):
        task = TaskFactory()
        url = reverse('task-detail', args=(task.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_create_without_login(self):
        data = self.fake_data()
        url = reverse('task-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_allow_create_with_login(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        proj = ProjectFactory(user=user)
        milestone = MilestoneFactory(project=proj)
        data = self.fake_data(milestone=milestone)
        url = reverse('task-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = data_from_json('task', response.content)
        self.assertEqual(task['name'], data['name'])
        self.assertEqual(task['description'], data['description'])
        self.assertEqual(task['status'], data['status'])
        self.assertEqual(task['milestone'], data['milestone'])
        url = reverse('activity-list')
        response = self.client.get(url, {'project': proj.id})
        count = data_count(response.content)
        self.assertEqual(count, 1)
