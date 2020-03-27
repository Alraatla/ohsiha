from django import forms
from .models import Goat

class GoatForm(forms.ModelForm):
    class Meta:
        model = Goat
        fields = ['name', 'age', 'breed']
