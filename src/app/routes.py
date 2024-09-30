import base64
import gzip

from flask import Blueprint, redirect, render_template, request, url_for
from sqlfluff.api import fix, lint
from .config import VALID_DIALECTS

bp = Blueprint("routes", __name__)


def sql_encode(data: str) -> str:
    """Gzip and base-64 encode a string."""
    return base64.urlsafe_b64encode(gzip.compress(data.encode())).decode()


def sql_decode(data: str) -> str:
    """Gzip and base-64 decode a string."""
    return gzip.decompress(base64.urlsafe_b64decode(data.encode())).decode()


@bp.route("/", methods=["GET", "POST"])
def home():
    """Render the main page."""
    if request.method == "GET":
        return render_template("index.html", result=False)

    # if there is post data, we have the form and need to encode the SQL
    # to pass to the results route.
    #
    # this encoding dance is to protect against the possibility of getting a very
    # long SQL string that breaks something in HTTP get.
    sql = request.form["sql"]
    dialect = request.form["dialect"]
    return redirect(
        url_for("routes.fluff_results", sql=sql_encode(sql), dialect=dialect)
    )


@bp.route("/fluffed")
def fluff_results():
    """Serve the results page."""
    # we get carriage returns from the form somehow. so split on them and join via
    # regular newline. add a newline to avoid the annoying newline-at-end-of-file error.
    sql = sql_decode(request.args["sql"]).strip()
    sql = "\n".join(sql.splitlines()) + "\n"

    # dialect must be a dialect label for `load_raw_dialect`. VALID_DIALECTS is a
    # dictionary of dialect labels to dialect names. If we have a name, we need to
    # get the label.
    dialect = request.args["dialect"]
    if dialect in VALID_DIALECTS.values():
        dialect = next(
            label for label, name in VALID_DIALECTS.items() if name == dialect
        )

    try:
        linted = lint(sql, dialect=dialect)
        fixed_sql = fix(sql, dialect=dialect)
    except RuntimeError as e:
        linted = [
            {
                "start_line_no": 1,
                "start_line_pos": 1,
                "code": "RuntimeError",
                "description": str(e),
            }
        ]
        fixed_sql = sql
    return render_template(
        "index.html",
        results=True,
        sql=sql,
        dialect=dialect,
        lint_errors=linted,
        fixed_sql=fixed_sql,
    )
