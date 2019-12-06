from flask import Response, render_template
from werkzeug.exceptions import (InternalServerError, NotFound,
                                 RequestEntityTooLarge)
from werkzeug.http import HTTP_STATUS_CODES


def file_too_large(error):
    resp_data = {"code": "4013", "message": HTTP_STATUS_CODES.get(413)}
    return resp_data, RequestEntityTooLarge.code


def page_not_found(error):
    return Response(render_template("404.html"), status=NotFound.code)


def server_error(error):
    return Response(render_template("500.html"), status=InternalServerError.code)
