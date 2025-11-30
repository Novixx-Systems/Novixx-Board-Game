from dataclasses import dataclass
from enum import Enum
from typing import Callable

from compress import (
    encode_move_duck,
    encode_move_flipping,
    encode_move_standard,
    decode_move_duck,
    decode_move_flipping,
    decode_move_standard,
)
from settings import PROD


@dataclass
class Variant:
    code: str
    uci_variant: str
    display_name: str
    icon: str
    chess960: bool = False
    grand: bool = False
    byo: bool = False
    two_boards: bool = False
    base_variant: str = ""
    move_encoding: Callable = encode_move_standard
    move_decoding: Callable = decode_move_standard


#  Deferred translations!
def _(message):
    return message


class ServerVariants(Enum):
    def __init__(self, variant):
        self.code = variant.code
        self.uci_variant = variant.uci_variant
        self.display_name = variant.display_name.upper()
        self.translated_name = variant.display_name
        self.icon = variant.icon
        self.chess960 = variant.chess960
        self.grand = variant.grand
        self.byo = variant.byo
        self.two_boards = variant.two_boards
        self.base_variant = variant.base_variant
        self.move_encoding = variant.move_encoding
        self.move_decoding = variant.move_decoding

    NOVIXXIA = Variant("*", "chess", _("Chess"), "N")
    NOVIXXIA960 = Variant("*", "chess", _("Chess Randomizer"), "N", chess960=True)


    @property
    def server_name(self):
        return self.uci_variant + ("960" if self.chess960 else "")


del _


def get_server_variant(uci_variant, chess960):
    return ALL_VARIANTS[uci_variant + ("960" if chess960 else "")]


NO_VARIANTS = (
)

TWO_BOARD_VARIANTS = tuple(variant for variant in ServerVariants if variant.two_boards)
TWO_BOARD_VARIANT_CODES = [variant.code for variant in TWO_BOARD_VARIANTS]

ALL_VARIANTS = {variant.server_name: variant for variant in ServerVariants}

VARIANTS = {
    variant.server_name: variant for variant in ServerVariants if variant not in NO_VARIANTS
}

VARIANT_ICONS = {variant.server_name: variant.icon for variant in ServerVariants}


DEV_VARIANTS = (
)

# Remove DEV variants on prod site until they stabilize
if PROD:
    for variant in DEV_VARIANTS:
        del VARIANTS[variant.server_name]

# Two board variants has no ratings implemented so far
RATED_VARIANTS = tuple(
    variant.server_name
    for variant in ServerVariants
    if (variant not in NO_VARIANTS) and (variant not in DEV_VARIANTS) and not variant.two_boards
)

NOT_RATED_VARIANTS = tuple(
    variant.server_name
    for variant in ServerVariants
    if (variant.server_name not in RATED_VARIANTS) and (variant.server_name in VARIANTS)
)

C2V = {variant.code: variant.uci_variant for variant in ServerVariants}

GRANDS = tuple(variant.server_name for variant in ServerVariants if variant.grand)

BYOS = tuple(variant.server_name for variant in ServerVariants if variant.byo)


if __name__ == "__main__":
    print(GRANDS)

    from deprecated import VARIANT_ICONS_ORIG, V2C_ORIG

    for sn, variant in VARIANTS.items():
        print(variant.code, variant.icon, sn)
        assert variant.code == V2C_ORIG[variant.uci_variant]
        assert variant.icon == VARIANT_ICONS_ORIG[variant.server_name]
