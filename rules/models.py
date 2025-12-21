from django.db import models

ASSET_TYPES = [
    ('companion', 'Companion'),
    ('path', 'Path'),
    ('combat', 'Combat Talent'),
    ('ritual', 'Ritual'),
]

# Create your models here.
class AssetDefinition(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class AssetAbilityDefinition(models.Model):
    asset = models.ForeignKey(AssetDefinition, on_delete=models.CASCADE, related_name='abilities')
    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.asset.name} Ability: {self.name}. {self.description[:30]}..."
    
