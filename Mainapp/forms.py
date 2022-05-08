# from attr import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ('username', 'first_name')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name',)