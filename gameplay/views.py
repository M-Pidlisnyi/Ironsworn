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

