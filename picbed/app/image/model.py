from datetime import datetime

from flask_mongoengine import MongoEngine
from mongoengine import DateTimeField, Document, StringField

image_db = MongoEngine()


class PicBed(Document):
    img_id = StringField(max_length=10, required=True)
    img_name = StringField(max_length=32, required=True)
    orig_img_name = StringField(required=True)
    created_time = DateTimeField(default=datetime.utcnow())
    meta = {
        "collection": "images",
        "indexes": ['img_id', 'orig_img_name', ('img_id', 'img_name')]
    }

    def __repr__(self):
        return '<%s(img_id=%s, img_name=%s)>' % (self.__class__.__name__, self.img_id, self.img_name)
