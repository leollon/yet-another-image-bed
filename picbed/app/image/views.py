from flask import Blueprint, render_template
from werkzeug.exceptions import InternalServerError, NotFound

from .errors import page_not_found, server_error
from .model import PicBed
from .utils import remove_image

image = Blueprint("image", __name__, template_folder="templates")
image.app_errorhandler(NotFound)(page_not_found)
image.app_errorhandler(InternalServerError)(server_error)


@image.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@image.route("/remove/<string:img_id>", methods=["GET"])
def remove(img_id):
    resp = render_template("success.html")
    return remove_image(img_id, resp)


@image.route("/all-images/", methods=["GET"])
def list_image():
    image_list = PicBed.objects
    return render_template("list.html", image_list=image_list)
