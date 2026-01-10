from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Character(models.Model):
    """
    A player character in an Ironsworn campaign.

    Represents the complete mechanical and narrative state of a character,
    including core stats, resources, experience, bonds progress, and assets.

    All related game data is scoped to a Django :model:`auth.User`.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")#keep Character and all game data user-scoped

    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Character's descrption and/or background")

    # stats
    edge = models.IntegerField(default=0, verbose_name="Stat: Edge")
    heart = models.IntegerField(default=0, verbose_name="Stat: Heart")
    iron = models.IntegerField(default=0, verbose_name="Stat: Iron")
    shadow = models.IntegerField(default=0, verbose_name="Stat: Shadow")
    wits = models.IntegerField(default=0, verbose_name="Stat: Wits")

    #resources
    health = models.IntegerField(default=5, verbose_name="Tracker: Health")
    spirit = models.IntegerField(default=5, verbose_name="Tracker: Spirit")
    supply = models.IntegerField(default=5, verbose_name="Tracker: Supply")
    momentum = models.IntegerField(default=2, verbose_name="Tracker: Momentum")
    momentum_max = models.IntegerField(default=10, verbose_name="Maximal Momentum")
    momentum_reset = models.IntegerField(default=2, verbose_name="Momentum Reset value")
    
    experience = models.IntegerField(default=0, verbose_name="Gained experience points", help_text="Spendable on new assets or asset upgrades")

    @property
    def bonds_progress(self) -> int:
        """ticks, not progress boxes"""
        return self.bonds.count()#type: ignore

    def __str__(self):
        return self.name
    
class Vow(models.Model):
    """
    A sworn vow undertaken by a character making the Swear an Iron Vow move.

    Vows are long-term narrative commitments with a defined difficulty
    rank and a progress track measured in ticks.

    Each vow belongs to exactly one :model:`characters.Character`.
    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='vows')
    description = models.TextField()
    progress = models.IntegerField(default=0, help_text="ticks, not progress boxes")
    difficulty = models.IntegerField(choices=settings.DIFFICULTY_LEVELS)

    def __str__(self):
        return f"{self.character.name} vowed to {self.description[:20]}..."
    
class Bond(models.Model):
    """
    A narrative bond between a character and a person or community, created by making a Forge a Bond move.

    Bonds do not have individual progress tracks. All bonds contribute to the
    shared bonds progress of a :model:`characters.Character`.
    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='bonds')
    description = models.TextField()

    def __str__(self):
        return f"{self.character.name} is bound to {self.description[:20]}..."

class MinorQuest(models.Model):
    """
        Minor Quest is continous activity with a set goal and undetermined outcome.
        This model isused to measure the pace and determine the outcome of a goal or challenge in specific situations.

        By default the model includes ``Journey`` and ``Fight`` but is extendable.
        
        Each :model:`characters.MinorQuest` object belongs to  :model:`characters.Character`.

        **Notice regarding the Ironsworn rules:**
        
        In the Ironsworn rulebook there is no gameplay difference between the vow, fight, journey or bonds progress track.
        They are split here for easier management(e.g. grouping minor quest and separating vows) 
        and because they have a clear narrative difference*
    """
    QUEST_TYPE = [
        ('journey', "Journey"),
        ('fight',   "Fight")
    ]
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="quests")
    type = models.CharField(choices=QUEST_TYPE, max_length=10)
    difficulty = models.IntegerField(choices=settings.DIFFICULTY_LEVELS)

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    progress = models.IntegerField(default=0, help_text="ticks, not progress boxes")

    modified_at = models.DateTimeField(auto_now=True, help_text="used to display last modifed quet on charsheet")

    class Meta:
        ordering = ["modified_at"]

    def __str__(self) -> str:
        return f"{self.type.capitalize()}: {self.title}"



class Debility(models.Model):
    """
    A debility affecting a character.

    Debilities are narrative conditions that impose long-term consequences.
    They reduce maximum momentum and influence fiction, but do not have
    per-type mechanical effects beyond their presence.

    Debilities belong to a :model:`characters.Character`.
    """
     
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
    
    class Meta:
        verbose_name_plural = "Debilities"
    

class CharacterAsset(models.Model):
    """
    An asset owned by a character.

    This model links a :model:`characters.Character` to a
    :model:`rules.AssetDefinition` and serves as the root container
    for character-specific asset state such as abilities and components.

    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='assets')
    definition = models.ForeignKey('rules.AssetDefinition', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('character', 'definition')

    def __str__(self):
        return f"{self.character.name}'s {self.definition.title}"

class CharacterAssetAbility(models.Model):
    """
    A character-specific instance of an asset ability.

    Each ability references an :model:`rules.AssetAbilityDefinition`
    and tracks whether that ability is currently active for the character.
    """
    character_asset = models.ForeignKey(CharacterAsset, on_delete=models.CASCADE, related_name='abilities')
    definition = models.ForeignKey('rules.AssetAbilityDefinition', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, 
        verbose_name="Is this ability active for this character", 
        help_text="Only active abilities provide narrative and mechanical effects")
   
    class Meta:
        unique_together = ('character_asset', 'definition')
    
    def __str__(self):
        return self.definition.title

class CharacterAssetComponent(models.Model):
    """
    A character-specific asset component.

    Components reference an :model:`rules.AssetComponentDefinition` and
    store per-asset custom state such as names, counters, tracks, or other
    narrative properties.
    
    """
    character_asset = models.ForeignKey(CharacterAsset, on_delete=models.CASCADE, related_name='components')
    definition = models.ForeignKey('rules.AssetComponentDefinition', on_delete=models.CASCADE)
    value = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('character_asset', 'definition')

    def __str__(self):
        return f"{self.definition.title} {self.value}"