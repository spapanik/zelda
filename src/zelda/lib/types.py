from collections.abc import Callable
from typing import Any

from django.db import models
from django.db.models.deletion import Collector

OnDeleteType = Callable[
    [Collector, Any, models.QuerySet[models.Model], str],
    None,
]
