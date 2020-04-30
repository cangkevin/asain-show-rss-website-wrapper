from flask import Blueprint

bp = Blueprint("core", __name__)

from website.core import routes
