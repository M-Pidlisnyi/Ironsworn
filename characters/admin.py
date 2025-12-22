from django.contrib import admin

from .models import Character, Bond, Vow, CharacterAsset


class BondInline(admin.TabularInline):
	model = Bond
	extra = 0


class VowInline(admin.TabularInline):
	model = Vow
	extra = 0

class AssetInline(admin.TabularInline):
	model = CharacterAsset
	extra = 0

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
	list_display = ("name", "user")
	search_fields = ("name", "user__username")
	inlines = [BondInline, VowInline, AssetInline]
