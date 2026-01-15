from django.db import models

# Create your models here.
class Story(models.Model):
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

class Event(models.Model):
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
    

class StoryParticipant(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    participant = models.ForeignKey("characters.Character", on_delete=models.CASCADE, related_name='stories')

    class Meta:
        unique_together = ("story", "participant")