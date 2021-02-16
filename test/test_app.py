"""Tests for the application."""
import app
import pytest
from app.routes import sql_encode


@pytest.fixture
def client():
    """Application fixture."""
    application = app.create_app()

    with application.test_client() as cli:
        yield cli


def test_home(client):
    """Test that the homepage is good to go."""
    rv = client.get("/")
    html = rv.data.decode().lower()
    assert "sqlfluff online" in html
    assert "fixed sql" not in html


def test_results_no_errors(client):
    """Test that the results is good to go when there is no error."""
    sql_encoded = sql_encode("select * from table")
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql_encoded}""")
    html = rv.data.decode().lower()
    assert "sqlfluff online" in html
    assert "fixed sql" in html
    assert "select * from table" in html


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
