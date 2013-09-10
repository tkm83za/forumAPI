from tastypie import authorization
from tastypie_mongoengine import resources
from forumAPI import documents

class TopicResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Topic.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete') #TODO: own submission auth
        authorization = authorization.Authorization()
        
class CommentResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Comment.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = authorization.Authorization() #TODO: own-submission authorization, allow admin to put/patch

class UserResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.User.objects.filter(is_admin__ne=True)
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = authorization.Authorization() #TODO: own-submission authorization for get, put, patch, delete any for post
        excludes = ['is_admin', 'password']

class AdminUserResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.User.objects.filter(is_admin=True)
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = authorization.Authorization() #TODO: admin-only authorization
        excludes = ['is_admin', 'password']

