"""Init the applicaiton."""

from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from . import csp

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
    talisman = Talisman(
        app,
        content_security_policy=csp.csp,
        content_security_policy_nonce_in=["script-src"],
    )

    from . import config, routes

    limiter.init_app(app)
    app.register_blueprint(routes.bp)

    @app.context_processor
    def inject_vars():
        """Inject arbitrary data into all templates."""
        return dict(
            all_rules=config.VALID_RULES,
            all_dialects=config.VALID_DIALECTS,
            sqlfluff_version=config.SQLFLUFF_VERSION,
        )

    return app
