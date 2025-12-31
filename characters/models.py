from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_LEVELS = [#list of tuples, not a dict cause order matters
    (1, 'troublesome'),
    (2, 'dangerous'),
    (3, 'formidable'),
    (4, 'extreme'),
    (5, 'epic'),
]

# Create your models here.
class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")#keep Character and all game data user-scoped

    name = models.CharField(max_length=100)
    description = models.TextField()

    # stats
    edge = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    iron = models.IntegerField(default=0)
    shadow = models.IntegerField(default=0)
    wits = models.IntegerField(default=0)

    #resources
    health = models.IntegerField(default=5)
    spirit = models.IntegerField(default=5)
    supply = models.IntegerField(default=5)
    momentum = models.IntegerField(default=2)
    momentum_max = models.IntegerField(default=10)
    momentum_reset = models.IntegerField(default=2)
    
    experience = models.IntegerField(default=0)

    bonds_progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Vow(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='vows')
    description = models.TextField()
    progress = models.IntegerField(default=0)
    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS)

    def __str__(self):
        return f"{self.character.name} vowed to {self.description[:20]}..."
    
class Bond(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='bonds')
    description = models.TextField()

    def __str__(self):
        return f"{self.character.name} is bound to {self.description[:20]}..."




class Debility(models.Model):
    DEBILITIES = [
    ("wounded", "Condition: Wounded"),
    ("shaken", "Condition: Shaken"),
    ("unprepared", "Condition: Unprepared"),
    ("encumbered", "Condition: Encumbered"),

    ("maimed", "Bane: Maimed"),
    ("corrupted", "Bane: Corrupted"),

    ("cursed", "Burden: Cursed"),
    ("tormented", "Burden: Tormented"),
    ]
    DEBILITY_TYPES = [
        ("cond", "Condition"),
        ("bane", "Bane"),
        ("burd", "Burden")
    ]
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='debilities')
    name = models.CharField(max_length=20, choices=DEBILITIES)
    type = models.CharField(max_length=4, choices=DEBILITY_TYPES)

    def __str__(self):
        return f"{self.character.name} is {self.name}"
    

class CharacterAsset(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='assets')
    definition = models.ForeignKey('rules.AssetDefinition', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('character', 'definition')

    def __str__(self):
        return f"{self.character.name}'s {self.definition.title}"

class CharacterAssetAbility(models.Model):
    character_asset = models.ForeignKey(CharacterAsset, on_delete=models.CASCADE, related_name='abilities')
    definition = models.ForeignKey('rules.AssetAbilityDefinition', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
   
    class Meta:
        unique_together = ('character_asset', 'definition')
    
    def __str__(self):
        return self.definition.title

class CharacterAssetComponent(models.Model):
    character_asset = models.ForeignKey(CharacterAsset, on_delete=models.CASCADE, related_name='components')
    definition = models.ForeignKey('rules.AssetComponentDefinition', on_delete=models.CASCADE)
    value = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('character_asset', 'definition')

    def __str__(self):
        return f"{self.definition.title} {self.value}"