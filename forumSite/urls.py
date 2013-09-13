from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # The normal jazz here...
#    (r'^topic/<?P>', views.topic()),
    ('^register/?$', 'forumSite.views.signup'),
#    ('^topics', 'forumSite.views.topics'),
    ('^submit/topic/?$', 'forumSite.views.topic'),
    ('^topic/?$', 'forumSite.views.topic'),
#     ('^addcomment', 'forumSite.views.addcomment'),
    ('^$', 'forumSite.views.index')
)