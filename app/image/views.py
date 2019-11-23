import uuid
import json
from pathlib import Path

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import current_app, request, Response
from flask import render_template, abort
from mongoengine.errors import DoesNotExist
from flask_restplus import Api, fields, Resource

from . import image
from .model import PicBed
from .utils import allowed_file

api = Api()
model = api.model('Model', {
    "img_id": fields.String,
    "img_name": fields.String,
})


@api.route("/image/")
class ImageResource(Resource):

    @api.marshal_with(model, envelope='image')
    def get(self, *args, **kwargs):
        return PicBed.objects

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

@image.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resp_data = {
            "code": 'success',
            "data": {
                "imgName": None,
                "fileId": None
            }
        }
        Path(current_app.config['UPLOAD_BASE_FOLDER']).mkdir(parents=True, exist_ok=True)
        if 'file' not in request.files:
            msg = 'No file part'
            resp_data['code'] = 'failure'
            resp_data['msg'] = msg
            resp_data.pop('data')
            return Response(
                json.dumps(resp_data, indent=4),
                content_type="application/json; charset=utf-8",
                status=400)
        file = request.files['file']
        # if a user don't select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            msg = 'No selected file'
            resp_data['code'] = 'failure'
            resp_data['msg'] = msg
            resp_data.pop('data')
            return Response(
                json.dumps(resp_data, indent=4),
                content_type="application/json; charset=utf-8",
                status=400)
        if file and allowed_file(file.filename):
            original_name = file.filename.rsplit('/')[-1]  # 取上传文件的原始文件名
            file_type = secure_filename(file.filename).rsplit('.')[-1].lower()
            img_name = str(uuid.uuid4()).replace('-',
                                                 '')[:16] + '.' + file_type
            file_id = str(uuid.uuid1()).replace('-', '')[:10]
            status_code = 200
            try:
                file.save((Path(current_app.config['UPLOAD_BASE_FOLDER']) / img_name).as_posix())
            except PermissionError:
                status_code = 502
                resp_data.update({
                    "data": None,
                    "code": 1,
                    "message": "no permission."
                    })
            else:
                resp_data.update({
                    "data": {
                        "imgName": img_name,
                        "fileId": file_id,
                        "origName": original_name
                    }
                })
                pic_bed = PicBed(
                    img_id=file_id, orig_img_name=original_name, img_name=img_name)
                pic_bed.save()
            return Response(
                json.dumps(resp_data, indent=4),
                content_type="application/json; charset=utf-8",
                status=status_code)
        else:
            resp_data['msg'] = 'error'
            return Response(
                json.dumps(resp_data, indent=4),
                content_type='application/json; charset=utf-8',
                status=400)
    return render_template('upload.html')


@image.route('/remove/<img_id>')
def remove(img_id):
    try:
        img = PicBed.objects.get(img_id=img_id)
    except DoesNotExist:
        abort(404)
    base_dir = current_app.config['UPLOAD_BASE_FOLDER']
    file_path = Path(base_dir) / img.img_name
    if file_path.is_file():
        img.delete()
        file_path.unlink()
        return render_template('success.html')
    else:
        return render_template('404.html')


@image.route('/all-images/')
def list_image():
    image_list = PicBed.objects
    return render_template('list.html', image_list=image_list)
