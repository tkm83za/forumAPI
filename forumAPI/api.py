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
    
#     def dehydrate_topic(self, bundle):
#             bundle.data['topic'] = documents.Topic.objects(__raw__ = {_id:bundle.data['topic']}).first()
#             return bundle.data['topic']
    class Meta:
        queryset = documents.Comment.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = authorization.Authorization() #TODO: own-submission authorization, allow admin to put/patch
        exclude = ['topic']

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
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return tastypie.http.HttpGone("What")
        except mongoengine.MultipleObjectsReturned:
            return tastypie.http.HttpMultipleChoices("More than one resource is found at this URI.")

        comment_resource = CommentResource()
        return comment_resource.get_detail(request, topic=obj.pk)

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
