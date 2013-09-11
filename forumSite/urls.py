from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # The normal jazz here...
#    (r'^topic/<?P>', views.topic()),
    ('', 'forumSite.views.signup'),
)