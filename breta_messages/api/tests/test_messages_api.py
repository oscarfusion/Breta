import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.tests.factories import UserFactory
from ...tests.factories import MessageFactory, MessageRecipientFactory
from ...models import Message, MessageRecipient


def get_message_from_data(data):
    return json.loads(data)['message']


def get_records_count(data):
    return int(json.loads(data)['meta']['count'])


class MessageAPITest(APITestCase):
    def fake_data(self, sender, subject="Subject", body="Body"):
        return {
            'sender': sender,
            'subject': subject,
            'body': body
        }

    def test_should_require_auth_for_get_list(self):
        MessageFactory()
        url = reverse('message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_require_auth_for_get_object(self):
        msg = MessageFactory()
        url = reverse('message-detail', args=(msg.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_create_without_login(self):
        sender = UserFactory()
        data = self.fake_data(sender)
        url = reverse('message-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_allow_create_with_login(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        data = self.fake_data(sender=user.id)
        url = reverse('message-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_have_access_only_to_own_messages(self):
        url = reverse('message-list')
        user = UserFactory()
        user2 = UserFactory()
        MessageFactory(sender=user)
        MessageFactory(sender=user)
        MessageFactory(sender=user2)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        count = get_records_count(response.content)
        self.assertEqual(count, 2)
        self.client.logout()
        self.client.force_authenticate(user=user2)
        response = self.client.get(url)
        count = get_records_count(response.content)
        self.assertEqual(Message.objects.all().count(), 3)
        self.assertEqual(count, 1)
        self.client.logout()
        self.assertEqual(Message.objects.all().count(), 3)

    def test_should_not_allow_get_not_own_messages(self):
        user = UserFactory()
        auth_user = UserFactory()
        msg = MessageFactory(sender=user)
        self.client.force_authenticate(user=auth_user)
        url = reverse('message-detail', args=(msg.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_allow_get_own_messages(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        msg1 = MessageFactory(sender=user)
        msg2 = MessageFactory(sender=user)
        url1 = reverse('message-detail', args=(msg1.id,))
        url2 = reverse('message-detail', args=(msg2.id,))
        response = self.client.get(url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_create_message_with_normal_data(self):
        user = UserFactory()
        subject = 'Test subject'
        body = 'Test body'
        expected_msg = MessageFactory(sender=user, subject=subject, body=body)
        url = reverse('message-detail', args=(expected_msg.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        real_msg = get_message_from_data(response.content)
        self.assertEqual(expected_msg.pk, real_msg['id'])
        self.assertEqual(expected_msg.subject, real_msg['subject'])
        self.assertEqual(expected_msg.body, real_msg['body'])


class TestMessageWithRecipients(APITestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.user3 = UserFactory()

        # Message from user1 to user2, user3:
        self.message1 = MessageFactory(sender=self.user1)
        self.message_recipient1 = MessageRecipientFactory(message=self.message1, recipient=self.user2)
        self.message_recipient2 = MessageRecipientFactory(message=self.message1, recipient=self.user3)

        # Message from user2 to user1, user3:
        self.message2 = MessageFactory(sender=self.user2)
        self.message_recipient3 = MessageRecipientFactory(message=self.message2, recipient=self.user1)
        self.message_recipient4 = MessageRecipientFactory(message=self.message2, recipient=self.user3)

        # Message from user3 to user1:
        self.message3 = MessageFactory(sender=self.user3)
        self.message_recipient5 = MessageRecipientFactory(message=self.message3, recipient=self.user1)

    def test_user_1_messages(self):
        user_1_msgs = MessageRecipient.objects.filter(recipient=self.user1)
        self.assertEqual(list(user_1_msgs), [self.message_recipient3, self.message_recipient5])

    def test_user_2_messages(self):
        user_2_msgs = MessageRecipient.objects.filter(recipient=self.user2)
        self.assertEqual(list(user_2_msgs), [self.message_recipient1])

    def test_user_3_messages(self):
        user_3_msgs = MessageRecipient.objects.filter(recipient=self.user3)
        self.assertEqual(list(user_3_msgs), [self.message_recipient2, self.message_recipient4])


class TestMessageWithRecipientsAPI(APITestCase):
    def setUp(self):
        self.sender = UserFactory()
        self.recipient1 = UserFactory()
        self.recipient2 = UserFactory()
        self.msg = MessageFactory(sender=self.sender)
        self.fake_data = {
            'message': self.msg.id,
            'recipient': self.recipient1.id
        }

    def test_should_require_auth_for_get_list(self):
        MessageRecipientFactory()
        url = reverse('messagerecipient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(2+2, 4)

    def test_should_require_auth_for_get_object(self):
        msg = MessageRecipientFactory()
        url = reverse('messagerecipient-detail', args=(msg.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_create_without_login(self):
        url = reverse('messagerecipient-list')
        response = self.client.post(url, self.fake_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_allow_create_with_login(self):
        url = reverse('messagerecipient-list')
        self.client.force_authenticate(user=self.recipient1)
        response = self.client.post(url, self.fake_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_have_access_only_to_own_objects(self):
        MessageRecipientFactory(message=self.msg, recipient=self.recipient1)
        MessageRecipientFactory(message=self.msg, recipient=self.recipient2)
        url = reverse('messagerecipient-list')
        self.client.force_authenticate(user=self.recipient1)
        response = self.client.get(url)
        count = get_records_count(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 1)
