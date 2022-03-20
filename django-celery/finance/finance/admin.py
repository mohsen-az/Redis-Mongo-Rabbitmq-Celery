from django.contrib import admin

from finance.models import Payment, Gateway


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "amount", "is_paid"]
    list_editable = ["is_paid"]


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    pass
