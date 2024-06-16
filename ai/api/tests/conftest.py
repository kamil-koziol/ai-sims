import warnings

import pytest
from fastapi.testclient import TestClient

from api.app import App


@pytest.fixture(autouse=True)
def ignore_httpx_deprecation_warning():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        yield


@pytest.fixture
def client():
    app = App()
    with TestClient(app.app) as client:
        yield client
