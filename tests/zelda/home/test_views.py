from http import HTTPStatus
from pathlib import Path

from tests.conftest import HttpTestClient


def test_homepage(http_client: HttpTestClient) -> None:
    response = http_client.get("/")
    assert response.status_code == HTTPStatus.OK
    template = Path(response.templates[0].origin.name)
    assert template.name == "home.html"
