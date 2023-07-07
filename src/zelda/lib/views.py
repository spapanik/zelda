from typing import Any

from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class BaseView(View):
    template_name: str

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return kwargs

    def get_template_name(self, **_kwargs: Any) -> str:
        return self.template_name

    def render(self, context: dict[str, Any]) -> HttpResponse:
        template = self.get_template_name(**context)
        return render(self.request, template, context)

    def get(
        self, request: HttpRequest, *_args: Any, **kwargs: Any  # noqa: ARG002
    ) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return self.render(context)


class BaseFormView(BaseView):
    form_class: type[BaseForm]

    @property
    def get_form(self) -> type[BaseForm]:
        return self.form_class

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context
