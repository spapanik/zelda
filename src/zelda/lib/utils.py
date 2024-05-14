from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Self, cast

from joselib import jwt
from pathurl import URL, Query
from pyutilkit.date_utils import now
from pyutilkit.files import hash_file

from django.conf import settings
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.writer import MigrationWriter

if TYPE_CHECKING:
    from zelda.users.models import User


@dataclass
class JWT:
    sub: Literal["access", "refresh"]
    email: str
    exp: int

    @classmethod
    def for_user(cls, user: "User", jwt_type: Literal["access", "refresh"]) -> Self:
        expiry_delta = (
            settings.REFRESH_TOKEN_EXPIRY
            if jwt_type == "refresh"
            else settings.ACCESS_TOKEN_EXPIRY
        )
        return cls(
            sub=jwt_type,
            email=user.email,
            exp=int((now() + expiry_delta).timestamp()),
        )

    @classmethod
    def from_token(cls, token: str) -> Self:
        return cls(**jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]))  # type: ignore[no-untyped-call]

    def __str__(self) -> str:
        return cast(
            str, jwt.encode(asdict(self), settings.SECRET_KEY, algorithm="HS256")  # type: ignore[no-untyped-call]
        )


def get_app_url(path: str, **kwargs: str | list[str]) -> URL:
    return URL.from_parts(
        scheme=settings.BASE_SCHEME,
        hostname=settings.BASE_APP_DOMAIN,
        port=settings.BASE_APP_PORT,
        path=path,
        query=Query.from_dict(dict_={}, **kwargs),
    )


def hash_migrations() -> list[str]:
    loader = MigrationLoader(None, ignore_no_migrations=True)
    hashes = []
    source = settings.BASE_DIR.joinpath("src").as_posix()
    for (app, migration_name), migration in loader.graph.nodes.items():
        path = MigrationWriter(migration).path
        if path.startswith(source):
            hashes.append(f"{app}::{migration_name}::{hash_file(Path(path))}")
    return sorted(hashes)
