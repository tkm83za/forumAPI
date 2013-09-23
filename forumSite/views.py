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
from django.http.response import HttpResponse

logger = logging.getLogger(__name__)

def signup(request):
    form = SignupForm()
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid() and form.save():
            return render(request, "registration/registration_complete.html")
    return render(request, "registration/registration_form.html", {"form": form},
                  context_instance=RequestContext(request))

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
    
    new_comments = {}
    class node():
        def __init__(self, value):
            self.value = value
            self.children = []
    
        def add_child(self, obj):
            self.children.append(obj)
           
    nodes = dict((e["id"], node(e)) for e in comments['objects'])
    for e in comments['objects']:
        if e["in_reply_to"]:
            if not nodes.get(e["in_reply_to"], False):
                nodes[e["in_reply_to"]] = node({"is_hidden": True})
            nodes[e["in_reply_to"]].add_child(nodes[e["id"]])
            
    return render(request, 'forum/topic.html', {'topic': topic, 'comments': nodes, 'form': comment_form})
    
@login_required
def newtopic(request):
    user = request.user
    form = None
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid() and form.save():
            return redirect('/topics/')
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
            return redirect('/topic/' + request.POST.get('topic', "-empty-") + "/")
        else:
            message = "Failed ot save comment"
    skeleton = CommentForm(initial={'id': id})
    comment = api_client.get(skeleton)
    comment_form = CommentForm(initial={'comment_body':comment['comment_body'],
                                        'topic': comment['topic'].split("/")[-2]})
    return render(request, 'forum/form.html', {'form': comment_form, 'title': 'Edit Comment'})
    
@login_required
def delete_comment(request, id):
    if request.POST:
        comment_form = CommentForm(initial={'id': id})
        if api_client.delete(comment_form):
            return redirect('/topic/' + request.POST.get('topic', "-empty-") + "/")
        else:
            message = "Failed to delete comment"
            return redirect('/topic/' + request.POST.get('topic', "-empty-") + "/")


@login_required
def hide_comment(request, id):
    if request.POST:
        comment_form = CommentForm(initial={'id': id})
        payload = {'is_hidden': True}
        if api_client.save(comment_form, method='PATCH', payload=payload):
            return redirect('/topic/' + request.POST.get('topic', "-empty-") + "/")
        else:
            message = "Failed ot save comment"
        return redirect('/topic/' + request.POST.get('topic', "-empty-") + "/")

def index(request):
    return render_to_response('forum/index.html', { 'form': SignupForm()},
                              context_instance=RequestContext(request))
