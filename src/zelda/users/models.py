from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Self

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest

from zelda.lib.models import BaseModel, BaseQuerySet
from zelda.lib.utils import JWT

if TYPE_CHECKING:
    from zelda.armor.models import UserArmor


class UserManager(BaseUserManager.from_queryset(BaseQuerySet["User"])):  # type: ignore[misc]
    use_in_migrations = True

    def _create_user(
        self, email: str, password: str | None, **extra_fields: Any
    ) -> User:
        if not email:
            msg = "An email must be set"
            raise ValueError(msg)

        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None  # type: ignore[assignment]
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(unique=True)
    armor = models.ManyToManyField("armor.Armor", through="armor.UserArmor")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: ClassVar[UserManager] = UserManager()
    armor_levels: ClassVar[models.Manager[UserArmor]]

    class Meta(AbstractUser.Meta):  # type: ignore[name-defined,misc]
        swappable = "AUTH_USER_MODEL"

    def __str__(self) -> str:
        return self.email

    @classmethod
    def from_request(cls, request: HttpRequest) -> Self:
        bearer = request.META.get("HTTP_AUTHORIZATION")
        if not bearer:
            msg = "No bearer token"
            raise LookupError(msg)

        _, token = bearer.split()
        jwt = JWT.from_token(token)
        if jwt.sub != "access":
            msg = "Not an access token"
            raise LookupError(msg)

        try:
            user: Self = cls.objects.get(email=jwt.email)
        except cls.DoesNotExist as exc:
            msg = "No such user"
            raise LookupError(msg) from exc

        return user

    def get_tokens(self) -> dict[str, str]:
        refresh_token = JWT.for_user(self, "refresh")
        access_token = JWT.for_user(self, "access")
        return {
            "refresh": str(refresh_token),
            "access": str(access_token),
        }
