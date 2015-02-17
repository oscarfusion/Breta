from django.contrib import admin
from .models import Customer, CreditCard, PayoutMethod, Transaction


class CreditCardInline(admin.TabularInline):
    model = CreditCard


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = (CreditCardInline, )


class PayoutMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('stripe_id', 'amount', 'credit_card', 'transaction_type')
    list_filter = ('transaction_type', )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(PayoutMethod, PayoutMethodAdmin)
admin.site.register(Transaction, TransactionAdmin)
