# forms.py

from django import forms
from .models import User, Movie, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', ]


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'mobile', 'address1', 'address2', 'postcode', 'state', 'area', 'education', 'country',
                  'region']
