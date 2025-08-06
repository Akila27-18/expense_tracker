from django import forms
from .models import Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date", "notes"]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
