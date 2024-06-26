from __future__ import annotations

from functools import total_ordering
from typing import Any, ClassVar

from django.db import models

from zelda.lib.choices import ArmorSet, BodyPart, Item
from zelda.lib.models import BaseModel, ForeignKey
from zelda.registration.models import User


class Armor(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    set_code = models.CharField(
        max_length=255, choices=ArmorSet.choices(), null=True, blank=True
    )
    body_part_code = models.CharField(max_length=255, choices=BodyPart.choices())
    max_level = models.PositiveSmallIntegerField()

    objects: ClassVar[models.Manager[Armor]]
    costs: ClassVar[models.Manager[ArmorUpgradeCost]]
    user_levels: ClassVar[models.Manager[UserArmor]]

    class Meta:
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["set_code", "body_part_code"],
                name="unique_armor_set_body_part",
            ),
        ]

    @total_ordering
    class SortingKey:
        def __init__(self, armor: Armor):
            self.armor = armor

        def __eq__(self, other: Any) -> bool:
            if not isinstance(other, Armor.SortingKey):
                return NotImplemented

            return self.armor.id == other.armor.id

        def __lt__(self, other: Any) -> bool:
            if not isinstance(other, Armor.SortingKey):
                return NotImplemented

            if self.armor.id == other.armor.id:
                return False

            if self.armor.set_code and not other.armor.set_code:
                return True

            if not self.armor.set_code and other.armor.set_code:
                return False

            if not self.armor.set_code and not other.armor.set_code:
                return self.armor.name < other.armor.name

            if self.armor.set_code != other.armor.set_code:
                return self.armor.set_code < other.armor.set_code  # type: ignore[operator]

            return (
                self.armor.body_part_code == BodyPart.HEAD.key
                or other.armor.body_part_code == BodyPart.LEGS.key
            )

    def __str__(self) -> str:
        return self.name

    def save(self, *_args: Any, **_kwargs: Any) -> None:
        if not self.set_code:
            self.set_code = None
        super().save()

    @property
    def armor_set(self) -> str:
        return ArmorSet[self.set_code].label if self.set_code else ""

    @property
    def body_part(self) -> str:
        return BodyPart[self.body_part].label


class ArmorUpgradeCost(BaseModel):
    armor = ForeignKey(Armor, related_name="costs")
    level = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField()
    item_code = models.CharField(max_length=255, choices=Item.choices(), blank=True)

    objects: ClassVar[models.Manager[ArmorUpgradeCost]]

    class Meta:
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["armor", "level", "item_code"],
                name="unique_level_upgrade_cost",
            ),
        ]

    def __str__(self) -> str:
        level = f"level {self.level}" if self.level else "acquisition"
        if self.free:
            return f"{self.armor} {level} for free"
        return f"{self.quantity} {self.item} for {self.armor} {level}"

    def save(self, *_args: Any, **_kwargs: Any) -> None:
        if bool(self.item_code) ^ bool(self.quantity):
            msg = "Must provide both an item and a quantity if either is provided"
            raise ValueError(msg)
        super().save()

    @property
    def free(self) -> bool:
        return self.quantity == 0

    @property
    def item(self) -> str:
        return "" if self.free else Item[self.item_code].label


class UserArmor(BaseModel):
    user = ForeignKey(User, related_name="armor_levels")
    armor = ForeignKey(Armor, related_name="user_levels")
    level = models.PositiveSmallIntegerField()

    objects: ClassVar[models.Manager[UserArmor]]
