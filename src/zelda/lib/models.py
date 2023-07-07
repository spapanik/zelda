from collections.abc import Collection, Iterable
from typing import Any, Self, TypeVar, cast
from uuid import uuid4

from django.db import models

from zelda.lib.date_utils import now
from zelda.lib.types import OnDeleteType

_T = TypeVar("_T", bound=models.Model, covariant=True)
_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class ForeignKey(models.ForeignKey[_ST, _GT]):
    def __init__(
        self,
        to: type[models.Model] | str,
        on_delete: OnDeleteType = models.CASCADE,
        related_name: str | None = None,
        related_query_name: str | None = None,
        limit_choices_to: Any = None,
        parent_link: bool = False,  # noqa: FBT001,FBT002
        to_field: str | None = None,
        db_constraint: bool = True,  # noqa: FBT001,FBT002
        **kwargs: Any,
    ):
        super().__init__(
            to,
            on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs,
        )


class OneToOneField(models.OneToOneField[_ST, _GT]):
    def __init__(
        self,
        to: type[models.Model] | str,
        on_delete: OnDeleteType = models.CASCADE,
        to_field: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(to, on_delete, to_field=to_field, **kwargs)


class BaseQuerySet(models.QuerySet[_T]):
    def bulk_create(
        self,
        objs: Iterable[_T],
        batch_size: int | None = None,
        ignore_conflicts: bool = False,  # noqa: FBT001,FBT002
        update_conflicts: bool = False,  # noqa: FBT001,FBT002
        update_fields: Collection[str] | None = None,
        unique_fields: Collection[str] | None = None,
    ) -> list[_T]:
        dt = now()
        for obj in objs:
            obj.updated_at = dt  # type: ignore[attr-defined]
            obj.created_at = dt  # type: ignore[attr-defined]
        return super().bulk_create(
            objs,
            batch_size,
            ignore_conflicts,
            update_conflicts,
            update_fields,
            unique_fields,
        )

    def bulk_update(
        self, objs: Iterable[_T], fields: Iterable[str], batch_size: int | None = None
    ) -> int:
        dt = now()
        for obj in objs:
            obj.updated_at = dt  # type: ignore[attr-defined]
        if "updated_at" not in fields:
            fields = [*fields, "updated_at"]
        return super().bulk_update(objs, fields, batch_size)

    def flat_values(self, key: str) -> models.QuerySet[_T]:
        return cast(models.QuerySet[_T], self.values_list(key, flat=True))

    def random(self) -> _T | None:
        return self.order_by("?").first()

    def update(self, **kwargs: Any) -> int:
        kwargs.setdefault("updated_at", now())
        return super().update(**kwargs)


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    objects: models.Manager[Self] = BaseQuerySet.as_manager()

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.updated_at = now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
