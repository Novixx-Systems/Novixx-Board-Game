# All of this deprecated info is stored in ServerVariants enum now

GRANDS = ("xiangqi", "manchu", "grand", "grandhouse", "shako", "janggi")

BYOS = (
    "shogi",
    "minishogi",
    "kyotoshogi",
    "dobutsu",
    "gorogoroplus",
    "torishogi",
    "cannonshogi",
    "janggi",
    "shogun",
)

V2C_ORIG = {
}


VARIANTS_ORIG = (
)

VARIANT_ICONS_ORIG = {
}


def variant_display_name_orig(variant):
    if variant == "seirawan":
        return "S-CHESS"
    elif variant == "seirawan960":
        return "S-CHESS960"
    elif variant == "shouse":
        return "S-HOUSE"
    elif variant == "cambodian":
        return "OUK CHAKTRANG"
    elif variant == "ordamirror":
        return "ORDA MIRROR"
    elif variant == "gorogoroplus":
        return "GOROGORO+"
    elif variant == "kyotoshogi":
        return "KYOTO SHOGI"
    elif variant == "torishogi":
        return "TORI SHOGI"
    elif variant == "cannonshogi":
        return "CANNON SHOGI"
    elif variant == "duck":
        return "DUCK CHESS"
    elif variant == "kingofthehill":
        return "KING OF THE HILL"
    elif variant == "3check":
        return "THREE-CHECK"
    elif variant == "dragon":
        return "DRAGON CHESS"
    elif variant == "alice":
        return "ALICE CHESS"
    elif variant == "fogofwar":
        return "FOG OF WAR"
    else:
        return variant.upper()


def _(message):
    return message


TRANSLATED_VARIANT_NAMES_ORIG = {
}
