from django.db import models

ASSET_TYPES = [
    ('companion', 'Companion'),
    ('path', 'Path'),
    ('combat', 'Combat Talent'),
    ('ritual', 'Ritual'),
]

# Create your models here.
class AssetDefinition(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ASSET_TYPES)

    def __str__(self):
        return self.title
    
class AssetAbilityDefinition(models.Model):
    asset = models.ForeignKey(AssetDefinition, on_delete=models.CASCADE, related_name='abilities')
    title = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    initially_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asset.title} Ability: {self.title}"
    
class AssetComponentDefinition(models.Model):
    asset = models.ForeignKey(AssetDefinition, on_delete=models.CASCADE, related_name='components')
    title = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.asset.title} Component: {self.title}"