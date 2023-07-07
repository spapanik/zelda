from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, auto
from secrets import choice
from typing import Any, Self


@dataclass(frozen=True)
class ChoiceValue:
    key: str
    label: str
    obj: Any


class Choices(Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, _start: int, _count: int, _last_values: list[ChoiceValue]
    ) -> ChoiceValue:
        label = name.replace("_", " ").title()
        return ChoiceValue(name, label, name)

    def __init__(self, value: ChoiceValue):
        self.key = value.key
        self.label = value.label
        self.obj = value.obj

    @classmethod
    def random(cls) -> Self:
        return choice(list(cls))

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.key, item.label) for item in cls]

    @classmethod
    def names(cls) -> Iterator[str]:
        for item in cls:
            yield item.name

    @classmethod
    def values(cls) -> Iterator[ChoiceValue]:
        for item in cls:
            yield item.value

    @classmethod
    def keys(cls) -> Iterator[str]:
        for item in cls:
            yield item.key

    @classmethod
    def labels(cls) -> Iterator[str]:
        for item in cls:
            yield item.label

    @classmethod
    def objects(cls) -> Iterator[Any]:
        for item in cls:
            yield item.obj


class BodyPart(Choices):
    HEAD = auto()
    BODY = auto()
    LEGS = auto()


class ArmorSet(Choices):
    ARCHAIC_SET = auto()
    ARMOR_OF_THE_DEPTHS_SET = auto()
    ARMOR_OF_THE_WILD = auto()
    AWAKENING_SET = auto()
    BARBARIAN_SET = auto()
    CHARGED_SET = auto()
    CLIMBING_SET = auto()
    DARK_SET = auto()
    DESERT_VOE_SET = auto()
    EMBER_SET = auto()
    EVIL_SPIRIT_SET = auto()
    FIERCE_DEITY_SET = auto()
    FLAMEBREAKER_SET = auto()
    FROGGY_SET = auto()
    FROSTBITE_SET = auto()
    GLIDE_SET = auto()
    HERO_SET = auto()
    HYLIAN_SET = auto()
    MINER_SET = auto()
    MYSTIC_SET = auto()
    PHANTOM_SET = auto()
    RADIANT_SET = auto()
    ROYAL_GUARD_SET = auto()
    RUBBER_SET = auto()
    SKY_SET = auto()
    SNOWQUILL_SET = auto()
    SOLDIERS_SET = auto()
    STEALTH_SET = auto()
    TIME_SET = auto()
    TINGLE_SET = auto()
    TWILIGHT_SET = auto()
    WIND_SET = auto()
    YIGA_SET = auto()
    ZONAITE_SET = auto()
    ZORA_SET = auto()


