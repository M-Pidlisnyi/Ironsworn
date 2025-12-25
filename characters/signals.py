from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CharacterAssetAbility, CharacterAssetComponent, CharacterAsset

@receiver(post_save, sender=CharacterAsset)
def populate_character_assets(sender, instance, created, **kwargs):
    print("populate_character_assets signal triggered")
    if not created:
        return
        
    asset_definition = instance.definition

    for ability_def in asset_definition.abilities.all():
        CharacterAssetAbility.objects.create(
            character_asset=instance,
            definition=ability_def,
            is_active=ability_def.initially_active)
        
    for component_def in asset_definition.components.all():
        CharacterAssetComponent.objects.create(
            character_asset=instance,
            definition=component_def)