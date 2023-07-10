from typing import Any, Literal, TypedDict

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from zelda.armor.models import Armor, UserArmor
from zelda.lib.choices import Item
from zelda.lib.views import BaseView, LoginRequiredError


class UserArmorDict(TypedDict):
    current_level: int | Literal[""]
    max_level: int


class ArmorView(BaseView):
    template_name = "armor/armor.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG002
        user = self.request.user
        if user.is_anonymous:
            raise LoginRequiredError("User must be logged in to view armor")

        current_levels = dict(user.armor_levels.values_list("armor", "level"))
        remaining_cost = {item: 0 for item in Item.labels()}
        user_armor: dict[str, UserArmorDict] = {}
        for armor in Armor.objects.prefetch_related("costs").order_by(
            "set_code", "body_part_code"
        ):
            current_level = current_levels.get(armor.id, -1)
            user_armor[armor.name] = {
                "current_level": current_level if current_level >= 0 else "",
                "max_level": armor.max_level,
            }
            for cost in armor.costs.filter(level__gt=current_level):
                remaining_cost[cost.item] += cost.quantity
        return {
            "user_armor": user_armor,
            "remaining_cost": remaining_cost,
        }


class UpdateArmorView(TemplateView):
    @staticmethod
    def post(request: HttpRequest, *_args: Any, **_kwargs: Any) -> HttpResponse:
        user = request.user
        if user.is_anonymous:
            raise LoginRequiredError("User must be logged in to update armor")

        data = request.POST
        current_levels = dict(user.armor_levels.values_list("armor", "level"))
        update_armor: dict[int, int] = {}

        for armor in Armor.objects.prefetch_related("user_levels"):
            current_level = current_levels.get(armor.id, -1)
            new_level = (
                -1 if (new_data := data.get(armor.name, "-1")) == "" else int(new_data)
            )
            if new_level != current_level:
                update_armor[armor.id] = new_level

        for armor_id, new_level in update_armor.items():
            if new_level == -1:
                UserArmor.objects.filter(user=user, armor_id=armor_id).delete()
            elif current_levels.get(armor_id, -1) == -1:
                UserArmor.objects.create(user=user, armor_id=armor_id, level=new_level)
            else:
                UserArmor.objects.filter(user=user, armor_id=armor_id).update(
                    level=new_level
                )

        return redirect("armor:armor")
