"""verification for each uploaded image
"""


def allowed_file(file):
    """whether each uploaded file is allowed or not.
    Arguments:
        :type filename: str
        :rtype: bool
    >>> allowed_file('image1.jpg')
    jpg
    >>> allowed_file('image2.png')
    png
    """
    allowed_types = ('image/jpeg', 'image/png', 'image/gif', 'image/svg+xml')
    return '.' in file.filename and \
           file.content_type in allowed_types
