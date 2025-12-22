from django.contrib import admin

from .models import AssetDefinition, AssetAbilityDefinition
# Register your models here.
class AbilityInline(admin.TabularInline):
    model = AssetAbilityDefinition
    extra = 0


@admin.register(AssetDefinition)
class AssetDefinitionAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    search_fields = ("name", "type")
    inlines = [AbilityInline]