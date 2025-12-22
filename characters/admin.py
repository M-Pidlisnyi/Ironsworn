from django.contrib import admin

from .models import Character, Bond, Vow


class BondInline(admin.TabularInline):
	model = Bond
	extra = 0


class VowInline(admin.TabularInline):
	model = Vow
	extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
	list_display = ("name", "user", "edge", "heart", "iron", "wits")
	search_fields = ("name", "user__username")
	inlines = [BondInline, VowInline]
