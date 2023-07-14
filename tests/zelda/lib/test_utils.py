import os
from collections import defaultdict
from pathlib import Path

import pytest

from django.test import override_settings

from zelda.lib import utils


def test_handle_exceptions_handled_exception() -> None:
    @utils.handle_exceptions(exceptions=(ZeroDivisionError,), default=0.0)
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    assert invert(0) == 0


def test_handle_exceptions_unhandled_exception() -> None:
    @utils.handle_exceptions(exceptions=(TypeError,), default=0.0)
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    pytest.raises(ZeroDivisionError, invert, 0)


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


def test_hash_file() -> None:
    dev_null_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert utils.hash_file(Path(os.devnull)) == dev_null_hash


def test_hash_migrations() -> None:
    hashed_migrations = defaultdict(list)
    for hashed_migration in utils.hash_migrations():
        app, name, _ = hashed_migration.split("::")
        hashed_migrations[app].append(name)
    assert "registration" in hashed_migrations
    assert "0001_initial" in hashed_migrations["registration"]
