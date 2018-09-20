"""verification for each uploaded image
"""
from flask import current_app


def allowed_file(filename):
    """whether each uploaded file is allowed or not.
    Arguments:
        :type filename: str
        :rtype: bool
    >>> allowed_file('image1.jpg')
    jpg
    >>> allowed_file('image2.png')
    png
    """
    allowed_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_types