import datetime
import logging

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.http import Http404
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib import messages

from forms import SignupForm

def signup(request):
    user = request.user
    form = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SignupForm()
    return render(request, 'forum/signup.html', {"form": form})
    