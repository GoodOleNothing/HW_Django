from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar', 'country', 'password1', 'password2']

