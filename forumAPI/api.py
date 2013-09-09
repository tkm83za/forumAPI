from tastypie import authorization
from tastypie_mongoengine import resources
from forumAPI import documents

class TopicResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Topic.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()