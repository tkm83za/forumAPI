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
    id = forms.CharField(widget=forms.HiddenInput, required=False)

    def save(self, request=None):
        try:
            res = api_client.save(self, request=request)
            res.raise_for_status()
        except (requests.exceptions.HTTPError) as err:
            logger.error(err)
            raise err
#            return False
        return True

class UserForm(ApiForm):
    class Meta:
        api_path = "user/"
    

class SignupForm(UserForm):
    
    class Meta(UserForm.Meta):
        api_path = "register/"
        fields = ('email', 'username')
    def to_dict(self, request=None):
        my_vals = {
                    'email': self.cleaned_data.get('email', ''),
                    'username': self.cleaned_data.get('username', ''),
                    'password': self.cleaned_data.get('password', None),
                    'id': self.cleaned_data.get('id', None)
                  }
        if not my_vals['password']:
            del my_vals['password']
        if not my_vals['id']:
            del my_vals['id']
        return my_vals

    email = forms.EmailField(required = True)
    username = forms.CharField(max_length=50)
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
            self.cleaned_data['password'] = self.cleaned_data['password1']
        return self.cleaned_data    

class TopicForm(ApiForm):
    class Meta:
        api_path = "topic/"
        fields = ('name', 'blurb')

    _logger = logging.getLogger(__name__)

    name = forms.CharField(max_length=50, required=True, label="Topic")
    blurb = forms.CharField(max_length=50, required=False, widget=forms.Textarea, label="Summary")
    id = forms.CharField(widget=forms.HiddenInput, required=False)

    def to_dict(self, request=None):
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
    comment_body = forms.CharField(required=True, widget=forms.Textarea, label="Comment")
    
    in_reply_to = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_topic(self):
        data = self.cleaned_data['topic']
        if data:
            return "{}/{}/{}/".format(api_client.API_PATH, 'topic', data)
        else:
            raise forms.ValidationError("No topic specified")
    
    def clean_in_reply_to(self):
        data = self.cleaned_data['in_reply_to']
        if not data:
            return None
        else:
            return data

    def to_dict(self, request=None):
        my_vals = {
                    'topic': self.cleaned_data.get('topic', None),
                    'in_reply_to': self.cleaned_data.get('in_reply_to', None),
                    'comment_body': self.cleaned_data.get('comment_body', None),
                    'author': request.user.username,
                    'id': self.cleaned_data.get('id', None)
                  }
        return _drop_empty_id(my_vals)
