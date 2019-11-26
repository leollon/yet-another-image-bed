from flask import Blueprint, render_template
from werkzeug.exceptions import InternalServerError, NotFound

from .model import PicBed

image = Blueprint('image', __name__, template_folder='templates')


@image.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@image.app_errorhandler(NotFound)
def page_not_found(error):
    return render_template('404.html')


@image.app_errorhandler(InternalServerError)
def server_error(error):
    return render_template('500.html')


@image.route('/all-images/')
def list_image():
    image_list = PicBed.objects
    return render_template('list.html', image_list=image_list)
