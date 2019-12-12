from flask import render_template
from website.errors import bp

from website.rss_client import InvalidResourceError, ClientTimeoutError
from website.const import USER_ERROR_TEMPLATE, SERVER_ERROR_TEMPLATE


@bp.app_errorhandler(InvalidResourceError)
def not_found_error(error):
    return render_template(USER_ERROR_TEMPLATE), 404


@bp.app_errorhandler(ClientTimeoutError)
@bp.app_errorhandler(500)
def internal_error(error):
    return render_template(SERVER_ERROR_TEMPLATE), 500
