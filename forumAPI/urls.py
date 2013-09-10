from django.conf.urls.defaults import *
from tastypie.api import Api
from forumAPI.api import TopicResource, CommentResource, UserResource, AdminUserResource

v1_api = Api(api_name='v1')
v1_api.register(TopicResource())
v1_api.register(CommentResource())
v1_api.register(UserResource())
v1_api.register(AdminUserResource())



urlpatterns = patterns('',
    # The normal jazz here...
    (r'^api/', include(v1_api.urls)),
)