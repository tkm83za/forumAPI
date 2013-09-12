import requests
import logging

from django import forms
from django.forms.fields import *
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models

import api_client



class UserForm(forms.Form):
    class Meta:
        api_path = "user/"
        
class SignupForm(UserForm):
    logger = logging.getLogger(__name__)
    class Meta(UserForm.Meta):
        fields = ('email', 'first_name')
    def to_dict(self):
        my_vals = {
                    'email': self.cleaned_data.get('email', ''),
                    'first_name': self.cleaned_data.get('first_name', ''),
                    'last_name': self.cleaned_data.get('last_name', None),
                    'password': self.cleaned_data.get('password', None),
                    'id': self.cleaned_data.get('id', None)
                  }
        if not my_vals['password']:
            del my_vals['password']
        if not my_vals['id']:
            del my_vals['id']
        return my_vals

    email = EmailField(required = True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Password (again)"))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data    
         
    def save(self):
        try:
            res = api_client.save(self)
            res.raise_for_status()
        except (requests.exceptions.HTTPError) as err:
            #logger.error(err)
            return False
        return True