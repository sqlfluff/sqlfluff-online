import sqlfluff
from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .fluff import VALID_DIALECTS, VALID_RULES

limiter = Limiter(
    key_func=get_remote_address, default_limits=["2 per second", "1000 per day"]
)


@limiter.request_filter
def ip_whitelist():
    """Add some exemptions to the limiter."""
    return request.remote_addr in ("127.0.0.1", "localhost")


def create_app():
    """App factory."""
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from . import routes

    limiter.init_app(app)
    app.register_blueprint(routes.bp)

    @app.context_processor
    def inject_vars():
        """Inject arbitrary data into all templates."""
        return dict(
            all_rules=VALID_RULES,
            all_dialects=VALID_DIALECTS,
            sqlfluff_version=sqlfluff.__version__,
        )

    return app
