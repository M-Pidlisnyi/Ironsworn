from django.db import models
from django.contrib.auth.models import User


class World(models.Model):
    """
    A game world or setting for Ironsworn campaigns.

    Serves as the top-level container for stories, truths, and other world-specific
    elements. Each world is scoped to a Django :model:`auth.User`.
    """
    name = models.CharField(max_length=100, default="Ironlands")
    description = models.TextField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}({self.pk})"
    
 
class WorldTruth(models.Model):
    """
    A world truth defining aspects of the game world.

    World truths answer predefined questions about the world's lore, history,
    and setting, providing narrative context. Each truth belongs to a :model:`worlds.World`.
    """
    QUESTIONS = [
        ("old_world", "The Old World"),
        ("iron", "Iron"),
        ("legacies", "Legacies"),
        ("communities", "Communities"),
        ("leaders", "Leaders"),
        ("defense", "Defense"),
        ("religion", "Religion"),
        ("mysticism", "Mysticism"),
        ("firsborns", "The Fisrtborns"),
        ("beasts", "Beasts"),
        ("horrors", "The Horrors"),
    ]

    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="truths")
    question = models.TextField(choices=QUESTIONS, help_text="The predefined question about one of the key aspects of the world")
    answer = models.TextField(help_text="An answer that determines a key aspect of the world")
    quest_starter = models.TextField(null=True, blank=True, help_text="A situation emegrent from the answer that can lead to a quest")

