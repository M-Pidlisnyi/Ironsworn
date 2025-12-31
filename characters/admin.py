from django.contrib import admin

from .models import Character, Bond, Vow, CharacterAsset, CharacterAssetAbility, CharacterAssetComponent, Debility


class BondInline(admin.TabularInline):
	model = Bond
	extra = 0


class VowInline(admin.TabularInline):
	model = Vow
	extra = 0

class AssetInline(admin.TabularInline):
	model = CharacterAsset
	extra = 0

class DebilityInline(admin.TabularInline):
	model = Debility
	extra = 0



@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
	list_display = ("name", "user")
	search_fields = ("name", "user__username")
	inlines = [BondInline, VowInline, AssetInline, DebilityInline]

class CharacterAssetAbilityInline(admin.TabularInline):
    model = CharacterAssetAbility
    extra = 0

class CharacterAssetComponentInline(admin.TabularInline):
    model = CharacterAssetComponent
    extra = 0

@admin.register(CharacterAsset)
class CharacterAssetAdmin(admin.ModelAdmin):
	inlines = [CharacterAssetAbilityInline, CharacterAssetComponentInline]