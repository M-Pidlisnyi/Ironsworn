from django import forms

from .models import World, WorldTruth

class NewWorldForm(forms.ModelForm):
    class Meta:
        model = World
        fields = ["name", "description"]
        label = {
            "name": "World name",
            "description": "Worlds description"
        }

class WorldTruthsForm(forms.Form):
    """
    Form for defining all Ironsworn world truths for a single world.

    Fields are generated dynamically from :model:`WorldTruth.QUESTIONS` to ensure
    the form stays in sync with the canonical list of truth questions.
     
    For each truth question, two fields are generated:
    - ``<key>_answer``
    - ``<key>_quest_starter``
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.questions = [(key, label) for key, label in WorldTruth.QUESTIONS]

        for key, label in WorldTruth.QUESTIONS:
            self.fields[f"{key}_answer"] = forms.CharField(label=label, widget=forms.Textarea(attrs={"class": "form-control"}), required=True)

            self.fields[f"{key}_quest_starter" ] = forms.CharField(label=" ", widget=forms.Textarea(attrs={"class": "form-control", "placeholder":"Quest starter"}), required=False)