from django.contrib import admin


from .models import World, WorldTruth

class TruthInline(admin.TabularInline):
    model = WorldTruth
    extra = 0

@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    inlines = [TruthInline]

