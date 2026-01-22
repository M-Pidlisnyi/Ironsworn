from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .models import Story, Event

# Create your views here.
def home_page(request):
    return render(request, 'gameplay/home_page.html')

class StoriesListView(ListView):
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
    model = Story

    def post(self, request, *args, **kwargs):
        event_text = request.POST.get("text", '')

        new_event = Event.objects.create(text=event_text, story=self.get_object())
        return redirect(self.request.path_info)



class CreateStoryView(CreateView):
    model = Story
    fields = ["world", "title", "prologue"]
    template_name = "generic_form.html"
    success_url = reverse_lazy("gameplay:stories-list")

