import json
import uuid
from pathlib import Path

from flask import Blueprint, current_app
from flask_restplus import Api, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import (InternalServerError, NotFound,
                                 RequestEntityTooLarge)
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.utils import secure_filename

from .errors import file_too_large, page_not_found, server_error
from .model import PicBed
from .utils import allowed_file, remove_image

blueprint = Blueprint("api", __name__)
image_api = Api(
    blueprint,
    doc=False,
    version=1.0,
    title="Image API",
    description="Image API for listing images, uploding and removing an image",
)
image_api.errorhandler(RequestEntityTooLarge)(file_too_large)
image_api.errorhandler(NotFound)(page_not_found)
image_api.errorhandler(InternalServerError)(server_error)
upload_parser = image_api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)
image_model = image_api.model("image", {"img_id": fields.String, "img_name": fields.String})


@image_api.route("/images")
class ImageResourceList(Resource):
    @image_api.doc("list_images")
    @image_api.marshal_list_with(image_model, envelope="images")
    def get(self):
        return json.loads(PicBed.objects.only("img_id", "img_name").exclude("id").to_json())

    @image_api.doc("post_an_image")
    @image_api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        status_code = 200
        resp_data = {"code": 2000, "message": ""}
        Path(current_app.config["UPLOAD_BASE_FOLDER"]).mkdir(mode=0o755, parents=True, exist_ok=True)
        if "file" not in args:
            resp_data["code"] = "failure"
            resp_data["message"] = "No file part"
            resp_data.pop("data")
            return resp_data, 400
        uploaded_file = args["file"]
        # if a user don't select file, browser also
        # submit a empty part without filename
        if uploaded_file.filename == "":
            status_code = 400
            resp_data.update({"code": "4000", "message": "No selected file"})
            return resp_data, status_code
        if uploaded_file and allowed_file(uploaded_file):
            original_name = uploaded_file.filename.rsplit("/")[-1]  # 取上传文件的原始文件名
            file_suffix = secure_filename(uploaded_file.filename).rsplit(".")[-1].lower()
            random_string = uuid.uuid4().hex
            img_name = random_string[:16] + "." + file_suffix
            img_id = random_string[16:]
            try:
                uploaded_file.save((Path(current_app.config["UPLOAD_BASE_FOLDER"]) / img_name).as_posix())
            except PermissionError:
                status_code = 502
                resp_data.update({"code": "5002", "message": "No permission"})
            else:
                resp_data["image"] = {"imgName": img_name, "imgId": img_id}
                resp_data["message"] = "Success"
                PicBed(img_id=img_id, orig_img_name=original_name, img_name=img_name).save()
        else:
            status_code = 400
            resp_data["code"] = 4000
            resp_data["message"] = "No supported type"
        return resp_data, status_code


@image_api.route("/images/<string:img_id>")
class ImageResource(Resource):
    @image_api.doc("remove an image")
    def delete(self, img_id):
        resp = ({"code": "2004", "message": HTTP_STATUS_CODES.get(204)}, 204)
        return remove_image(img_id, resp)
