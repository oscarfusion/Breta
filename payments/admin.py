from django.contrib import admin
from .models import Customer, CreditCard, PayoutMethod


class CreditCardInline(admin.TabularInline):
    model = CreditCard


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = (CreditCardInline, )


class PayoutMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(PayoutMethod, PayoutMethodAdmin)
