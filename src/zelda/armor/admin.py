from django.contrib import admin

from zelda.armor.models import Armor, ArmorUpgradeCost
from zelda.users.admin import UserArmorInline


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin[Armor]):
    list_display = ("name", "set_code", "body_part_code", "max_level")
    ordering = ("name",)
    search_fields = ("name", "set_code", "body_part_code")
    list_filter = ("set_code", "body_part_code")
    inlines = (UserArmorInline,)


@admin.register(ArmorUpgradeCost)
class ArmorUpgradeCostAdmin(admin.ModelAdmin[ArmorUpgradeCost]):
    list_display = ("name", "armor", "armor_set")
    ordering = ("id",)
    search_fields = ("armor__name",)
    list_filter = ("armor", "item_code")

    @admin.display(ordering="id", description="Cost name")
    def name(self, obj: ArmorUpgradeCost) -> str:
        return str(obj)

    @admin.display(ordering="armor__set_code", description="Armor set")
    def armor_set(self, obj: ArmorUpgradeCost) -> str:
        return str(obj.armor.armor_set)
