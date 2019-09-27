
# official django docs:
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name','last_name', 'email', 'address', 'phone')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields =('first_name', 'last_name', 'email', 'address', 'phone')
        list_editable = ('last_name', 'email', 'address', 'phone')
