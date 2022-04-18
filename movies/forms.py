from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Genre, Film


class FilmModelForm(ModelForm):
    def clean_runtime(self):
       data = self.cleaned_data['runtime']
       if data <= 0 or data > 1000:
           raise ValidationError('Neplatná délka filmu')
       return data

    def clean_rate(self):
       data = self.cleaned_data['rate']
       if data < 1 or data > 10:
           raise ValidationError('Neplatné hodnocení: musí být v rozsahu 1-10')
       return data

    class Meta:
        model = Film
        fields = ['title', 'plot', 'poster', 'genres', 'release_date', 'runtime', 'rate']
        labels = {'title': 'Název filmu', 'plot': 'Stručný děj'}