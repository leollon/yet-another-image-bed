from flask import Blueprint, render_template
from werkzeug.exceptions import InternalServerError, NotFound

from .errors import page_not_found, server_error
from .model import PicBed

image = Blueprint('image', __name__, template_folder='templates')


@image.route('/', methods=['GET'])
def index():
    return render_template('index.html')


image.app_errorhandler(NotFound)(page_not_found)
image.app_errorhandler(InternalServerError)(server_error)


@image.route('/all-images/')
def list_image():
    image_list = PicBed.objects
    return render_template('list.html', image_list=image_list)
