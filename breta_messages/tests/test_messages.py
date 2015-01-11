from django.test import TestCase

from accounts.tests.factories import UserFactory
from .factories import MessageFactory


class MessagesTest(TestCase):
    def test_message_create(self):
        subject = 'Test'
        body = 'Body'
        sender = UserFactory()
        msg = MessageFactory(subject=subject, body=body, sender=sender)
        self.assertEqual(msg.subject, subject)
        self.assertEqual(msg.body, body)
        self.assertEqual(msg.sender, sender)

    def test_message_unicode(self):
        subject = 'Test subject'
        msg = MessageFactory(subject=subject)
        self.assertEqual(unicode(msg), subject)

