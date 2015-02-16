from django.contrib import admin
from .models import Customer, CreditCard


class CreditCardInline(admin.TabularInline):
    model = CreditCard


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = (CreditCardInline, )


admin.site.register(Customer, CustomerAdmin)
