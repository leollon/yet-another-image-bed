from flask import render_template
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.http import HTTP_STATUS_CODES


def file_too_large(error):
    resp_data = {"code": "4013", "message": HTTP_STATUS_CODES.get(413)}
    return resp_data, RequestEntityTooLarge.code


def page_not_found(error):
    return render_template("404.html")


def server_error(error):
    return render_template("500.html")
