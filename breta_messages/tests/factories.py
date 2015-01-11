import factory as factory
from factory.django import DjangoModelFactory


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = 'breta_messages.Message'

    subject = factory.Sequence(lambda n: 'Subject %d' % n)
    body = factory.Sequence(lambda n: 'Body %d' % n)
    sender = factory.SubFactory('accounts.tests.factories.UserFactory')


class MessageRecipientFactory(DjangoModelFactory):
    class Meta:
        model = 'breta_messages.MessageRecipient'

    recipient = factory.SubFactory('accounts.tests.factories.UserFactory')
    message = factory.SubFactory(MessageFactory)


class MessageWithOneRecipientFactory(MessageFactory):
    membership = factory.RelatedFactory(MessageRecipientFactory, 'message')
