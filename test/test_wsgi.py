"""Tests for the application."""
import subprocess
import time

import requests


def test_wsgi_app():
    """Confirm that the app is being served."""
    command = ["python", "-m", "app.wsgi", "--port=5000"]
    with subprocess.Popen(command) as proc:
        time.sleep(5)
        resp = requests.get("http://localhost:5000", allow_redirects=False)
        proc.kill()
        # Check Flask Talisman is redirecting to https version
        assert (
            resp.status_code == 302
            and resp.headers["location"] == "https://localhost:5000/"
        )
