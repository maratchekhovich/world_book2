from django import forms
from datetime import date
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Book

class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','genre','author','language','isbn','summary',]
        widgets = {}
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class AuthorForm(forms.Form):
    first_name = forms.CharField(label="Имя автра")
    last_name= forms.CharField(label="Фамилия автора")
    date_of_birth = forms.DateField(label="Дата рождения", initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Дата смерти", initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
