import json
import uuid
from pathlib import Path

from flask import Blueprint, current_app
from flask_restplus import Api, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from .model import PicBed
from .utils import allowed_file

blueprint = Blueprint('api', __name__)
image_api = Api(
    blueprint, version=1.0, title='Image API',
    description="Image API for listing images, uploding and removing an image",
)
upload_parser = image_api.parser()
upload_parser.add_argument(
    'file', location='files',
    type=FileStorage, required=True
)
image_model = image_api.model('image', {
    "img_id": fields.String,
    "img_name": fields.String,
})


@image_api.route("/image/")
class ImageResource(Resource):

    @image_api.doc('list_images')
    @image_api.marshal_list_with(image_model, envelope='images')
    def get(self):
        return json.loads(PicBed.objects.only('img_id', 'img_name').exclude('id').to_json())

    @image_api.doc('post_an_image')
    @image_api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        status_code = 200
        resp_data = {
            "code": 2000,
            "message": ''
        }
        Path(current_app.config['UPLOAD_BASE_FOLDER']).mkdir(mode=644, parents=True, exist_ok=True)
        if 'file' not in args:
            msg = 'No file part'
            resp_data['code'] = 'failure'
            resp_data['message'] = msg
            resp_data.pop('data')
            return resp_data, 400
        uploaded_file = args['file']
        # if a user don't select file, browser also
        # submit a empty part without filename
        if uploaded_file.filename == '':
            status_code = 400
            msg = ''
            resp_data.update({
                "code": "4000",
                "message": "No selected file"
            })
            resp_data['message'] = msg
        if uploaded_file and allowed_file(uploaded_file):
            original_name = uploaded_file.filename.rsplit('/')[-1]  # 取上传文件的原始文件名
            file_type = secure_filename(uploaded_file.filename).rsplit('.')[-1].lower()
            img_name = str(uuid.uuid4()).replace('-',
                                                 '')[:16] + '.' + file_type
            img_id = str(uuid.uuid1()).replace('-', '')[:10]
            try:
                uploaded_file.save((Path(current_app.config['UPLOAD_BASE_FOLDER']) / img_name).as_posix())
            except PermissionError:
                status_code = 502
                resp_data.update({
                    "code": '5002',
                    "message": "No permission"
                    })
            except RequestEntityTooLarge:
                status_code = 413
                resp_data.update({
                    "code": 4013,
                    "message": "File too large"
                })
            else:
                resp_data["data"] = {
                        "imgName": img_name,
                        "imgId": img_id,
                    }
                resp_data["message"] = "Success"
                PicBed(img_id=img_id, orig_img_name=original_name, img_name=img_name).save()
        else:
            status_code = 400
            resp_data['code'] = 4000
            resp_data['message'] = 'No supported type'
        return resp_data, status_code

    @image_api.doc('remove_an_image')
    def delete(self, *args, **kwargs):
        pass
