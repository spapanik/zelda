from collections import defaultdict

import pytest

from django.test import override_settings

from zelda.lib import utils


@override_settings(BASE_DOMAIN="www.example.com", BASE_PORT=443)
@pytest.mark.parametrize(
    ("path", "kwargs", "expected"),
    [
        ("relative/path", {}, "https://www.example.com/relative/path"),
        ("/absolute/path", {}, "https://www.example.com/absolute/path"),
        (
            "relative/path",
            {"foo": "bar"},
            "https://www.example.com/relative/path?foo=bar",
        ),
    ],
)
def test_get_app_url(path: str, kwargs: dict[str, str], expected: str) -> None:
    assert utils.get_app_url(path, **kwargs).string == expected


def test_hash_migrations() -> None:
    hashed_migrations = defaultdict(list)
    for hashed_migration in utils.hash_migrations():
        app, name, _ = hashed_migration.split("::")
        hashed_migrations[app].append(name)
    assert "registration" in hashed_migrations
    assert "0001_initial" in hashed_migrations["registration"]
