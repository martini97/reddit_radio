import tempfile
from pathlib import Path

import pytest

from reddit_radio.database import _tables, create_tables_if_needed, database


def skip_autofixt(request):
    if "noautofixt" not in request.keywords:
        return False

    noautofixt = [
        marker
        for marker in request.keywords._markers.get("pytestmark")
        if marker.name == "noautofixt" and request.fixturename in marker.args
    ]

    return len(noautofixt) > 0


@pytest.fixture(autouse=True)
def setup_teardown_database(request):
    if skip_autofixt(request):
        yield
    else:
        create_tables_if_needed()
        yield
        database.drop_tables(_tables)


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile() as file:
        yield Path(file.name)
