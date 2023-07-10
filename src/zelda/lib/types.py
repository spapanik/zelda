from collections.abc import Callable
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

from django.db import models
from django.db.models.deletion import Collector

OnDeleteType = Callable[
    [Collector, Any, models.QuerySet[models.Model], str],
    None,
]
CustomSerializable = Decimal | date | time | datetime
JsonType = (
    None | int | float | str | bool | list[Any] | dict[str, Any] | CustomSerializable
)
JsonList = list[JsonType]
JsonDict = dict[str, JsonType]
