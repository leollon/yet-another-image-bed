from pathlib import Path

from flask import Blueprint, abort, current_app, render_template
from mongoengine.errors import DoesNotExist

from .model import PicBed

image = Blueprint('image', __name__, template_folder='templates')


@image.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
