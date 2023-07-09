from typing import Any

from zelda.armor.models import Armor
from zelda.lib.choices import Item
from zelda.lib.views import BaseView


class ArmorView(BaseView):
    template_name = "armor/armor.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG002
        user = self.request.user
        current_levels = dict(user.armor_levels.values_list("armor", "level"))
        remaining_cost = {item: 0 for item in Item.labels()}
        named_levels: dict[str, int] = {}
        for armor in Armor.objects.prefetch_related("costs").order_by(
            "set_code", "body_part_code"
        ):
            current_level = current_levels.get(armor.id, -1)
            named_levels[armor.name] = (
                current_level if current_level >= 0 else "Not purchased"
            )
            for cost in armor.costs.filter(level__gt=current_level):
                remaining_cost[cost.item] += cost.quantity
        return {
            "armors": named_levels,
            "remaining_cost": remaining_cost,
        }
