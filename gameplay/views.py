from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .models import Story, Event

# Create your views here.
def home_page(request):
    return render(request, 'gameplay/home_page.html')

class StoriesListView(ListView):
    """
    Display all stories across the current user's worlds.

    This view aggregates :model:`gameplay.Story` instances from all worlds
    owned by the authenticated user, allowing them to see all ongoing narratives
    in one place.

    **Template:**
    Renders the :template:`gameplay/stories_list.html` template.

    **Context**

    ``stories_list``
        All :model:`gameplay.Story` objects across the user's worlds.

    ``worlds_list``
        All :model:`worlds.World` objects owned by the current user.
    """
    model = Story
    template_name = "gameplay/stories_list.html"
    context_object_name = "stories_list"

    def get_queryset(self):
        user = self.request.user
        user_worlds = user.world_set.all()#type:ignore
        stories = []
        for world in user_worlds:
            stories += world.story_set.all()
        return stories
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["worlds_list"] = self.request.user.world_set.all()#type: ignore
        return context


class StoryDetailView(DetailView):
    """
    Display a story and allow adding narrative events.

    This view displays the full :model:`gameplay.Story` including all
    :model:`gameplay.Event` instances in chronological order.

    POST requests create new events. The event text is provided via the
    ``text`` form field.

    **Template:**
    Renders the default detail template for :model:`gameplay.Story`.
    """
    model = Story

    def post(self, request, *args, **kwargs):
        event_text = request.POST.get("text", '')

        new_event = Event.objects.create(text=event_text, story=self.get_object())
        return redirect(self.request.path_info)



class CreateStoryView(CreateView):
    """
    Create a new story within a world.

    This view allows a user to create a new :model:`gameplay.Story`,
    selecting a :model:`worlds.World` and providing a title and prologue.

    **Template:**
    Renders the :template:`generic_form.html` template.
    """
    model = Story
    fields = ["world", "title", "prologue"]
    template_name = "generic_form.html"
    success_url = reverse_lazy("gameplay:stories-list")

