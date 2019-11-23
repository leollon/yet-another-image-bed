from datetime import datetime
from mongoengine import Document, StringField, DateTimeField
from flask_mongoengine import MongoEngine

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

    def __str__(self):
        return self.img_name
