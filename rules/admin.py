from django.contrib import admin

from .models import AssetDefinition, AssetAbilityDefinition, AssetComponentDefinition
# Register your models here.
class AbilityInline(admin.TabularInline):
    model = AssetAbilityDefinition
    extra = 0

class CustomAbilityInline(admin.TabularInline):
    model = AssetComponentDefinition
    extra = 0


@admin.register(AssetDefinition)
class AssetDefinitionAdmin(admin.ModelAdmin):
    list_display = ("title", "type")
    search_fields = ("title", "type")
    inlines = [AbilityInline, CustomAbilityInline]