from flask import Blueprint

bp = Blueprint("search", __name__)

from website.search import routes
