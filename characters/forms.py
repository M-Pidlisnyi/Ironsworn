from django import forms
from .models import Character

class CharBaseInfoForm(forms.Form):
    name = forms.CharField(max_length=100, label="Character Name")
    description = forms.CharField(widget=forms.Textarea, label="Character Description")

class CharStatsForm(forms.Form):
    edge = forms.IntegerField(min_value=1, max_value=5, label="Edge")
    heart = forms.IntegerField(min_value=1, max_value=5, label="Heart")
    iron = forms.IntegerField(min_value=1, max_value=5, label="Iron")
    shadow = forms.IntegerField(min_value=1, max_value=5, label="Shadow")
    wits = forms.IntegerField(min_value=1, max_value=5, label="Wits")
    
class CharResoursesForm(forms.Form):
    experice = forms.IntegerField(label="Experience", initial=0, disabled=True )
    health = forms.IntegerField(label="Health", initial=5, disabled=True )
    spirit = forms.IntegerField(label="Spirit", initial=5, disabled=True )
    supply = forms.IntegerField(label="Supply", initial=5, disabled=True )
    momentum = forms.IntegerField(label="Momentum", initial=2, disabled=True )

    momentum_max = forms.IntegerField(initial=10, max_value=10, min_value=0, label="Max Momentum")
    momentum_reset = forms.IntegerField(initial=2, max_value=2, min_value=0, label="Momentum Reset")

class CharBondsForm(forms.Form):
    bond_description_1 = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Bond 1 (Optional)",
        required=False
    )
    bond_description_2 = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Bond 2 (Optional)",
        required=False
    )
    bond_description_3 = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Bond 3 (Optional)",
        required=False
    )
