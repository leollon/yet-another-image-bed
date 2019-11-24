from .model import PicBed
from flask_restplus import Api, fields, Resource


image_api = Api()
wild = fields.Wildcard
model = image_api.model('image', {
    "img_id": fields.String,
    "img_name": fields.String,
})


@image_api.route("/image/")
class ImageResource(Resource):

    @image_api.doc('list_images')
    @image_api.marshal_list_with(model, envelope='picbed')
    def get(self, *args, **kwargs):
        return PicBed.objects

    @image_api.doc('post_an_image')
    @image_api.marshal_with(model, envelope='picbed')
    def post(self, *args, **kwargs):
        pass

    
    @image_api.doc('remove_an_image')
    def delete(self, *args, **kwargs):
        pass