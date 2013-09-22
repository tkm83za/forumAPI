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

from forms import SignupForm, TopicForm, CommentForm
from forumSite import api_client

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
    return render(request, 'registration/registration_form.html', {"form": form})

def topics(request):
    topic = TopicForm()
    topics = api_client.get(topic)
    return render(request, 'forum/topiclist.html', {'topics': topics['objects'], 'meta': topics['meta']})

def topic(request, id=None):
    form = TopicForm(initial={'id':id})
    comment_form = CommentForm(initial={"topic": id})
    if (request.POST):
        comment_form = CommentForm(request.POST)
        comment_form.user = request.user.username
        if comment_form.is_valid():
            if comment_form.save(request=request):
                message = "Comment submitted"
                return redirect('/topic/{}'.format(id))
            else:
                message = "Failed to save comment"
        else:
            pass
    try:
        topic = api_client.get(form)
        comments = api_client.get(form, sub_url="topic/{}/comments".format(id))
    except (Exception) as err:
        message = "Failed to retrieve topic and/or comments"
    
    return render(request, 'forum/topic.html', {'topic': topic, 'comments': comments['objects'], 'form': comment_form})
    
@login_required
def newtopic(request):
    user = request.user
    form = None
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid() and form.save():
            redirect('/')
        elif form.is_valid():
            form.non_field_errors = "Failed to save"
        else:
            form.non_field_errors = 'form is not valid'
    else:
        form = TopicForm()
    return render(request, 'forum/form.html', {"form": form})

@login_required
def edit_comment(request, id):
    if request.POST:
        comment_form = CommentForm(request.POST, initial={'id': id})
        payload = {'comment_body': request.POST['comment_body']}
        if api_client.save(comment_form, method='PATCH', payload=payload):
            redirect('/')
        else:
            message = "Failed ot save comment"
    skeleton = CommentForm(initial={'id': id})
    comment = api_client.get(skeleton)
    comment_form = CommentForm(initial={'comment_body':comment['comment_body']})
    return render(request, 'forum/form.html', {'form': comment_form})
    
@login_required
def delete_comment(request, id):
    pass

@login_required
def hide_comment(request, id):
#    if request.POST:
        comment_form = CommentForm(initial={'id': id})
        payload = {'is_hidden': True}
        if api_client.save(comment_form, method='PATCH', payload=payload):
            redirect('/')
        else:
            message = "Failed ot save comment"
        return redirect('/')

def index(request):
    return render_to_response('forum/index.html', { 'form': SignupForm()},
                              context_instance=RequestContext(request))