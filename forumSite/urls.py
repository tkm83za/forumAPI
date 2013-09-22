from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    (r'^topic/<?P>', views.topic()),
    ('^register/?$', 'forumSite.views.signup'),
    ('^topics/$', 'forumSite.views.topics'),
    ('^submit/topic/?$', 'forumSite.views.newtopic'),
    ('topic/(?P<id>[a-zA-Z0-9]{1,})/$', 'forumSite.views.topic'),
    ('^topic/?$', 'forumSite.views.topic'),
#     ('^addcomment', 'forumSite.views.addcomment'),
    ('^$', 'forumSite.views.index')
)