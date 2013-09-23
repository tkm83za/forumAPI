import mongoengine
import datetime

class InheritableDocument(mongoengine.Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }

class InheritableEmbeddedDocument(mongoengine.EmbeddedDocument):
    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }
    
class User(mongoengine.Document):
    email = mongoengine.EmailField(required=True, unique=True)
    username = mongoengine.StringField(max_length=50)
    is_staff = mongoengine.BooleanField(default=False)
#     first_name = mongoengine.StringField(max_length=50)
#     last_name = mongoengine.StringField(max_length=50)

class Topic(InheritableDocument):
    author = mongoengine.ReferenceField(User, dbref=False)
    name = mongoengine.StringField(max_length=200, required=True)
    blurb = mongoengine.StringField(required=False)

class Comment(InheritableDocument):
    topic = mongoengine.ReferenceField(Topic, required=True, reverse_delete_rule=mongoengine.CASCADE, dbref=False)
    author = mongoengine.StringField(max_length=50, required=False)
    in_reply_to = mongoengine.StringField(max_length=50)#mongoengine.ReferenceField(Comment)
    comment_body = mongoengine.StringField(required=True)
    is_hidden = mongoengine.BooleanField()
    created = mongoengine.DateTimeField()
    