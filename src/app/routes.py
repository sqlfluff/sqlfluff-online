import os
import base64
import gzip

from configparser import MissingSectionHeaderError
from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from sqlfluff.api import fix, lint

bp = Blueprint("routes", __name__)

config_directory = ".temp"
config_file_name = ".sqlfluff"

def sql_encode(data: str) -> str:
    """Gzip and base-64 encode a string."""
    return base64.urlsafe_b64encode(gzip.compress(data.encode())).decode()


def sql_decode(data: str) -> str:
    """Gzip and base-64 decode a string."""
    return gzip.decompress(base64.urlsafe_b64decode(data.encode())).decode()

def write_config_file(config: str) -> str:
    file_name = f"{config_directory}/{config_file_name}-{datetime.now()}"
    if not os.path.exists(config_directory):
        os.mkdir(config_directory)

    f = open(file_name, "w")
    f.write(config)
    f.close()
    return file_name

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
    sqlfluff_config = request.form["sqlfluff_config"]
    return redirect(
        url_for("routes.fluff_results", sql=sql_encode(sql), dialect=dialect, sqlfluff_config=sql_encode(sqlfluff_config))
    )


@bp.route("/fluffed")
def fluff_results():
    """Serve the results page."""
    # we get carriage returns from the form somehow. so split on them and join via
    # regular newline. add a newline to avoid the annoying newline-at-end-of-file error.
    sql = sql_decode(request.args["sql"]).strip()
    sql = "\n".join(sql.splitlines()) + "\n"

    dialect = request.args["dialect"]

    sqlfluff_config = "\n".join(sql_decode(request.args["sqlfluff_config"]).strip().splitlines()) + "\n"

    temp_config_file_path = write_config_file(sqlfluff_config)

    try:
        linted = lint(sql, dialect=dialect, config_path=temp_config_file_path)
        fixed_sql = fix(sql, dialect=dialect, config_path=temp_config_file_path)
    except MissingSectionHeaderError:
        linted = [{"code": "config", "description": "Failed to parse the config as it is missing a section header"}]
        fixed_sql = ""

    os.remove(temp_config_file_path)

    return render_template(
        "index.html",
        results=True,
        sql=sql,
        dialect=dialect,
        sqlfluff_config=sqlfluff_config,
        lint_errors=linted,
        fixed_sql=fixed_sql,
    )
