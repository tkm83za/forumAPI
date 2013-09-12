import datetime
import logging

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404,\
    render_to_response
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.http import Http404
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib import messages

from forms import SignupForm

logger = logging.getLogger(__name__)

def signup(request):
    user = request.user
    form = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid() and form.save():
            redirect('/welcome')
        elif form.is_valid():
            form.non_field_errors = "Failed to save"
        else:
            form.non_field_errors = 'form is not valid'
    else:
        form = SignupForm()
    return render(request, 'forum/signup.html', {"form": form})


def index(request):
    return render_to_response('forum/index.html', { 'form': SignupForm()},
                              context_instance=RequestContext(request))