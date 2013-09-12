from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from tastypie.api import Api

from forumSite import urls as site_urls
from forumAPI.api import TopicResource, CommentResource, UserResource, AdminUserResource
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

v1_api = Api(api_name='v1')
v1_api.register(TopicResource())
v1_api.register(CommentResource())
v1_api.register(UserResource())
v1_api.register(AdminUserResource())



urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    ('^admin/', include(admin.site.urls)),
    (r'^static/', 'django.views.static.serve', {'document_root' : 'forumAPI/static', 'show_indexes' : True}),
    ('', include(site_urls)),
)

urlpatterns = staticfiles_urlpatterns() + urlpatterns