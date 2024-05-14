from http import HTTPStatus
from typing import Any, cast

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from zelda.lib.http import JsonResponse
from zelda.users.models import User


class BaseAPIView(View):
    @staticmethod
    def has_permissions(_user: User | AnonymousUser) -> bool:
        return True

    @csrf_exempt
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        user: User | AnonymousUser
        try:
            user = User.from_request(request)
        except LookupError:
            user = AnonymousUser()
        if self.has_permissions(user):
            self.request.user = user
            return cast(JsonResponse, super().dispatch(request, *args, **kwargs))
        if user.is_anonymous:
            return JsonResponse(
                {"error": {"message": "You must be logged in to perform this action."}},
                status=HTTPStatus.UNAUTHORIZED,
            )
        return JsonResponse(
            {
                "error": {
                    "message": "You do not have permission to perform this action."
                }
            },
            status=HTTPStatus.FORBIDDEN,
        )


class BaseAuthenticatedAPIView(BaseAPIView):
    @staticmethod
    def has_permissions(user: User | AnonymousUser) -> bool:
        return user.is_authenticated


class BaseStaffAPIView(BaseAPIView):
    @staticmethod
    def has_permissions(user: User | AnonymousUser) -> bool:
        return user.is_staff
