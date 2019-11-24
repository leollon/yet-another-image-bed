from flask import Blueprint

image = Blueprint('image', '__name__')

from . import views