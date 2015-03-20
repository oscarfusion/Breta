from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djorm_pgjson.fields import JSONField

from . import utils


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
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            self.customer.credit_cards.update(is_active=False)
            self.is_active = True
        super(CreditCard, self).save(*args, **kwargs)

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
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            self.user.payout_methods.update(is_active=False)
            self.is_active = True
        super(PayoutMethod, self).save(*args, **kwargs)

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
    PAYOUT = 'payout'
    REFERRAL_PAYMENT = 'referral-payment'

    TRANSACTION_TYPE_CHOICES = (
        (ESCROW, 'Payment to Escrow'),
        (MILESTONE, 'Payment to Milestone'),
        (CREDIT, 'Credit'),
        (PAYOUT, 'Payout'),
        (REFERRAL_PAYMENT, 'Referral payment'),
    )

    payout_method = models.ForeignKey(PayoutMethod, related_name='transactions', blank=True, null=True)
    credit_card = models.ForeignKey(CreditCard, related_name='transactions', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_id = models.CharField(max_length=255, null=True, blank=True)
    extra_data = JSONField()
    payer = models.ForeignKey('accounts.User', null=True, blank=True, related_name='payment_transactions')
    receiver = models.ForeignKey('accounts.User', null=True, blank=True, related_name='received_transactions')
    referrer = models.ForeignKey('accounts.User', null=True, blank=True, related_name='referrals_transactions')
    referrer_email = models.EmailField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    referrer_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fee = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES)
    milestone = models.ForeignKey('projects.Milestone', null=True, blank=True)
    displayed_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'Transaction #{}'.format(self.pk)

    @property
    def milestone_name(self):
        return self.milestone.name if self.milestone else None

    @property
    def project_name(self):
        return self.milestone.project.name if self.milestone and self.milestone.project else None

    def get_user(self):
        if self.credit_card_id:
            return self.credit_card.customer.user
        elif self.payout_method:
            return self.payout_method.user
        else:
            return self.milestone.project.user


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, signal, created, **kwargs):
    if created:
        instance.displayed_at = instance.created_at
        if instance.transaction_type in [Transaction.MILESTONE, Transaction.CREDIT, Transaction.PAYOUT]:
            instance.displayed_at = utils.transaction_display_at(instance.created_at)
        instance.save()
