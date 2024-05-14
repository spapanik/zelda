import json
from typing import cast

from midas.lib.types import JSONType

from django.http import JsonResponse as BaseJsonResponse


class JsonResponse(BaseJsonResponse):
    @property
    def data(self) -> JSONType:
        if self.content:
            return cast(JSONType, json.loads(self.content))
        return None
