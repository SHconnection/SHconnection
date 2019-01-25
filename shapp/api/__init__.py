from flask import Blueprint

api = Blueprint("api",
                __name__,
                )

from . import evaluation, feed, parent, teacher, classes, chart