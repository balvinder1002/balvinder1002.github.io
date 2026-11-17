"""Serve the site over HTTP for the tests, the way GitHub Pages does."""
import functools
import http.server
import threading
from pathlib import Path

import pytest

SITE_ROOT = Path(__file__).resolve().parent.parent


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    # HTTP/1.1 keeps the connection open after a response; with HTTP/1.0 the Windows
    # server sometimes reset the socket mid-transfer on the ~800 KB diagram file.
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def site_url():
    handler = functools.partial(QuietHandler, directory=str(SITE_ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/"
    server.shutdown()


@pytest.fixture
def home(page, site_url):
    """The home page, loaded, with console errors collected."""
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(site_url)
    page.console_errors = errors
    return page
