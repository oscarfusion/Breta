from django.db import models
from djorm_pgjson.fields import JSONField


class Customer(models.Model):
    user = models.OneToOneField('accounts.User', related_name='stripe_customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_customer_id = models.CharField(max_length=255, null=True)
    extra_data = JSONField()

    def __unicode__(self):
        return u'Customer #{}'.format(self.pk)


class CreditCard(models.Model):
    customer = models.ForeignKey(Customer, related_name='credit_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_card_id = models.CharField(max_length=255, null=True)
    extra_data = JSONField()

    def __unicode__(self):
        return u'Credit Card #{}'.format(self.pk)

    @property
    def card_type(self):
        return self.extra_data.get('brand')

    @property
    def last4(self):
        return self.extra_data.get('last4')

    @property
    def exp_month(self):
        return self.extra_data.get('exp_month')

    @property
    def exp_year(self):
        return self.extra_data.get('exp_year')


class PayoutMethod(models.Model):
    user = models.ForeignKey('accounts.User', related_name='payout_methods')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_recipient_id = models.CharField(max_length=255, null=True)
    extra_data = JSONField()

    name = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'PayoutMethod #{}'.format(self.pk)

    @property
    def bank_name(self):
        return self.extra_data.get('active_account', {}).get('bank_name')

    @property
    def routing_number(self):
        return self.extra_data.get('active_account', {}).get('routing_number')

    @property
    def last4(self):
        return self.extra_data.get('active_account', {}).get('last4')


class Transaction(models.Model):
    ESCROW = 'escrow'
    MILESTONE = 'milestone'
    CREDIT = 'credit'

    TRANSACTION_TYPE_CHOICES = (
        (ESCROW, 'Payment to Escrow'),
        (MILESTONE, 'Payment to Milestone'),
        (CREDIT, 'Credit'),
    )

    credit_card = models.ForeignKey(CreditCard, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_id = models.CharField(max_length=255, null=True)
    extra_data = JSONField()

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES)
    milestone = models.ForeignKey('projects.Milestone', null=True, blank=True)

    def __unicode__(self):
        return u'Transaction #{}'.format(self.pk)

    @property
    def milestone_name(self):
        return self.milestone.name if self.milestone else None

    @property
    def project_name(self):
        return self.milestone.project.name if self.milestone and self.milestone.project else None