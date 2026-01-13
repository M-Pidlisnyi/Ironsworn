from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .models import Story

# Create your views here.
def home_page(request):
    return render(request, 'gameplay/home_page.html')

class StoriesListView(ListView):
    model = Story
    template_name = "gameplay/stories_list.html"
    context_object_name = "stories_list"

class StoryDetailView(DetailView):
    model = Story

class CreateStoryView(CreateView):
    model = Story
    fields = ["world", "title", "prologue"]
    template_name = "generic_form.html"
    success_url = reverse_lazy("stories-list")

    #TODO: new even form handling, best create django form
