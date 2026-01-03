from django.db import models



class AssetDefinition(models.Model):
    """
    A rules-level definition of an Ironsworn asset.

    Asset definitions describe reusable assets such as companions, paths,
    combat talents, and rituals. They contain no character-specific state
    and serve as templates for :model:`characters.CharacterAsset`.
    """

    ASSET_TYPES = [
    ('companion', 'Companion'),
    ('path', 'Path'),
    ('combat', 'Combat Talent'),
    ('ritual', 'Ritual'),
    ]
    
    title = models.CharField(max_length=20,
        verbose_name="Asset name",
        help_text="Name of the asset as listed in the Ironsworn Asset Library(Master Set).")
    
    description = models.TextField(
        verbose_name="Asset description",
        help_text="Asset's narrative description. Some assets don't have description. Asset's `title` used in such case"
    )
    type = models.CharField(max_length=20, choices=ASSET_TYPES,
        verbose_name="Asset type",
        help_text="Classification of the asset. Purely narrative")

    def __str__(self):
        return self.title
    
class AssetAbilityDefinition(models.Model):
    """
    A rules-level definition of an asset ability.
    Each ability belongs to a single asset, and each asset should contain exactly 3 abilities(not enforced)

    Asset abilities represent selectable or unlockable features of an asset.
    Each ability may be initially active or require player choice to enable.

    These definitions are instantiated per character as
    :model:`characters.CharacterAssetAbility`.
    """

    asset = models.ForeignKey(AssetDefinition, on_delete=models.CASCADE, related_name='abilities')
    title = models.CharField(max_length=20, null=True, blank=True,
        verbose_name="Ability name(if any)")
    description = models.TextField(
        help_text="Narrative and mechanical features of the related `AssetDefinition` object if this ability is active")
    initially_active = models.BooleanField(default=False,
        help_text="Whether this ability is aleary active when picking up the asset")

    def __str__(self):
        return f"{self.asset.title} Ability: {self.title}"
    
class AssetComponentDefinition(models.Model):
    """
    A rules-level definition of an asset component.
    Each compontent belogns to a single asset, and assets don't have to own components

    Asset components define custom per-asset fields such as names, tracks,
    counters, or narrative properties. Components are instantiated for
    characters as :model:`characters.CharacterAssetComponent`.
    """

    asset = models.ForeignKey(AssetDefinition, on_delete=models.CASCADE, related_name='components')
    title = models.CharField(max_length=20, verbose_name="Compontent's name: e.g. name of the companion/god/patron")

    def __str__(self):
        return f"{self.asset.title} Component: {self.title}"
    

class Move(models.Model):
    """
    A rules-level definition of an Ironsworn move.

    Moves describe fictional triggers, mechanical resolution, and narrative
    outcomes. A move may require an action roll, progress roll, oracle roll,
    or no roll at all.
    """
    MOVES_CATEGORIES = [
        ('adventure', 'Adventure'),
        ('relationship', 'Relationship'),
        ('combat', 'Combat'),
        ('suffer', 'Suffer'),
        ('quest', 'Quest'),
        ('fate', 'Fate'),
    ]

    ROLL_TYPES = [
        ('action', 'Action Roll'),
        ('progress', 'Progress Roll'),
        ('oracle', 'Oracle Roll'),
        ('none', 'No Roll'),
    ]

    title = models.CharField(max_length=50, unique=True, 
        verbose_name="Move name",
        help_text="Move name used in Ironsworn Rules Reference")
    category = models.CharField(max_length=20, choices=MOVES_CATEGORIES, 
        verbose_name="Move category",                        
        help_text="Category of the move. Purely narrative.")

    trigger_text = models.TextField(
        verbose_name="Move trigger",
        help_text="Narrative event that triggers the move. Also, mechanical conditions and actions need to make the move")
    
    outcome_text = models.TextField(
        verbose_name="Move outcome",
        help_text="Usually the outcome of the move on strong/weak hit or miss. Sometimes narrative outcome")
    
    roll_type = models.CharField(max_length=20, choices=ROLL_TYPES, 
        help_text="Roll required to make the move. Some moves require oracle roll after action roll. The move's role type is `action` in such case")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["category", "title"]