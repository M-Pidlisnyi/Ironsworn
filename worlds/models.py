from django.db import models
from django.contrib.auth.models import User


class World(models.Model):
    name = models.CharField(max_length=100, default="Ironlands")
    description = models.TextField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}({self.pk})"
    

class WorldTruth(models.Model):
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
    question = models.TextField(choices=QUESTIONS)
    answer = models.TextField()
    quest_starter = models.TextField(null=True, blank=True)

