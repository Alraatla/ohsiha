from django import forms
from .models import Goat
from django.contrib.auth.models import User

class GoatForm(forms.ModelForm):
    class Meta:
        model = Goat
        fields = ['name', 'age', 'breed']