class Item(Choices):
    RUPEE = auto()
    POE = auto()
    BUBBUL_GEM = auto()
    ACORN = auto()
    AEROCUDA_EYEBALL = auto()
    AEROCUDA_WING = auto()
    AMBER = auto()
    BLACK_BOKOBLIN_HORN = auto()
    BLACK_BOSS_BOKOBLIN_HORN = auto()
    BLACK_HINOX_HORN = auto()
    BLACK_HORRIBLIN_HORN = auto()
    BLACK_LIZALFOS_HORN = auto()
    BLADED_RHINO_BEETLE = auto()
    BLUE_BOKOBLIN_HORN = auto()
    BLUE_BOSS_BOKOBLIN_HORN = auto()
    BLUE_HORRIBLIN_HORN = auto()
    BLUE_LIZALFOS_HORN = auto()
    BLUE_LIZALFOS_TAIL = auto()
    BLUE_MOBLIN_HORN = auto()
    BLUE_NIGHTSHADE = auto()
    BLUE_MANED_LYNEL_MACE_HORN = ChoiceValue(
        "BLUE_MANED_LYNEL_MACE_HORN",
        " Blue-Maned Lynel Mace Horn",
        "BLUE_MANED_LYNEL_MACE_HORN",
    )
    BLUE_MANED_LYNEL_SABER_HORN = ChoiceValue(
        "BLUE_MANED_LYNEL_SABER_HORN",
        " Blue-Maned Lynel Saber Horn",
        "BLUE_MANED_LYNEL_SABER_HORN",
    )
    BLUE_WHITE_FROX_FANG = ChoiceValue(
        "BLUE_WHITE_FROX_FANG", " Blue-White Frox Fang", "BLUE_WHITE_FROX_FANG"
    )
    BOKOBLIN_FANG = auto()
    BOKOBLIN_GUTS = auto()
    BOKOBLIN_HORN = auto()
    BOSS_BOKOBLIN_FANG = auto()
    BOSS_BOKOBLIN_HORN = auto()
    BRIGHTBLOOM_SEED = auto()
    BRIGHTCAP = auto()
    CAPTAIN_CONSTRUCT_I_HORN = auto()
    CAPTAIN_CONSTRUCT_II_HORN = auto()
    CAPTAIN_CONSTRUCT_III_HORN = auto()
    CHILLFIN_TROUT = auto()
    CHILLSHROOM = auto()
    CHUCHU_JELLY = auto()
    COLD_DARNER = auto()
    COOL_SAFFLINA = auto()
    COURSER_BEE_HONEY = auto()
    DARK_CLUMP = auto()
    DAZZLEFRUIT = auto()
    DEEP_FIREFLY = auto()
    DIAMOND = auto()
    DINRAAL_S_CLAW = ChoiceValue("DINRAAL_S_CLAW", "Dinraal's Claw", "DINRAAL_S_CLAW")
    DINRAAL_S_HORN = ChoiceValue("DINRAAL_S_HORN", "Dinraal's Horn", "DINRAAL_S_HORN")
    DINRAAL_S_SCALE = ChoiceValue(
        "DINRAAL_S_SCALE", "Dinraal's Scale", "DINRAAL_S_SCALE"
    )
    ELECTRIC_DARNER = auto()
    ELECTRIC_KEESE_WING = auto()
    ELECTRIC_LIZALFOS_HORN = auto()
    ELECTRIC_LIZALFOS_TAIL = auto()
    ELECTRIC_SAFFLINA = auto()
    ENERGETIC_RHINO_BEETLE = auto()
    FAROSH_S_CLAW = ChoiceValue("FAROSH_S_CLAW", "Farosh's Claw", "FAROSH_S_CLAW")
    FAROSH_S_HORN = ChoiceValue("FAROSH_S_HORN", "Farosh's Horn", "FAROSH_S_HORN")
    FAROSH_S_SCALE = ChoiceValue("FAROSH_S_SCALE", "Farosh's Scale", "FAROSH_S_SCALE")
    FIRE_FRUIT = auto()
    FIRE_KEESE_WING = auto()
    FIRE_LIKE_STONE = auto()
    FIRE_BREATH_LIZALFOS_HORN = ChoiceValue(
        "FIRE_BREATH_LIZALFOS_HORN",
        "Fire-Breath Lizalfos Horn",
        "FIRE_BREATH_LIZALFOS_HORN",
    )
    FIRE_BREATH_LIZALFOS_TAIL = ChoiceValue(
        "FIRE_BREATH_LIZALFOS_TAIL",
        "Fire-Breath Lizalfos Tail",
        "FIRE_BREATH_LIZALFOS_TAIL",
    )
    FIREPROOF_LIZARD = auto()
    FLINT = auto()
    FROX_FANG = auto()
    FROX_FINGERNAIL = auto()
    FROX_GUTS = auto()
    GIANT_BRIGHTBLOOM_SEED = auto()
    GIBDO_BONE = auto()
    GIBDO_GUTS = auto()
    GIBDO_WING = auto()
    GLEEOK_FLAME_HORN = auto()
    GLEEOK_FROST_HORN = auto()
    GLEEOK_GUTS = auto()
    GLEEOK_THUNDER_HORN = auto()
    GLEEOK_WING = auto()
    GLOWING_CAVE_FISH = auto()
    HEARTY_BASS = auto()
    HEARTY_LIZARD = auto()
    HIGHTAIL_LIZARD = auto()
    HINOX_GUTS = auto()
    HINOX_TOENAIL = auto()
    HINOX_TOOTH = auto()
    HORRIBLIN_GUTS = auto()
    HORRIBLIN_HORN = auto()
    HOT_FOOTED_FROG = ChoiceValue(
        "HOT_FOOTED_FROG", "Hot-Footed Frog", "HOT_FOOTED_FROG"
    )
    HYRULE_BASS = auto()
    ICE_FRUIT = auto()
    ICE_KEESE_WING = auto()
    ICE_LIKE_STONE = auto()
    ICE_BREATH_LIZALFOS_HORN = ChoiceValue(
        "ICE_BREATH_LIZALFOS_HORN",
        "Ice-Breath Lizalfos Horn",
        "ICE_BREATH_LIZALFOS_HORN",
    )
    ICE_BREATH_LIZALFOS_TAIL = ChoiceValue(
        "ICE_BREATH_LIZALFOS_TAIL",
        "Ice-Breath Lizalfos Tail",
        "ICE_BREATH_LIZALFOS_TAIL",
    )
    KEESE_EYEBALL = auto()
    KEESE_WING = auto()
    LARGE_ZONAI_CHARGE = auto()
    LARGE_ZONAITE = auto()
    LIGHT_DRAGON_S_HORN = ChoiceValue(
        "LIGHT_DRAGON_S_HORN", "Light Dragon's Horn", "LIGHT_DRAGON_S_HORN"
    )
    LIGHT_DRAGON_S_SCALE = ChoiceValue(
        "LIGHT_DRAGON_S_SCALE", "Light Dragon's Scale", "LIGHT_DRAGON_S_SCALE"
    )
    LIGHT_DRAGON_S_TALON = ChoiceValue(
        "LIGHT_DRAGON_S_TALON", "Light Dragon's Talon", "LIGHT_DRAGON_S_TALON"
    )
    LIZALFOS_HORN = auto()
    LIZALFOS_TAIL = auto()
    LIZALFOS_TALON = auto()
    LUMINOUS_STONE = auto()
    LYNEL_GUTS = auto()
    LYNEL_HOOF = auto()
    LYNEL_MACE_HORN = auto()
    LYNEL_SABER_HORN = auto()
    MIGHTY_BANANAS = auto()
    MIGHTY_THISTLE = auto()
    MOBLIN_FANG = auto()
    MOBLIN_GUTS = auto()
    MOBLIN_HORN = auto()
    MOLDUGA_FIN = auto()
    MOLDUGA_GUTS = auto()
    MOLDUGA_JAW = auto()
    NAYDRA_S_HORN = ChoiceValue("NAYDRA_S_HORN", "Naydra's Horn", "NAYDRA_S_HORN")
    NAYDRA_S_SCALE = ChoiceValue("NAYDRA_S_SCALE", "Naydra's Scale", "NAYDRA_S_SCALE")
    OBSIDIAN_FROX_FANG = auto()
    OCTO_BALLOON = auto()
    OCTOROK_EYEBALL = auto()
    OCTOROK_TENTACLE = auto()
    OPAL = auto()
    PUFFSHROOM = auto()
    RAZORCLAW_CRAB = auto()
    RAZORSHROOM = auto()
    RED_CHUCHU_JELLY = auto()
    RUBY = auto()
    RUSHROOM = auto()
    SAPPHIRE = auto()
    SHARD_OF_DINRAAL_S_FANG = ChoiceValue(
        "SHARD_OF_DINRAAL_S_FANG", "Shard of Dinraal's Fang", "SHARD_OF_DINRAAL_S_FANG"
    )
    SHARD_OF_FAROSH_S_FANG = ChoiceValue(
        "SHARD_OF_FAROSH_S_FANG", "Shard of Farosh's Fang", "SHARD_OF_FAROSH_S_FANG"
    )
    SHARD_OF_FAROSH_S_SPIKE = ChoiceValue(
        "SHARD_OF_FAROSH_S_SPIKE", "Shard of Farosh's Spike", "SHARD_OF_FAROSH_S_SPIKE"
    )
    SHARD_OF_LIGHT_DRAGON_S_FANG = ChoiceValue(
        "SHARD_OF_LIGHT_DRAGON_S_FANG",
        "Shard of Light Dragon's Fang",
        "SHARD_OF_LIGHT_DRAGON_S_FANG",
    )
    SHOCK_FRUIT = auto()
    SHOCK_LIKE_STONE = auto()
    SILENT_PRINCESS = auto()
    SILENT_SHROOM = auto()
    SILVER_BOKOBLIN_HORN = auto()
    SILVER_BOSS_BOKOBLIN_HORN = auto()
    SILVER_LIZALFOS_HORN = auto()
    SILVER_LYNEL_MACE_HORN = auto()
    SILVER_LYNEL_SABER_HORN = auto()
    SILVER_MOBLIN_HORN = auto()
    SIZZLEFIN_TROUT = auto()
    SMOTHERWING_BUTTERFLY = auto()
    SNEAKY_RIVER_SNAIL = auto()
    SOLDIER_CONSTRUCT_HORN = auto()
    SOLDIER_CONSTRUCT_II_HORN = auto()
    SOLDIER_CONSTRUCT_III_HORN = auto()
    SOLDIER_CONSTRUCT_IV_HORN = auto()
    STAR_FRAGMENT = auto()
    STEALTHFIN_TROUT = auto()
    STICKY_FROG = auto()
    STICKY_LIZARD = auto()
    SUMMERWING_BUTTERFLY = auto()
    SUNDELION = auto()
    SUNSET_FIREFLY = auto()
    SUNSHROOM = auto()
    SWIFT_CARROT = auto()
    SWIFT_VIOLET = auto()
    THUNDERWING_BUTTERFLY = auto()
    TOPAZ = auto()
    VOLTFIN_TROUT = auto()
    VOLTFRUIT = auto()
    WARM_DARNER = auto()
    WARM_SAFFLINA = auto()
    WHITE_CHUCHU_JELLY = auto()
    WHITE_MANED_LYNEL_MACE_HORN = ChoiceValue(
        "WHITE_MANED_LYNEL_MACE_HORN",
        "White-Maned Lynel Mace Horn",
        "WHITE_MANED_LYNEL_MACE_HORN",
    )
    WHITE_MANED_LYNEL_SABER_HORN = ChoiceValue(
        "WHITE_MANED_LYNEL_SABER_HORN",
        "White-Maned Lynel Saber Horn",
        "WHITE_MANED_LYNEL_SABER_HORN",
    )
    WINTERWING_BUTTERFLY = auto()
    YELLOW_CHUCHU_JELLY = auto()
    ZAPSHROOM = auto()
    ZONAITE = auto()
