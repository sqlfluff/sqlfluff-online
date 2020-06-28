from flask import Blueprint, render_template, request

from .fluff import fix, lint

bp = Blueprint("routes", __name__)


@bp.route("/")
def home():
    """The main page."""
    return render_template("index.html", result=False)


@bp.route("/fluffed")
def fluff_results():
    """The results page."""
    sql = request.args["sql"].strip() + "\n"
    dialect = request.args["dialect"]

    return render_template(
        "index.html",
        results=True,
        sql=sql,
        dialect=dialect,
        lint_errors=lint(sql, dialect=dialect),
        fixed_sql=fix(sql, dialect=dialect),
    )
