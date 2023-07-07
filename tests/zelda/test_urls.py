from http import HTTPStatus

from tests.conftest import HttpTestClient


def test_admin(http_client: HttpTestClient) -> None:
    response = http_client.get("/admin", follow=True)
    expected_redirects = [("/admin/", 301), ("/admin/login/?next=/admin/", 302)]
    assert response.status_code == HTTPStatus.OK
    assert response.redirect_chain == expected_redirects
