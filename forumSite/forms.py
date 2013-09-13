import requests
import logging

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models

import api_client

logger = logging.getLogger(__name__)

def _drop_empty_id(my_vals):
    if 'id' in my_vals and not my_vals['id']:
        del my_vals['id']
    return my_vals

class ApiForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput)

    def save(self):
        try:
            res = api_client.save(self)
            res.raise_for_status()
        except (requests.exceptions.HTTPError) as err:
            logger.error(err)
            return False
        return True

class UserForm(ApiForm):
    class Meta:
        api_path = "user/"
    

class SignupForm(UserForm):
    
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

    email = forms.EmailField(required = True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
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

class TopicForm(ApiForm):
    class Meta:
        api_path = "topic/"
        fields = ('name', 'blurb')

    _logger = logging.getLogger(__name__)

    name = forms.CharField(max_length=50, required=True)
    blurb = forms.CharField(max_length=50, required=False)
    id = forms.CharField(widget=forms.HiddenInput, required=False)

    def to_dict(self):
        my_vals = {
                    'name': self.cleaned_data.get('name', None),
                    'blurb': self.cleaned_data.get('blurb', None),
                    'id': self.cleaned_data.get('id', None)
                  }
        return _drop_empty_id(my_vals)
    
class CommentForm(ApiForm):
    class Meta:
        api_path = "comment/"
        fields = ('topic', 'in_reply_to', 'comment_body', 'id')
        exclude = ("is_hidden",)

    _logger = logging.getLogger(__name__)

    topic = forms.CharField(max_length=500, required=True, widget=forms.HiddenInput)
    comment_body = forms.CharField(max_length=50, required=True, widget=forms.Textarea, label="Comment")
    
    in_reply_to = forms.CharField(widget=forms.HiddenInput, required=False)

    def to_dict(self):
        my_vals = {
                    'topic': self.cleaned_data.get('topic', None),
                    'in_reply_to': self.cleaned_data.get('in_reply_to', None),
                    'comment_body': self.cleaned_data.get('comment_body', None),
                    'id': self.cleaned_data.get('id', None)
                  }
        return _drop_empty_id(my_vals)


