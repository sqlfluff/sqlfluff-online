"""Tests for the application."""

import app
import pytest
from app.routes import sql_encode
from bs4 import BeautifulSoup
from unittest.mock import patch


@pytest.fixture
def client():
    """Application fixture."""
    application = app.create_app()
    application.debug = True

    with application.test_client() as cli:
        yield cli


def test_home(client):
    """Test that the homepage is good to go."""
    rv = client.get("/")
    html = rv.data.decode().lower()
    assert "sqlfluff online" in html
    assert "fixed sql" not in html


def test_post_redirect(client):
    """Test the redirect works."""
    rv = client.post(
        "/",
        data=dict(sql="1234", dialect="ansi"),
        follow_redirects=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert rv.status_code == 302 and "/fluffed?sql" in rv.headers["location"]


@pytest.mark.parametrize("dialect", ["sparksql", "Apache Spark SQL"])
def test_results_no_errors(client, dialect):
    """Test that the results is good to go when there is no error.

    Parameterized dialect asserts that either the formatted name or label can be used
    as the dialect parameter.
    """
    sql_encoded = sql_encode("select * from table")
    rv = client.get("/fluffed", query_string=f"""dialect={dialect}&sql={sql_encoded}""")
    html = rv.data.decode().lower()
    assert "sqlfluff online" in html
    assert "fixed sql" in html
    assert "select * from table" in html

    # Test that the dialect is correctly selected in the results page.
    selected_dialect = (
        BeautifulSoup(html, "html.parser")
        .find("select", {"id": "sql_dialect"})
        .find("option", {"selected": "selected"})
    )
    assert selected_dialect.text.strip() == "apache spark sql"


def test_results_some_errors(client):
    """Test that the results is good to go with one obvious error."""
    sql_encoded = sql_encode("select * FROM table")
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql_encoded}""")
    html = rv.data.decode().lower()
    assert "sqlfluff online" in html
    assert "fixed sql" in html
    assert "select * from table" in html
    assert "line / position" in html
    assert "1 / 10" in html  # position of the error


def test_carriage_return_sql(client):
    """Test the splitlines fix.

    If it doesn't work, we should have one extra fixed character per carriage return.
    """
    sql_encoded = sql_encode("select col \r\n \r\n \r\n from xyz")
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql_encoded}""")

    html = rv.data.decode().lower()
    soup = BeautifulSoup(html, "html.parser")
    user_sql = soup.find("textarea", {"id": "user_sql"}).text
    fixed_sql = soup.find("textarea", {"id": "fixedsql"}).text
    table_of_errors = soup.find("table", {"id": "table_of_errors"}).text

    # we should get an extra z in there if the carriage returns are not well handled.
    assert fixed_sql.count("z") == 1
    assert user_sql.endswith("\n")
    assert str("L009").lower() not in table_of_errors
    assert str("Files must end with a trailing newline").lower() not in table_of_errors


def test_newlines_in_error(client):
    """Test newlines in error messages get correctly displayed"""
    sql_encoded = sql_encode("select 1 from t group by 1\n\nAAAAAA")
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql_encoded}""")

    html = rv.data.decode().lower()
    soup = BeautifulSoup(html, "html.parser")
    table_of_errors = str(soup.find("table", {"id": "table_of_errors"}))
    # Note we want HTML in above so use str() not .text()

    # Check that we have the error with new lines, wrapped in a <pre>:
    assert (
        str.lower("<pre>Line 3, Position 1: Found unparsable section: 'AAAAAA'</pre>")
        in table_of_errors
    )


@patch("app.routes.lint")
def test_runtime_error(mock_lint, client):
    """Test that a runtime error is handled."""
    mock_lint.side_effect = RuntimeError("This is a test error")
    sql_encoded = sql_encode("select * from table")
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql_encoded}""")
    html = rv.data.decode().lower()
    assert "sqlfluff online" in html
    assert "fixed sql" in html
    assert "select * from table" in html
    assert "runtimeerror" in html
    assert "this is a test error" in html


def test_security_headers(client):
    """Test flask-talisman is setting the security headers"""
    rv = client.get("/")
    assert (
        rv.headers["Content-Security-Policy"] != None
        and rv.headers["X-Content-Type-Options"] == "nosniff"
    )
