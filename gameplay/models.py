from django.db import models

# Create your models here.
class Story(models.Model):
    """
    A narrative story within a world.

    Represents a cohesive narrative arc or campaign thread, containing events
    and involving multiple characters. Each story belongs to a :model:`worlds.World`
    and has participants linked via :model:`gameplay.StoryParticipant`.
    """
    world = models.ForeignKey("worlds.World", on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    prologue = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField("characters.Character", through="StoryParticipant")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Stories"
        ordering = ["world", "title"]

    

class Event(models.Model):
    """
    A specific event within a story.

    Events record narrative occurrences, optionally tied to a character and/or move,
    providing chronological progression of the story. Each event belongs to a
    :model:`gameplay.Story`.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="events")
    character = models.ForeignKey("characters.Character", 
                                  on_delete=models.SET_NULL, null=True, blank=True,
                                  help_text="Character primarily responsible for this event, if any.")
    move = models.ForeignKey("rules.Move", on_delete=models.SET_NULL, null=True, blank=True,
                                    help_text="Move that was made during the event, if any.")
    

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ["story", "created_at"]
    
    def __str__(self) -> str:
        return f"{self.story}: {self.text[:30]}..."

class StoryParticipant(models.Model):
    """
    A through model linking stories to participating characters.

    Establishes the many-to-many relationship between :model:`gameplay.Story`
    and :model:`characters.Character`, allowing characters to participate in multiple stories.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    participant = models.ForeignKey("characters.Character", on_delete=models.CASCADE, related_name='stories')

    class Meta:
        unique_together = ("story", "participant")