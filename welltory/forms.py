from django import forms
from django.forms import ModelForm, Textarea
from django.forms.widgets import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Practitioner, Patient


# USERS, PRACTITIONERS & AUTHENTICATION ====================================================================================
# ======================================================================================================================
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(max_length=80, required=True)
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,)

    password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput,
        strip=False,)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
        help_texts = {
            'username': None,
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(max_length=80, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        help_texts = {
            'username': None,
        }


# form to create/update lawyer details
class PractitionerUpdateForm(forms.ModelForm):
    class Meta:
        model = Practitioner
        fields = ('dateOfBirth',
                  'gender',
                  'national_id',
                  'mobile',
                  'street1',
                  'street2',
                  'city',
                  'country',
                  'image')

        labels = {
            'dateOfBirth': 'Date Of Birth',
            'gender': 'Gender',
            'national_id': 'National ID',
            'mobile': 'Mobile',
            'street1': 'Address (Street)',
            'street2': 'Address (Surburb)',
            'city': 'City',
            'country': 'Country'
        }

        widgets = {'dateOfBirth': DateInput(attrs={'type': 'date'})}


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = (
            'first_name',
            'last_name',
            'mobile',
            'email',
            'street1',
            'street2',
            'city',
            'country',
            'dateOfBirth',
            'national_id',
            'gender',
        )

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'mobile': 'Mobile',
            'email': 'Email Address',
            'address1': 'Address (Street)',
            'address2': 'Address (Surburb)',
            'city': 'City',
            'country': 'Country',
            'dateOfBirth': 'Date of Birth',
            'national_id': 'National ID',
            'gender': 'Gender',
        }

        widgets = {'dateOfBirth': DateInput(attrs={'type': 'date'})}


# form for disabled field inputs on user profile
class ProfileGrayedForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40, disabled=True)
    last_name = forms.CharField(max_length=40, disabled=True)
    email = forms.EmailField(max_length=80, disabled=True)
    username = forms.CharField(max_length=80, disabled=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')