import json

from flask import Response, render_template
from . import image


@image.app_errorhandler(413)
def file_too_large(e):
    resp_data = {"code": "error", "msg": "file too large"}
    return Response(
        json.dumps(resp_data, indent=4),
        content_type="application/json; charset=utf-8",
        status=413)


@image.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@image.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
