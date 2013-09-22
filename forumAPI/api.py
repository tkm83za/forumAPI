from tastypie import authorization
import tastypie
from tastypie_mongoengine import resources
from tastypie_mongoengine import fields
import mongoengine

from forumAPI import documents
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from django.core.exceptions import ObjectDoesNotExist

class CommentResource(resources.MongoEngineResource):
    topic =  fields.ReferenceField(to='forumAPI.api.TopicResource', attribute='topic', full=False)
#    creation = fields.()
    
#     def dehydrate_topic(self, bundle):
#             bundle.data['topic'] = documents.Topic.objects(__raw__ = {_id:bundle.data['topic']}).first()
#             return bundle.data['topic']
    class Meta:
        queryset = documents.Comment.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = authorization.Authorization() #TODO: own-submission authorization, allow admin to put/patch
        exclude = ['topic']
        filtering = {"topic": [ "exact", ],
                     "author": ["exact", ],
                      }
    def dehydrate_created(self, bundle):
        import calendar
        d2 = bundle.obj.id.generation_time
        return d2.strftime("%c")
        

class TopicResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Topic.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete') #TODO: own submission auth
        authorization = authorization.Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/comments%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_comments'), name="api_get_comments"),
        ]

    def get_comments(self, request, **kwargs):

        comment_resource = CommentResource()
        try:
            return comment_resource.get_list(request, topic=kwargs.get('pk', -1), order_by=['-creation'])
        except (mongoengine.errors.ValidationError):
            return tastypie.http.HttpNotFound()

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
