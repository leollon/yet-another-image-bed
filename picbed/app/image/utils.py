from pathlib import Path

from flask import abort, current_app
from mongoengine.errors import DoesNotExist

from .model import PicBed


def allowed_file(file):
    """whether each uploaded file is allowed or not.
    Arguments:
        :type file: werkzeug.datastructure.FileStorage
        :rtype: bool
    """
    allowed_types = ("image/jpeg", "image/png", "image/gif", "image/svg+xml")
    return "." in file.filename and file.content_type in allowed_types


def remove_image(img_id, resp):
    try:
        img = PicBed.objects.get(img_id=img_id)
        base_dir = current_app.config["UPLOAD_BASE_FOLDER"]
        file_path = Path(base_dir) / img.img_name
        if file_path.is_file():
            img.delete()
            file_path.unlink()
            return resp
    except DoesNotExist:
        pass
    abort(404)
