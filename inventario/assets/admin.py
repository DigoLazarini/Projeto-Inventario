from django.contrib import admin

from .models import Asset, HostingService, OfficeLicense


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("hostname", "name", "model", "status", "serial_number", "updated_at")
    list_filter = ("status", "model")
    search_fields = ("hostname", "name", "username", "email", "serial_number")


@admin.register(HostingService)
class HostingServiceAdmin(admin.ModelAdmin):
    list_display = ("domain", "provider", "renewal_date", "billing_cycle", "cost")
    list_filter = ("provider", "billing_cycle")
    search_fields = ("domain", "site", "provider", "notes")


@admin.register(OfficeLicense)
class OfficeLicenseAdmin(admin.ModelAdmin):
    list_display = ("version", "key", "company", "user")
    search_fields = ("version", "key", "company", "user")
