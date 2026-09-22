from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("hostname", "name", "model", "status", "serial_number", "updated_at")
    list_filter = ("status", "model")
    search_fields = ("hostname", "name", "username", "email", "serial_number")
