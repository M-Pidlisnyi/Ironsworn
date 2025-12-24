import os 
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ironsworn.settings")
django.setup()


from rules import models


companions = models.AssetDefinition.objects.filter(type='companion')
for companion in companions:
    models.CustomAssetAbility.objects.get_or_create(asset=companion, name="Name", value="")
    models.CustomAssetAbility.objects.get_or_create(asset=companion, name="Health", tracker=0)