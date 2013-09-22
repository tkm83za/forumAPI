from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    (r'^topic/<?P>', views.topic()),
    ('^register/?$', 'forumSite.views.signup'),
    ('^topics/$', 'forumSite.views.topics'),
    ('^submit/topic/?$', 'forumSite.views.newtopic'),
    ('topic/(?P<id>[a-zA-Z0-9]{1,})/$', 'forumSite.views.topic'),
    ('comment/(?P<id>[a-zA-Z0-9]{1,})/delete/$', 'forumSite.views.delete_comment'),
    ('comment/(?P<id>[a-zA-Z0-9]{1,})/hide/$', 'forumSite.views.hide_comment'),
    ('comment/(?P<id>[a-zA-Z0-9]{1,})/$', 'forumSite.views.edit_comment'),
    ('^topic/?$', 'forumSite.views.topic'),
#     ('^addcomment', 'forumSite.views.addcomment'),
    ('^$', 'forumSite.views.index')
)