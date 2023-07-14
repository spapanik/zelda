import json

from django.apps.registry import Apps
from django.conf import settings
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

FAIRY_TAX = {
    1: 10,
    2: 50,
    3: 200,
    4: 500,
}


def create_armor(apps: Apps, _schema_editor: BaseDatabaseSchemaEditor) -> None:
    Armor = apps.get_model("armor", "Armor")
    ArmorUpgradeCost = apps.get_model("armor", "ArmorUpgradeCost")

    armor_definitions = settings.PROJECT_DIR.joinpath(
        "zelda", "armor", "data", "armor.json"
    )
    with armor_definitions.open() as file:
        data = json.load(file)

    for armor_name, armor_data in data.items():
        max_level = len(armor_data["upgrades"]) - 1
        armor, _ = Armor.objects.get_or_create(
            name=armor_name,
            defaults={
                "set_code": armor_data.get("set"),
                "body_part_code": armor_data["body_part"],
                "max_level": max_level,
            },
        )

        for level, costs in enumerate(armor_data["upgrades"]):
            if level:
                costs["RUPEE"] = FAIRY_TAX[level] + costs.get("RUPEE", 0)
            for item, quantity in costs.items():
                ArmorUpgradeCost.objects.get_or_create(
                    armor=armor,
                    item_code=item,
                    level=level,
                    defaults={"quantity": quantity},
                )


def drop_armor(apps: Apps, _schema_editor: BaseDatabaseSchemaEditor) -> None:
    Armor = apps.get_model("armor", "Armor")
    ArmorUpgradeCost = apps.get_model("armor", "ArmorUpgradeCost")

    Armor.objects.all().delete()
    ArmorUpgradeCost.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("armor", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_armor, drop_armor)]
