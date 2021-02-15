"""Tests for the application."""
import subprocess
import time

import requests


def test_wsgi_app():
    """Confirm that the app is being served."""
    command = ["python", "-m", "app.wsgi", "--port=5000"]
    with subprocess.Popen(command) as proc:
        time.sleep(1)
        resp = requests.get("http://localhost:5000")
        resp.raise_for_status()
        proc.kill()

