from .models import Property, Person
from .models import digits_validator, letters_validator, phone_num_validator
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


from django import forms
from django.forms import ModelForm

"""Defining the form based on the Property model"""

class PropertyForm(ModelForm):
    class Meta:
        model = Property

        fields = ['name', 'description', 'address', 'property_type', 'owner']



class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = ['surname', 'name', 'middle_name', 'phone_number', 'email']

