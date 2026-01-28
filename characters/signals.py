from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CharacterAssetAbility, CharacterAssetComponent, CharacterAsset

@receiver(post_save, sender=CharacterAsset)
def populate_character_assets(sender, instance, created, **kwargs):
    """
    Automatically instantiate asset abilities and components when a character acquires an asset.

    When a new :model:`characters.CharacterAsset` is created, this signal:
    1. Retrieves all ability definitions from the asset's definition
    2. Creates :model:`characters.CharacterAssetAbility` instances for each ability,
       with is_active field matching the ability definition's initially_active field
    3. Retrieves all component definitions from the asset's definition
    4. Creates :model:`characters.CharacterAssetComponent` instances for each component

    This ensures complete asset initialization without requiring manual creation of
    related ability and component instances.
    """
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