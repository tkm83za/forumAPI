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
class Topic(InheritableDocument):
    name = mongoengine.StringField(max_length=200, required=True)
    blurb = mongoengine.StringField(required=False)
    