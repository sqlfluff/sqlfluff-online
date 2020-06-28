import html
import json

import pytest

import app


@pytest.fixture
def client():
    """Application fixture."""
    application = app.create_app()

    with application.test_client() as cli:
        yield cli


def test_home(client):
    """Test that the homepage is good to go."""
    rv = client.get("/")
    assert b"Sqlfluff Online" in rv.data
    assert b"Fixed SQL" not in rv.data


def test_results(client):
    """Test that the results is good to go."""
    sql = html.escape(("select * from table").replace(" ", "%20"))
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql}""")
    assert b"Sqlfluff Online" in rv.data
    assert b"Fixed SQL" in rv.data
