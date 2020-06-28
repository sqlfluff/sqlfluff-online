import html
import json

import pytest

import app
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
    assert b"Sqlfluff Online" in rv.data
    assert b"Fixed SQL" not in rv.data


def test_results(client):
    """Test that the results is good to go."""
    sql_encoded = sql_encode("select * from table")
    rv = client.get("/fluffed", query_string=f"""dialect=ansi&sql={sql_encoded}""")
    assert b"Sqlfluff Online" in rv.data
    assert b"Fixed SQL" in rv.data
    assert b"select * from table" in rv.data
