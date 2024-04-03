"""
Configurations for running the script to generate plots and CSVs.

For convenience, this file stores (or will store) several pre-made "types" of configurations,
so that you don't have to change everything whenever you want to run something different.
"""

from params import *

TEMPORARY_MEGA_FIX = False  # Whether to turn off megas from default attacker criteria
TEMPORARY_FRIENDSHIP_DEFAULT = "Not"

#CONFIG_WRITE_ALL_COUNTERS = True

SINGLE_TYPE_ATTACKER = ["Psychic"]
MULTI_TYPE_ATTACKERS_COMPARE = ["Dark", "Ghost"]  # Use this for Dark/Ghost
EXTRA_TYPE_ATTACKER = ["Ground"]  # Attacker types that use non-STAB moves, doesn't apply to moves
    # Dark/Ghost: Psychic (Mewtwo, Mega Alakazam)
    # Dragon: Fire, Water (Mega Charizard Y, Mega Gyarados)
    # Electric: Psychic (Mewtwo)
    # Fairy: Electric, Psychic (Xurkitree, Mega Alakazam)
    # Fighting: Psychic (Mega Alakazam)
    # Fire: Psychic (Mewtwo)
    # Flying: Grass (Kartana AS/AA)
    # Grass: Electric (Xurkitree)
    # Ice: Psychic (Mewtwo)
    # Rock: Ground (Landorus-I RT/RS)
MODE = "SINGLE"  # SINGLE, SINGLE+, MULTI, MULTI+  (Use MULTI+ for DARK GHOST)

#CONFIG_SORT_OPTION = "Estimator"
#CONFIG_SORT_OPTIONS = ["Estimator", "TTW"]
CONFIG_SORT_OPTIONS = ["Estimator"]
# Sorting option as on Pokebattler:
# "Overall", "Power", "Win Rate", "Time to Win", "Potions", "Damage (TDO)", "Estimator"
# Recommended to use either Estimator or TTW; others may not be perfectly supported.

def get_move_types():
    return SINGLE_TYPE_ATTACKER if "SINGLE" in MODE else MULTI_TYPE_ATTACKERS_COMPARE

def get_pokemon_types():
    return (
        SINGLE_TYPE_ATTACKER if MODE == "SINGLE"
        else SINGLE_TYPE_ATTACKER + EXTRA_TYPE_ATTACKER if MODE == "SINGLE+"
        else MULTI_TYPE_ATTACKERS_COMPARE if MODE == "MULTI"
        else MULTI_TYPE_ATTACKERS_COMPARE + EXTRA_TYPE_ATTACKER  # MULTI+
    )

def get_ensemble_weak_key():
    return ("Weak to contender types" if "MULTI" not in MODE
            else "Weak to contender types simultaneously")

CONFIG_BATTLE_SETTINGS = {
    # All battle settings that are allowed on Pokebattler counters list page, EXCEPT attacker level.
    # Can accept lists instead of a single value, e.g. "Weather": ["Extreme", "Rainy"],
    # In that case, simulations for all combinations of all specified options will be generated.
    "Weather": "Extreme",  # "Extreme",  # Extreme/No Weather/Neutral, Sunny/Clear, Rainy, Partly Cloudy, Cloudy, Windy, Snow, Fog
                           # Default: Extreme
    "Friendship": "Best",  # Not Friend, New Friend, Good Friend, Great Friend, Ultra Friend, Best Friend (can omit "Friend")
                           # Default: Best Friend
    "Attack strategy": "No Dodging",  # No Dodging, Dodge Specials PRO, Dodge All Weave
                                      # Default: No Dodging
    "Dodge strategy": "Realistic Dodging"  # Perfect Dodging, Realistic Dodging, Realistic Dodging Pro, 25 Percent Dodging
                                           # Default: Realistic Dodging
}

CONFIG_ATTACKER_CRITERIA = [
    # Lists of attackers you want to view for analysis.
    # You can specify several sets of criteria, each enclosed by a {} with the format shown below.
    # An attacker will be considered if it satisfies any single {} block.
    # To use a filter, delete the first # at the start of the line, and then change the value as you wish.
    # To drop a filter, add back the # at the start of the line.
    # {
    #     # Each block contains several filters. To meet the criteria for this particular {} block,
    #     # an attacker needs to pass all the filters (example: Ice charged move, levels 30-50, AND non-shadow).
    #     #"Charged move types": SINGLE_TYPE_ATTACKER,
    #     #"Charged move types": MULTI_TYPE_ATTACKERS_COMPARE,
    #     "Charged move types": get_move_types(),
    #                                       # This is an approximation for "attacker type",
    #                                       # and should be used primarily for type-based filtering.
    #                                       # Always put "" around type names!
    #     "Min level": 30,
    #     "Max level": 50,
    #     "Level step size": 5, #5,  # Can be as low as 0.5, but recommend 5 for efficiency
    #     # "Pokemon code names": [],  # Specific Pokemon to be considered,
    #         # e.g. "MEWTWO", "VENUSAUR_SHADOW_FORM", "RAICHU_ALOLA_FORM",
    #         # "SLOWBRO_GALARIAN_FORM", "CHARIZARD_MEGA_Y"
    #         # NOTE: This does NOT guarantee the required Pokemon will be on the counters list,
    #         # especially if the Pokemon is too weak to be in top 32 against bosses.
    #         # To guarantee results, use "Pokemon code names and moves" instead.
    #     #"Pokemon code names and moves": [],
    #         # Specific Pokemon and movesets to be considered, as a list of tuples. Possibly including IVs.
    #         # e.g. [
    #         #     ("URSALUNA", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
    #         #     ("URSALUNA", "TACKLE_FAST", "HIGH_HORSEPOWER"),
    #         #     ("GOLURK_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         #     ("GARCHOMP_MEGA", "MUD_SHOT_FAST", "EARTH_POWER", "10/10/10"),
    #         #     ...
    #         # ]
    #         # This DOES guarantee the required Pokemon will be on the counters list.
    #         # Use this option if you want to test unreleased Pokemon or movesets, or Pokemon that are too weak
    #         # to appear on any of the top 32 lists.
    #     # "Trainer ID": 52719,  # Pokebattler trainer ID
    #     #                       # If this is provided, only Pokemon from that Trainer's Pokebox are used
    #     # "Must be shadow": False,  # This describes attackers, not bosses
    #     # "Must be non shadow": True,
    #     # "Must be mega": True,
    #     # "Must be non mega": True,
    #     # "Must be legendary": False,
    #     # "Must be non legendary": True,
    #     # "Must be mythical": False,
    #     # "Must be non mythical": True,
    #     # "Must be legendary or mythical": False,
    #     # "Must be non legendary or mythical": False,
    #     #"Pokemon types": SINGLE_TYPE_ATTACKER,  # Only use this if you know what you're doing
    #     #"Pokemon types": SINGLE_TYPE_ATTACKER + ["Psychic"],  # Only use this if you know what you're doing
    #     #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE,
    #     #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE + ["Psychic"],
    #     "Pokemon types": get_pokemon_types(),
    #     # "Fast move types": ["Flying"],  # Only use this if you know what you're doing
    #     "Exclude": ["LUCARIO_MEGA", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "MEWTWO_MEGA_X", "MEWTWO_MEGA_Y",
    #                 "CALYREX_SHADOW_RIDER_FORM", "BLACEPHALON", "ETERNATUS", "ETERNATUS_ETERNAMAX_FORM"],
    #         # Specific Pokemon to be excluded,
    #         # in the same format as "Pokemon code names", e.g. "VENUSAUR_SHADOW_FORM"
    # },
    # # {
    # #     "Trainer ID": 52719,
    # #     #"Charged move types": SINGLE_TYPE_ATTACKER,
    # #     #"Charged move types": MULTI_TYPE_ATTACKERS_COMPARE,
    # #     "Charged move types": get_move_types(),
    # #     #"Pokemon types": SINGLE_TYPE_ATTACKER,  # Only use this if you know what you're doing
    # #     #"Pokemon types": SINGLE_TYPE_ATTACKER + ["Psychic"],  # Only use this if you know what you're doing
    # #     #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE,
    # #     #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE + ["Psychic"],
    # #     "Pokemon types": get_pokemon_types(),
    # #     # "Fast move types": ["Fire"],  # Only use this if you know what you're doing
    # # },
    # {
    #     "Min level": 30,
    #     "Max level": 50,
    #     "Level step size": 5,
    #     "Pokemon code names and moves": [
    #         # REMINDER: UPDATE "Attackers that should not be combined"
    #
    #         # Future Pokemon
    #         # Future shadows
    #         # Future megas
    #         # Better moves
    #         # Signature moves
    #
    #         # [Dark Ghost]
    #         # ("DHELMISE", "SHADOW_CLAW_FAST", "SHADOW_BALL"),  # Future Pokemon
    #         # ("LUNALA", "CONFUSION_FAST", "SHADOW_BALL"),
    #         # ("LUNALA", "AIR_SLASH_FAST", "SHADOW_BALL"),
    #         # ("MARSHADOW", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
    #         # ("MARSHADOW", "SHADOW_CLAW_FAST", "SHADOW_PUNCH"),
    #         # ("MARSHADOW", "ASTONISH_FAST", "SHADOW_BALL"),
    #         # ("BLACEPHALON", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
    #         # ("BLACEPHALON", "ASTONISH_FAST", "SHADOW_BALL"),
    #         # ("POLTEAGEIST", "HEX_FAST", "SHADOW_BALL"),
    #         # ("GRIMMSNARL", "BITE_FAST", "FOUL_PLAY"),
    #         # ("GRIMMSNARL", "SUCKER_PUNCH_FAST", "FOUL_PLAY"),
    #         # ("CURSOLA", "HEX_FAST", "SHADOW_BALL"),
    #         # ("DRAGAPULT", "HEX_FAST", "SHADOW_BALL"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "SUCKER_PUNCH_FAST", "PAYBACK"),
    #         # ("CALYREX_SHADOW_RIDER_FORM", "CONFUSION_FAST", "SHADOW_BALL"),  # (Spectrier no fast move)
    #         # ("GENGAR_SHADOW_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),  # Future shadows
    #         # ("GENGAR_SHADOW_FORM", "LICK_FAST", "SHADOW_BALL"),
    #         # ("CHANDELURE_SHADOW_FORM", "HEX_FAST", "SHADOW_BALL"),
    #         # ("HYDREIGON_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "DARK_PULSE"),
    #         # ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "SHADOW_BALL"),
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),  # Future megas
    #         # ("TYRANITAR_MEGA", "BITE_FAST", "CRUNCH"),
    #         # ("SHARPEDO_MEGA", "BITE_FAST", "CRUNCH"),  # Mega Sableye ignored due to low power
    #         # ("TYRANITAR", "BITE_FAST", "FOUL_PLAY"),  # Better moves
    #         # ("TYRANITAR", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "FOUL_PLAY"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_MEGA", "BITE_FAST", "FOUL_PLAY"),
    #         # ("TYRANITAR_MEGA", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR", "SNARL_FAST", "CRUNCH"),
    #         # ("TYRANITAR", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("TYRANITAR", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_SHADOW_FORM", "SNARL_FAST", "CRUNCH"),
    #         # ("TYRANITAR_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("TYRANITAR_SHADOW_FORM", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_MEGA", "SNARL_FAST", "CRUNCH"),
    #         # ("TYRANITAR_MEGA", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("TYRANITAR_MEGA", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("GYARADOS_MEGA", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("ABSOL", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("ABSOL_SHADOW_FORM", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("ABSOL_MEGA", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("HONCHKROW", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("HONCHKROW_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("KROOKODILE", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("GRENINJA", "FEINT_ATTACK_FAST", "BRUTAL_SWING"),
    #         # ("INCINEROAR", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("ZARUDE", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("DARKRAI", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "SUCKER_PUNCH_FAST", "FOUL_PLAY"),  # Or Snarl
    #         # ("LUNALA", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
    #         # ("LUNALA", "HEX_FAST", "SHADOW_BALL"),
    #         # ("SPECTRIER", "HEX_FAST", "SHADOW_BALL"),
    #         # ("CALYREX_SHADOW_RIDER_FORM", "HEX_FAST", "SHADOW_BALL"),
    #         # ("DARKRAI", "SNARL_FAST", "BRUTAL_SWING"),  # Signature moves (Dark)
    #         # ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("ZOROARK", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("PANGORO", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("HOOPA_UNBOUND_FORM", "ASTONISH_FAST", "BRUTAL_SWING"),
    #         # ("GRIMMSNARL", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("GRIMMSNARL", "SUCKER_PUNCH_FAST", "BRUTAL_SWING"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "SUCKER_PUNCH_FAST", "BRUTAL_SWING"),  # Or Snarl
    #         # ("DECIDUEYE", "ASTONISH_FAST", "SHADOW_FORCE"),  # Signature moves (Ghost) (Most of them already have Shadow Ball elsewhere)
    #         # ("DECIDUEYE", "ASTONISH_FAST", "SHADOW_BALL"),
    #         # ("DECIDUEYE", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
    #         # ("LUNALA", "HEX_FAST", "SHADOW_FORCE"),
    #         # ("NECROZMA_DAWN_WINGS_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),  # (Signature move)
    #         # ("MARSHADOW", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
    #         # ("CALYREX_SHADOW_RIDER_FORM", "HEX_FAST", "SHADOW_FORCE"),
    #
    #         # [DarkGhost] for boss movesets
    #         # ("TYRANITAR", "BITE_FAST", "CRUNCH"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "CRUNCH"),
    #         # ("TYRANITAR_MEGA", "BITE_FAST", "CRUNCH"),
    #         # ("HYDREIGON", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("HYDREIGON_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_MEGA", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "CRUNCH", "10/10/10"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "CRUNCH", "5/5/5"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "CRUNCH", "0/0/0"),
    #         # ("WEAVILE", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("WEAVILE_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("DARKRAI", "SNARL_FAST", "DARK_PULSE"),
    #         # ("DARKRAI", "SNARL_FAST", "SHADOW_BALL"),
    #         # ("GIRATINA_ORIGIN_FORM", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
    #
    #         # [Dragon]
    #         # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Now
    #         # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future Pokemon
    #         # ("KYUREM_WHITE_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
    #         # ("DRAMPA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("NECROZMA_ULTRA_FORM", "PSYCHO_CUT_FAST", "OUTRAGE"),
    #         # ("NAGANADEL", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DURALUDON", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGAPULT", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("ETERNATUS", "DRAGON_TAIL_FAST", "DRAGON_PULSE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future shadows
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
    #         # ("RESHIRAM_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future megas
    #         # ("GARCHOMP_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("CHARIZARD_MEGA_X", "DRAGON_BREATH_FAST", "OUTRAGE"),  # Better moves
    #         # ("CHARIZARD_MEGA_Y", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("EXEGGUTOR_ALOLA_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("EXEGGUTOR_ALOLA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("AMPHAROS_MEGA", "DRAGON_TAIL_FAST", "DRAGON_PULSE"),
    #         # ("AMPHAROS_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SCEPTILE_MEGA", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("SCEPTILE_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("ALTARIA_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("LATIOS_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("LATIOS_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("HAXORUS", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("HYDREIGON", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("KOMMO_O", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DURALUDON", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("ETERNATUS", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # # Signature moves (ignored because no moves are better than Outrage)
    #
    #         # [Dragon] For boss movesets
    #         # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Now
    #         # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Manually "fill blanks"
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("GARCHOMP", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("ZEKROM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future shadows
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
    #         # ("RESHIRAM_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future megas
    #         # ("GARCHOMP_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("HAXORUS", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #
    #         # [Electric]
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "FUSION_BOLT"),  # Future Pokemon
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "FUSION_BOLT"),
    #         # ("ZERAORA", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("ZERAORA", "VOLT_SWITCH_FAST", "THUNDERBOLT"),
    #         # ("REGIELEKI", "THUNDER_SHOCK_FAST", "ZAP_CANNON"),
    #         # ("JOLTEON_SHADOW_FORM", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),  # Future shadows
    #         # ("ZEKROM_SHADOW_FORM", "CHARGE_BEAM_FAST", "WILD_CHARGE"),
    #         # ("ZEKROM_SHADOW_FORM", "CHARGE_BEAM_FAST", "FUSION_BOLT"),
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "THUNDERBOLT"),  # Future megas
    #         # ("JOLTEON", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),  # Better regular moves
    #         # ("JOLTEON_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("ZAPDOS", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("AMPHAROS_MEGA", "VOLT_SWITCH_FAST", "THUNDERBOLT"),
    #         # ("AMPHAROS_MEGA", "VOLT_SWITCH_FAST", "WILD_CHARGE"),
    #         # ("LUXRAY", "THUNDER_FANG_FAST", "WILD_CHARGE"),
    #         # ("LUXRAY_SHADOW_FORM", "THUNDER_FANG_FAST", "WILD_CHARGE"),
    #         # ("ZEKROM", "THUNDER_FANG_FAST", "FUSION_BOLT"),
    #         # ("ZEKROM_SHADOW_FORM", "THUNDER_FANG_FAST", "FUSION_BOLT"),
    #         # ("THUNDURUS_THERIAN_FORM", "VOLT_SWITCH_FAST", "WILD_CHARGE"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),
    #         # ("VIKAVOLT", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("TAPU_KOKO", "VOLT_SWITCH_FAST", "WILD_CHARGE"),
    #         # ("REGIELEKI", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # Signature moves (ignored because no moves are significantly better than Wild Charge)
    #
    #         # [Fighting]
    #         # ("KELDEO", "LOW_KICK_FAST", "SACRED_SWORD"),  # Future Pokemon
    #         # ("KELDEO", "LOW_KICK_FAST", "SACRED_SWORD", "10/10/10"),
    #         # ("MELOETTA_PIROUETTE_FORM", "LOW_KICK_FAST", "CLOSE_COMBAT"),
    #         # ("HAWLUCHA", "LOW_KICK_FAST", "FLYING_PRESS"),
    #         # ("MARSHADOW", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("MARSHADOW", "COUNTER_FAST", "CLOSE_COMBAT"),
    #         # ("MARSHADOW", "LOW_KICK_FAST", "BRICK_BREAK"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("BRELOOM_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),  # Future shadows
    #         # ("LUCARIO_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("TERRAKION_SHADOW_FORM", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
    #         # ("MEWTWO_MEGA_X", "PSYCHO_CUT_FAST", "FOCUS_BLAST"),  # Future megas
    #         # ("BLAZIKEN_MEGA", "COUNTER_FAST", "FOCUS_BLAST"),
    #         # ("HERACROSS_MEGA", "COUNTER_FAST", "CLOSE_COMBAT"),
    #         # ("LUCARIO_MEGA", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("GALLADE_MEGA", "LOW_KICK_FAST", "CLOSE_COMBAT"),
    #         # ("HITMONLEE", "DOUBLE_KICK_FAST", "AURA_SPHERE"),  # Better regular moves
    #         # ("HITMONLEE_SHADOW_FORM", "DOUBLE_KICK_FAST", "AURA_SPHERE"),
    #         # ("MEWTWO", "LOW_KICK_FAST", "FOCUS_BLAST"),
    #         # ("MEWTWO_SHADOW_FORM", "LOW_KICK_FAST", "FOCUS_BLAST"),
    #         # ("MEWTWO_MEGA_X", "LOW_KICK_FAST", "FOCUS_BLAST"),
    #         # ("MEWTWO", "COUNTER_FAST", "FOCUS_BLAST"),
    #         # ("MEWTWO_SHADOW_FORM", "COUNTER_FAST", "FOCUS_BLAST"),
    #         # ("MEWTWO_MEGA_X", "COUNTER_FAST", "FOCUS_BLAST"),
    #         # ("MEWTWO", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("MEWTWO_SHADOW_FORM", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("MEWTWO_MEGA_X", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("MEWTWO", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("MEWTWO_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("MEWTWO_MEGA_X", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("BLAZIKEN", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("BLAZIKEN_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("BLAZIKEN_MEGA", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("GALLADE", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("GALLADE_SHADOW_FORM", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("GALLADE_MEGA", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("LOPUNNY_MEGA", "DOUBLE_KICK_FAST", "AURA_SPHERE"),
    #         # ("MIENSHAO", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("MIENSHAO_SHADOW_FORM", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("KELDEO", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
    #         # ("KELDEO", "DOUBLE_KICK_FAST", "SACRED_SWORD", "10/10/10"),
    #         # ("MELOETTA_PIROUETTE_FORM", "LOW_KICK_FAST", "FOCUS_BLAST"),
    #         # ("CRABOMINABLE", "ROCK_SMASH_FAST", "DYNAMIC_PUNCH"),
    #         # ("KOMMO_O", "COUNTER_FAST", "CLOSE_COMBAT"),
    #         # ("KOMMO_O", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("BUZZWOLE", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("ZAPDOS_GALARIAN_FORM", "COUNTER_FAST", "SUPER_POWER"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("SNEASLER", "COUNTER_FAST", "CLOSE_COMBAT"),
    #         # ("SNEASLER", "COUNTER_FAST", "FOCUS_BLAST"),
    #         # ("MACHAMP", "COUNTER_FAST", "SACRED_SWORD"),  # Signature moves
    #         # ("MACHAMP", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("MACHAMP_SHADOW_FORM", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("MACHAMP_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("CONKELDURR", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("CONKELDURR", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("SIRFETCHD", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("SIRFETCHD", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("ZAPDOS_GALARIAN_FORM", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("ZAPDOS_GALARIAN_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("HERACROSS", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("HERACROSS", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("HERACROSS_MEGA", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("HERACROSS_MEGA", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("HARIYAMA", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("HARIYAMA", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("HARIYAMA_SHADOW_FORM", "COUNTER_FAST", "SACRED_SWORD"),
    #         # ("HARIYAMA_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("PANGORO", "LOW_KICK_FAST", "SACRED_SWORD"),
    #         # ("PANGORO", "LOW_KICK_FAST", "AURA_SPHERE"),
    #
    #         # [Fire]
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "OVERHEAT"),  # Future Pokemon
    #         # ("BLACEPHALON", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("BLACEPHALON", "FIRE_SPIN_FAST", "FIRE_BLAST"),
    #         # ("DELPHOX", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("INCINEROAR", "FIRE_FANG_FAST", "BLAST_BURN"),
    #         # ("CINDERACE", "EMBER_FAST", "BLAST_BURN"),
    #         # ("DARMANITAN_ZEN_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "TACKLE_FAST", "OVERHEAT"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "OVERHEAT"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("VOLCANION", "INCINERATE_FAST", "OVERHEAT"),
    #         # ("KYUREM_WHITE_FORM", "DRAGON_BREATH_FAST", "FUSION_FLARE"),
    #         # ("KYUREM_WHITE_FORM", "STEEL_WING_FAST", "FUSION_FLARE"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "OVERHEAT"),  # Future megas
    #         # ("BLAZIKEN_MEGA", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("BLAZIKEN_MEGA", "COUNTER_FAST", "BLAST_BURN"),
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "FLAMETHROWER"),
    #         # ("BLAZIKEN_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),  # Future shadows
    #         # ("BLAZIKEN_SHADOW_FORM", "COUNTER_FAST", "BLAST_BURN"),
    #         # ("CHANDELURE_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("HEATRAN_SHADOW_FORM", "FIRE_SPIN_FAST", "FLAMETHROWER"),
    #         # ("EMBOAR_SHADOW_FORM", "EMBER_FAST", "BLAST_BURN"),
    #         # ("FLAREON_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("RESHIRAM_SHADOW_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("RESHIRAM_SHADOW_FORM", "FIRE_FANG_FAST", "FUSION_FLARE"),
    #         # ("HEATRAN", "FIRE_SPIN_FAST", "OVERHEAT"),  # Better moves
    #         # ("RESHIRAM", "FIRE_FANG_FAST", "BLAST_BURN"),  # Signature moves
    #         # ("HEATRAN", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("HEATRAN", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("CHANDELURE", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("CHANDELURE", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("BLACEPHALON", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("BLACEPHALON", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("ENTEI", "FIRE_FANG_FAST", "BLAST_BURN"),
    #         # ("ENTEI", "FIRE_FANG_FAST", "V_CREATE"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "BLAST_BURN"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "V_CREATE"),
    #         # ("ENTEI_SHADOW_FORM", "FIRE_FANG_FAST", "BLAST_BURN"),
    #         # ("ENTEI_SHADOW_FORM", "FIRE_FANG_FAST", "V_CREATE"),
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # GamePress only: Primal Groudon
    #
    #         # [Flying]
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "SKY_ATTACK"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "BRAVE_BIRD"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "AEROBLAST"),
    #         # ("RAYQUAZA", "AIR_SLASH_FAST", "SKY_ATTACK"),
    #         # ("RAYQUAZA", "AIR_SLASH_FAST", "FLY"),
    #         # ("RAYQUAZA", "AIR_SLASH_FAST", "BRAVE_BIRD"),
    #         # ("RAYQUAZA", "AIR_SLASH_FAST", "AEROBLAST"),
    #         # ("ARCHEOPS", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("ARCHEOPS_SHADOW_FORM", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #
    #         # [Grass]
    #         # ("CHESNAUGHT", "VINE_WHIP_FAST", "FRENZY_PLANT"),  # Future Pokemon
    #         # ("DECIDUEYE", "RAZOR_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("TSAREENA", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("RILLABOOM", "RAZOR_LEAF_FAST", "GRASS_KNOT"),
    #         # ("RILLABOOM", "RAZOR_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("SCEPTILE_SHADOW_FORM", "BULLET_SEED_FAST", "FRENZY_PLANT"),  # Future shadows
    #         # ("SCEPTILE_SHADOW_FORM", "FURY_CUTTER_FAST", "FRENZY_PLANT"),
    #         # ("ROSERADE_SHADOW_FORM", "RAZOR_LEAF_FAST", "GRASS_KNOT"),
    #         # ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "GRASS_KNOT"),
    #         # ("SCEPTILE_MEGA", "BULLET_SEED_FAST", "FRENZY_PLANT"),  # Future megas
    #         # ("SCEPTILE_MEGA", "FURY_CUTTER_FAST", "FRENZY_PLANT"),
    #         # ("SCEPTILE", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),  # Better regular moves
    #         # ("SCEPTILE_SHADOW_FORM", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("SCEPTILE_MEGA", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("ABOMASNOW_MEGA", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("VENUSAUR", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("VENUSAUR_SHADOW_FORM", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("VENUSAUR_MEGA", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("ROSERADE", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("ROSERADE_SHADOW_FORM", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("SHAYMIN_SKY_FORM", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("DECIDUEYE", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("ZARUDE", "MAGICAL_LEAF_FAST", "POWER_WHIP"),
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "GRASS_KNOT"),
    #         # ("TSAREENA", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),  # Signature moves
    #         # ("ZARUDE", "VINE_WHIP_FAST", "FRENZY_PLANT"),
    #
    #         # [Ground]
    #         # ("URSALUNA", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("URSALUNA", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
    #         # ("URSALUNA", "COUNTER_FAST", "HIGH_HORSEPOWER"),
    #         # ("URSALUNA_SHADOW_FORM", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("URSALUNA_SHADOW_FORM", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
    #         # ("URSALUNA_SHADOW_FORM", "COUNTER_FAST", "HIGH_HORSEPOWER"),
    #         # ("URSALUNA", "TACKLE_FAST", "EARTH_POWER"),
    #         # ("URSALUNA", "ROCK_SMASH_FAST", "EARTH_POWER"),
    #         # ("URSALUNA", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("URSALUNA", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("URSALUNA", "COUNTER_FAST", "EARTH_POWER"),
    #         # ("URSALUNA_SHADOW_FORM", "TACKLE_FAST", "EARTH_POWER"),
    #         # ("URSALUNA_SHADOW_FORM", "ROCK_SMASH_FAST", "EARTH_POWER"),
    #         # ("URSALUNA_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("URSALUNA_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("URSALUNA_SHADOW_FORM", "COUNTER_FAST", "EARTH_POWER"),
    #         # ("MAMOSWINE", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("MAMOSWINE_SHADOW_FORM", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("GOLURK_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("MUDSDALE", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("MUDSDALE", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("GROUDON", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("GROUDON", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
    #         # ("GARCHOMP_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("GARCHOMP_MEGA", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL", "METAL_CLAW_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SHOT_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "EARTH_POWER"),
    #         # ("RHYPERIOR", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("KROOKODILE", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("KROOKODILE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("KROOKODILE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("SWAMPERT", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("SWAMPERT_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("SWAMPERT_MEGA", "MUD_SHOT_FAST", "EARTHQUAKE"),
    #         # ("SWAMPERT_MEGA", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("CAMERUPT_MEGA", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "EARTH_POWER"),
    #         # ("CAMERUPT_MEGA", "ROCK_SMASH_FAST", "EARTH_POWER"),
    #         # ("CAMERUPT_MEGA", "EMBER_FAST", "EARTH_POWER"),
    #         # ("MAMOSWINE", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("MAMOSWINE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("LANDORUS_THERIAN_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("GOLEM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("GOLEM_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("STEELIX_MEGA", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("STEELIX_MEGA", "MUD_SLAP_FAST", "EARTH_POWER"),
    #
    #         # [Ice]
    #         # ("KYUREM", "DRAGON_BREATH_FAST", "GLACIATE"),  # Now
    #         # ("KYUREM", "STEEL_WING_FAST", "GLACIATE"),
    #         # ("AVALUGG_HISUIAN_FORM", "POWDER_SNOW_FAST", "BLIZZARD"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "BLIZZARD"),  # Future Pokemon
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "BLIZZARD"),
    #         # ("KYUREM_WHITE_FORM", "DRAGON_BREATH_FAST", "BLIZZARD"),
    #         # ("KYUREM_WHITE_FORM", "STEEL_WING_FAST", "BLIZZARD"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("FROSMOTH", "POWDER_SNOW_FAST", "ICE_BEAM"),
    #         # ("CALYREX_ICE_RIDER_FORM", "CONFUSION_FAST", "AVALANCHE"),
    #         # ("GLACEON_SHADOW_FORM", "FROST_BREATH_FAST", "AVALANCHE"),  # Future shadows
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "ICE_BEAM"),  # Future megas
    #         # ("KYUREM", "ICE_SHARD_FAST", "GLACIATE"),  # Better regular moves
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "ICE_BEAM"),
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "ICE_BEAM"),
    #         # ("KYUREM_BLACK_FORM", "ICE_SHARD_FAST", "BLIZZARD"),
    #         # ("KYUREM_BLACK_FORM", "ICE_SHARD_FAST", "ICE_BEAM"),
    #         # ("GLALIE_MEGA", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("ABOMASNOW_MEGA", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "AVALANCHE"),  # Signature moves
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "AVALANCHE"),
    #         # ("KYUREM_BLACK_FORM", "ICE_SHARD_FAST", "AVALANCHE"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "GLACIATE"),
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "GLACIATE"),
    #         # ("KYUREM_BLACK_FORM", "ICE_SHARD_FAST", "GLACIATE"),
    #         # ("AVALUGG_HISUIAN_FORM", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("AVALUGG_HISUIAN_FORM", "POWDER_SNOW_FAST", "GLACIATE"),
    #         # ("CRABOMINABLE", "FROST_BREATH_FAST", "AVALANCHE"),
    #         # ("CRABOMINABLE", "FROST_BREATH_FAST", "GLACIATE"),
    #         # ("CALYREX_ICE_RIDER_FORM", "CONFUSION_FAST", "GLACIATE"),
    #
    #         # [Ice Rock Electric]
    #         # ("WEAVILE", "ICE_SHARD_FAST", "AVALANCHE"),
    #         # ("GLACEON", "FROST_BREATH_FAST", "AVALANCHE"),
    #         # ("TYRANITAR", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #
    #         # [Psychic]
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "12/15/15"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "9/15/15"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "6/15/15"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "15/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "12/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "9/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "6/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "15/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "12/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "9/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "6/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "15/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "12/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "9/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE", "6/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "12/15/15"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "9/15/15"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "6/15/15"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "15/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "12/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "9/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "6/12/12"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "15/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "12/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "9/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "6/9/9"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "15/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "12/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "9/6/6"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "PSYSTRIKE", "6/6/6"),
    #         # ("NECROZMA_ULTRA_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("CALYREX_SHADOW_RIDER_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #
    #         # [Rock]
    #         # ("STONJOURNER", "ROCK_THROW_FAST", "ROCK_SLIDE"),  # Future Pokemon
    #         # ("STONJOURNER", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("STAKATAKA", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("STAKATAKA", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("STAKATAKA", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("RHYPERIOR_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_WRECKER"),  # Future shadows
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("GIGALITH_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("TERRAKION_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_MEGA", "SMACK_DOWN_FAST", "STONE_EDGE"),  # Future megas
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR", "SMACK_DOWN_FAST", "ROCK_SLIDE"),  # Better moves
    #         # ("TYRANITAR", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_SHADOW_FORM", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_MEGA", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_MEGA", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("RHYPERIOR", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("RHYPERIOR", "ROLLOUT_FAST", "ROCK_WRECKER"),
    #         # ("RHYPERIOR", "ROLLOUT_FAST", "METEOR_BEAM"),
    #         # ("RHYPERIOR_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("RHYPERIOR_SHADOW_FORM", "ROLLOUT_FAST", "ROCK_WRECKER"),
    #         # ("RHYPERIOR_SHADOW_FORM", "ROLLOUT_FAST", "METEOR_BEAM"),
    #         # ("ARCHEOPS", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("ARCHEOPS", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("AERODACTYL", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("AERODACTYL_SHADOW_FORM", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("AERODACTYL_MEGA", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("NIHILEGO", "POISON_JAB_FAST", "METEOR_BEAM"),
    #         # ("NIHILEGO", "ROCK_THROW_FAST", "ROCK_SLIDE"),  # ("Stealth Rock")
    #         # ("NIHILEGO", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("NIHILEGO", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("NIHILEGO", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("ARCANINE_HISUIAN_FORM", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("RAMPARDOS", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("RAMPARDOS", "SMACK_DOWN_FAST", "METEOR_BEAM"),  # Signature moves
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "ROCK_WRECKER"),  # (MB above)
    #         # ("LYCANROC_MIDDAY_FORM", "ROCK_THROW_FAST", "ROCK_WRECKER"),
    #         # ("LYCANROC_MIDDAY_FORM", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #
    #         # [Rock] for boss movesets
    #         # ("TYRANITAR", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #         # ("TYRANITAR_MEGA", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #         # ("RAMPARDOS", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("RHYPERIOR", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "STONE_EDGE", "10/10/10"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "STONE_EDGE", "5/5/5"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "STONE_EDGE", "0/0/0"),
    #
    #         # [Water]
    #         # ("GRENINJA", "BUBBLE_FAST", "HYDRO_CANNON"),  # Future Pokemon
    #         # ("VOLCANION", "WATER_GUN_FAST", "HYDRO_PUMP"),
    #         # ("PRIMARINA", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("WISHIWASHI_SCHOOL_FORM", "WATERFALL_FAST", "SURF"),
    #         # ("WISHIWASHI_SCHOOL_FORM", "WATERFALL_FAST", "HYDRO_PUMP"),
    #         # ("INTELEON", "WATER_GUN_FAST", "SURF"),
    #         # ("INTELEON", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # ("BARRASKEWDA", "WATERFALL_FAST", "AQUA_JET"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "WATERFALL_FAST", "AQUA_JET"),
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "SURF"),  # Future shadows
    #         # ("KINGLER_SHADOW_FORM", "BUBBLE_FAST", "CRABHAMMER"),
    #         # ("EMPOLEON_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("EMPOLEON_SHADOW_FORM", "METAL_CLAW_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_SHADOW_FORM", "FURY_CUTTER_FAST", "HYDRO_CANNON"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "AQUA_TAIL"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "HYDRO_PUMP"),
    #         # ("SWAMPERT_MEGA", "WATER_GUN_FAST", "HYDRO_CANNON"),  # Future megas
    #         # ("SWAMPERT_MEGA", "MUD_SHOT_FAST", "HYDRO_CANNON"),
    #         # ("SHARPEDO_MEGA", "WATERFALL_FAST", "HYDRO_PUMP"),
    #         # ("SLOWBRO_MEGA", "WATER_GUN_FAST", "SURF"),  # Better regular moves
    #         # ("GYARADOS", "WATERFALL_FAST", "SURF"),
    #         # ("GYARADOS_SHADOW_FORM", "WATERFALL_FAST", "SURF"),
    #         # ("GYARADOS_MEGA", "WATERFALL_FAST", "SURF"),
    #         # ("SHARPEDO", "WATERFALL_FAST", "SURF"),
    #         # ("SHARPEDO_SHADOW_FORM", "WATERFALL_FAST", "SURF"),
    #         # ("SHARPEDO_MEGA", "WATERFALL_FAST", "SURF"),
    #         # ("PALKIA", "WATERFALL_FAST", "AQUA_TAIL"),
    #         # ("PALKIA", "WATERFALL_FAST", "HYDRO_PUMP"),
    #         # ("PALKIA", "WATERFALL_FAST", "SURF"),
    #         # ("PALKIA_SHADOW_FORM", "WATERFALL_FAST", "AQUA_TAIL"),
    #         # ("PALKIA_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_PUMP"),
    #         # ("PALKIA_SHADOW_FORM", "WATERFALL_FAST", "SURF"),
    #         # ("BARRASKEWDA", "WATERFALL_FAST", "SURF"),
    #         # ("KYOGRE", "WATERFALL_FAST", "ORIGIN_PULSE"),  # Signature moves
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "ORIGIN_PULSE"),
    #         # ("KYOGRE", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("VOLCANION", "WATER_GUN_FAST", "CRABHAMMER"),
    #         # ("VOLCANION", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "WATERFALL_FAST", "CRABHAMMER"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #
    #     ],
    # },

    # Below is for the utility metric
    {
        "Min level": 40,
        "Max level": 40,
        "Level step size": 5,
        "Must be non mega": True,
        "Exclude": ["LUCARIO_MEGA", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "MEWTWO_MEGA_X", "MEWTWO_MEGA_Y",
                    "CALYREX_SHADOW_RIDER_FORM", "BLACEPHALON", "ETERNATUS", "ETERNATUS_ETERNAMAX_FORM"],
            # Specific Pokemon to be excluded,
            # in the same format as "Pokemon code names", e.g. "VENUSAUR_SHADOW_FORM"
    },
    {
        "Min level": 40,
        "Max level": 40,
        "Level step size": 5,
        "Must be non mega": True,  # Just in case I screw up and have a mega in there
        "Pokemon code names and moves": [
            # All future shadows, shadow legendaries, and top non-shadows (e.g. bug Volcarona)
            # Does not include speculative moves (yet)
            # [Bug]
            ("VOLCARONA", "BUG_BITE_FAST", "BUG_BUZZ"),
            ("VOLCARONA_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),
            ("YANMEGA_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),
            # [Dark/Ghost]
            ("BLACEPHALON", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            ("GENGAR_SHADOW_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            ("CHANDELURE_SHADOW_FORM", "HEX_FAST", "SHADOW_BALL"),
            ("HYDREIGON_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "DARK_PULSE"),
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "SHADOW_BALL"),
            # [Dragon]
            ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
            ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
            ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
            ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
            ("RESHIRAM_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
            ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
            # [Electric]
            ("ZEKROM_SHADOW_FORM", "CHARGE_BEAM_FAST", "FUSION_BOLT"),
            ("ZEKROM_SHADOW_FORM", "CHARGE_BEAM_FAST", "WILD_CHARGE"),
            # [Fighting]
            ("LUCARIO_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
            ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            ("TERRAKION_SHADOW_FORM", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
            # [Fire]
            ("VOLCARONA", "FIRE_SPIN_FAST", "OVERHEAT"),  # Future Pokemon
            ("BLACEPHALON", "FIRE_SPIN_FAST", "OVERHEAT"),
            ("BLAZIKEN_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),  # Future shadows
            ("BLAZIKEN_SHADOW_FORM", "COUNTER_FAST", "BLAST_BURN"),
            ("CHANDELURE_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
            ("HEATRAN_SHADOW_FORM", "FIRE_SPIN_FAST", "FLAMETHROWER"),
            ("RESHIRAM_SHADOW_FORM", "FIRE_FANG_FAST", "FUSION_FLARE"),
            # [Flying]
            ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE"),
            ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE"),
            # [Grass]
            ("SCEPTILE_SHADOW_FORM", "BULLET_SEED_FAST", "FRENZY_PLANT"),
            ("ROSERADE_SHADOW_FORM", "RAZOR_LEAF_FAST", "GRASS_KNOT"),
            ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "GRASS_KNOT"),
            # [Ground]
            ("GROUDON", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
            ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
            ("GARCHOMP_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
            ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "DRILL_RUN"),
            ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # [Ice]
            ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "AVALANCHE"),
            # [Poison]
            ("GENGAR_SHADOW_FORM", "LICK_FAST", "SLUDGE_BOMB"),
            ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            ("NAGANADEL", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            ("ETERNATUS", "POISON_JAB_FAST", "CROSS_POISON"),
            # [Psychic]
            ("NECROZMA_ULTRA_FORM", "CONFUSION_FAST", "PSYCHIC"),
            ("CALYREX_SHADOW_RIDER_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # [Rock]
            ("RHYPERIOR_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
            ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            ("TERRAKION_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            # [Steel]
            ("DIALGA_SHADOW_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),
            # [Water]
            ("INTELEON", "WATER_GUN_FAST", "HYDRO_CANNON"),
            ("KYOGRE", "WATERFALL_FAST", "ORIGIN_PULSE"),
            ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "ORIGIN_PULSE"),
            ("KINGLER_SHADOW_FORM", "BUBBLE_FAST", "CRABHAMMER"),
            ("EMPOLEON_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
            ("SAMUROTT_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "AQUA_TAIL"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "HYDRO_PUMP"),

            # [Speculative moves]
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
            ("ZEKROM_SHADOW_FORM", "THUNDER_FANG_FAST", "FUSION_BOLT"),
            ("ZEKROM_SHADOW_FORM", "THUNDER_FANG_FAST", "WILD_CHARGE"),
            ("HEATRAN_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
            ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "SKY_ATTACK"),
        ]
    }

    # Replacing unnerfed megas on Pokebattler
    # {
    #     "Min level": 25,  # Unnerfed 25 = Nerfed 30
    #     "Max level": 25,
    #     "Level step size": 5,
    #     "Pokemon code names and moves": [
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    #     ],
    # },
    # {
    #     "Min level": 27.5,  # Unnerfed 27.5 = Nerfed 35
    #     "Max level": 27.5,
    #     "Level step size": 5,
    #     "Pokemon code names and moves": [
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    #     ],
    # },
    # {
    #     "Min level": 29.5,  # Unnerfed 29.5 = Nerfed 40
    #     "Max level": 29.5,
    #     "Level step size": 5,
    #     "Pokemon code names and moves": [
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    #     ],
    # },
    # {
    #     "Min level": 32.5,  # Unnerfed 32.5 = Nerfed 45
    #     "Max level": 32.5,
    #     "Level step size": 5,
    #     "Pokemon code names and moves": [
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    #     ],
    # },
    # {
    #     "Min level": 36.5,  # Unnerfed 36.5 = Nerfed 50
    #     "Max level": 36.5,
    #     "Level step size": 5,
    #     "Pokemon code names and moves": [
    #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    #     ],
    # },

    # Add more {} blocks here if needed
    # {
    #     "Charged move types": ["Ice"],
    #     "Min level": 40,
    #     "Max level": 50,
    #     "Level step size": 10,
    # },
]

CONFIG_RAID_BOSS_ENSEMBLE = [
    # Lists of raid bosses you want to use.
    # You can specify several groups, each group enclosed by a {} with the format shown below.
    # Each group starts with a pool of Pokemon, which can be one of the following:
    # - "All Pokemon": All Pokemon in Game Master. (Gen 1-6 & 8, except Honedge line and Zygarde)
    #                  You will need to specify the "Raid tier" field to specify which tier they are. (Default: T3)
    # - "All Pokemon except above": All Pokemon, except those already listed in groups above.
    # - "By raid tier": All bosses of a certain tier, including past, present and future.
    #                   You will need to specify the "Raid tier" field,
    #                   e.g. "Raid tier": "Tier 5" - All past/present/future T5s (except Meloetta)
    # - "By raid category": All bosses listed under a certain category in Pokebattler.
    #                       You will need to specify the "Raid category" field,
    #                       e.g. "Raid category": "Legacy Tier 5", or "Tier 5" - current bosses only
    #
    # After choosing the group, you can then apply filters to select certain Pokemon from them.
    # All filters that are currently supported are listed below.
    # To use them, delete the first # at the start of the line, and then change the value as you wish.
    # To drop them, add back the # at the start of the line.
    #
    # Each raid boss in the ensemble is given a weight, which describes its importance in the evaluation
    # of attackers.
    # For example, if T5 Kyogre has a weight of 5 and T5 Skarmory has a weight of 1, then an attacker's
    # performance against T5 Kyogre is 5 times more important than against T3 Skarmory.
    # Use "Weight of each Pokemon" to give all Pokemon here a constant weight (default: 1).
    # Use "Weight of whole group" if you want the entire {} block to have a certain total weight, overriding
    # individual weights. (E.g. If you want all T5s to have a total of 50 and all T3s a total of 10.)
    # (If you don't want to do that, add a # at the start of the line.)
    #
    # "Forms weight strategy" allows you to change how different forms of the same raid boss gets weights,
    # such as Arceus, Giratina and Landorus:
    # - "combine" (default option): All forms combined are considered a single Pokemon, and each form splits the weight.
    #   (e.g. Each Arceus form has weight 1/18.)
    # - "separate": Each form is considered as a separate Pokemon and weighed accordingly.
    #   (e.g. Each Arceus form has weight 1, all Arceus combined are 18 times as important as another boss.)
    # Note that shadows, megas, Alolans and Galarians are always considered separate Pokemon.
    # Currently there's no way to change that.
    #
    # You can specify specific battle settings for each group listed here (e.g. Best Friends for T5s,
    # No Friend for T3s). Use the "Battle settings" key, and write all settings as a dict （in a {} block)
    # just like CONFIG_BATTLE_SETTINGS.
    # If not specified, CONFIG_BATTLE_SETTINGS will be used.
    #
    # ----- End of documentation for this section -----

    # [For testing]
    # {
    #     "Pokemon pool": "By raid category",
    #     "Raid categories": ["Tier 5", "Ultra Beast Tier", "Mega Tier"],  # Here, "Tier 5" has only current bosses
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",  # "combine" or "separate"
    #     # "Filters": {  # Only those without # at the start are applied
    #     #     "Weak to contender types": ["Dragon"],
    #     # }
    # },

    {
        "Pokemon pool": "By raid tier",  # "All Pokemon", "All Pokemon except above", "By raid tier" or "By raid category"
        "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier"],  # Here, "Tier 5" has all past/present/future bosses
        #"Raid category": "Ultra Beast Tier",  # Here, "Tier 5" has only current bosses
        # "Filters": {  # Only those without # at the start are applied
        #     #"Weak to contender types": SINGLE_TYPE_ATTACKER,
        #     #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        #     get_ensemble_weak_key(): get_move_types(),
        #     #"Evolution stage": "Final",  # "Final", "Pre-evolution"
        #     #"Must be shadow": False,  # This describes BOSSES, not attackers
        #     #"Must be non shadow": True,
        #     #"Must be mega": False,
        #     #"Must be non mega": True,
        #     #"Must be legendary": False,
        #     #"Must be non legendary": False,
        #     #"Must be mythical": False,
        #     #"Must be non mythical": False,
        #     #"Must be legendary or mythical": False,
        #     #"Must be non legendary or mythical": False,
        #     # TODO: Add a filter for ignoring certain Pokemon or raids, identified by user
        # },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 65, #50,
        "Forms weight strategy": "combine",  # "combine" or "separate"
        # "Battle settings": {  # Write group-specific battle settings, in the same format as CONFIG_BATTLE_SETTINGS
        #     # If absent, CONFIG_BATTLE_SETTINGS will be used
        #     "Friendship": "Best",
        #     "Weather": "Extreme",
        #     "Attack strategy": "No Dodging",
        #     "Dodge strategy": "Realistic Dodging"
        # },
        # "Baseline battle settings": {
        #     "Weather": "Extreme",
        #     "Friendship": "Best",
        #     "Attack strategy": "No Dodging",
        #     "Dodge strategy": "Realistic Dodging",
        # }
    },
    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier"],
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Attack strategy": "Dodge Specials PRO",
    #     },
    # },
    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier"],
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Weather": "Sunny",
    #     },
    # },

    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
        # "Filters": {
        #     #"Weak to contender types": SINGLE_TYPE_ATTACKER,
        #     #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        #     get_ensemble_weak_key(): get_move_types(),
        # },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 35,  #25,
        "Forms weight strategy": "combine",
    },
    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Attack strategy": "Dodge Specials PRO",
    #     },
    # },
    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Weather": "Sunny",
    #     },
    # },

    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tier": "Tier 3",
    #     # "Filters": {
    #     #     #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #     #     #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #     #     get_ensemble_weak_key(): get_move_types(),
    #     # },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 15,  #25,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Friendship": "Not",
    #     },
    #     "Baseline battle settings": {
    #         "Friendship": "Not",
    #     }
    # },
    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tier": "Tier 3",
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Friendship": "Not",
    #         "Attack strategy": "Dodge Specials PRO",
    #     },
    #     "Baseline battle settings": {
    #         "Friendship": "Not",
    #     }
    # },
    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tier": "Tier 3",
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Friendship": "Not",
    #         "Weather": "Sunny",
    #     },
    #     "Baseline battle settings": {
    #         "Friendship": "Not",
    #     }
    # },

    # {
    #     "Pokemon pool": "All Pokemon except above",
    #     "Raid tier": "Tier 3",
    #     # "Raid category": "Legacy Tier 5",
    #     "Filters": {
    #         "Weak to contender types": ["Grass"],
    #         "Evolution stage": "Final",  # "Final", "Pre-evolution"
    #         "Must be non shadow": True,
    #         "Must be non mega": True,
    #         "Must be non legendary or mythical": True,  # Ignores Glastrier etc
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 10,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Friendship": "Not",
    #     },
    # },
]

CONFIG_ESTIMATOR_SCALING_SETTINGS = {
    # Estimator Scaling: Estimators of different attackers against a particular boss are typically
    # scaled before their averages across bosses are taken.
    # A "baseline" is chosen - typically the best attacker, whose estimator will be scaled to 1.0.
    # All other estimators will be scaled proportionally.
    # These settings allow you to enable or disable scaling and choose the baseline.
    #
    # Example: Against Terrakion with random moveset, Mewtwo has estimator 1.64, Kyogre 2.10, Empoleon 2.19.
    # Suppose we're analyzing water attackers. If scaling is not enabled, 2.10 and 2.19 will be used for averages.
    # If "Baseline chosen before filter" is True, the best attacker before filtering attackers by type,
    # Mewtwo (1.64), will become the baseline.
    # Mewtwo's estimator is scaled to 1.0, Kyogre 2.10/1.64=1.28, Empoleon 2.19/1.64=1.34.
    # If "Baseline chosen before filter" is False, AFTER filtering attackers by type (AttackerCriteria),
    # the best attacker, Kyogre (2.10), will become the baseline.
    # Kyogre's estimator is scaled to 1.0, and Empoleon 2.19/2.10=1.04.
    #
    # Why is scaling useful? This is primarily to standardize the absolute size of estimators against
    # various bosses, allowing them to carry equivalent weight when averages are taken.
    # With no scaling, harder bosses like Lugia and Deoxys-D, which often have estimators above 3,
    # will have disproportionally greater impact on the average estimators of attackers.
    # In other words, an attacker that does particularly well against Lugia will be overestimated.
    # This is also why the "Baseline chosen before filter" is necessary, to make sure comparisons
    # of attackers of one type (water) don't become skewed by better attackers from other types (Mewtwo).
    #
    # [Baseline boss moveset]
    #
    # "Baseline boss moveset" can be either "random", "easiest" or "hardest".
    # The best attacker against this particular moveset (aka. the smallest estimator value), either
    # before or after filtering, will be used as the baseline.
    # Here, "easiest" is defined as the moveset for which the minimum estimator is obtained.
    #
    # Example: T5 Reshiram, no shadows/megas, no attacker filtering.
    # With random moveset, Rhyperior is #1, estimator 2.26.
    # With DB/DM, Dialga is #1, estimator 2.36. This is the largest #1 estimator for any Reshiram moveset.
    # With FF/Crunch, Rayquaza is #1, estimator 2.07. This is the smallest #1 estimator for any Reshiram moveset.
    # Baseline chosen with each option: "random" - 2.26, "easiest" - 2.07, "hardest" - 2.36.
    # Note that once a baseline is chosen, it will be consistent across all boss movesets. For example,
    # if set to "easiest", then all attackers against random moveset will have estimator at least 2.26/2.07=1.09.
    #
    # In practice, two options for "Baseline boss moveset" have merit and can be used accordingly:
    # - random: This allows the best attacker to consistently have estimator 1.0 for best comparison across bosses.
    #           It also gives an easy way to check the difficulty of a boss moveset (below or above 1.0).
    # - easiest: This gives greater importance to bosses with "hard" movesets, which are often coverages
    #            against its counters. If even the best attacker takes a huge hit (like Rayquaza against
    #            dragons), its scaled estimator against random moveset will be above 1.0. Thus, this raid boss
    #            will matter more when taking averages across bosses.
    #            The averages will then favor attackers who perform more consistently against bosses and movesets,
    #            like Dialga, by giving greater weight to bosses where its gap with Rayquaza is smaller.
    #            Example: T5 Palkia. Rayquaza's random estimator is 2.27, but only 1.98 against DT/AT.
    #            With "Easiest", Rayquaza's scaled estimator will become 1.14. The fact that it's significantly
    #            above 1.0 suggests T5 Palkia is a hard boss with a troublesome worst-case moveset.
    #
    # [Baseline attacker level]
    #
    # If you have multiple attacker levels, "Baseline attacker level" allows you to choose a standard level
    # to determine a baseline, and apply the same baseline to attackers of all levels.
    # Possible options include: A specific level, "min" (minimum level across all attackers), "max",
    # "average" (average level across all attackers).
    # To turn this feature off, set it to "by level", -1 or None.
    # Default is "by level" or turned off.
    #
    # Note: If the raid uses Trainers' Pokebox, "min", "max" and "average" are chosen using the by-level
    # simulations of this raid boss with current battle settings (not baseline battle settings).
    # e.g. If simulating Dialga raids in extreme weather with L30-50 and cloudy weather with L40 and Pokebox,
    # when "min" is used, the baseline attacker level is 40, even for attackers from the Pokebox in cloudy.
    #
    # Example: Suppose against a particular boss, L40 Zekrom's estimator is 2.0 and L50 is 1.75.
    # Without a standard baseline attacker level, both will be chosen as the baseline for all L40 attackers
    # and L50 attackers respectively, thus both are scaled to 1.0.
    # With baseline attacker level at 40, L40 Zekrom will be scaled to 1.0, and L50 Zekrom will be scaled
    # to 1.75/2=0.875.
    #
    # [Baseline battle settings]
    #
    # Similar to baseline attacker level, but for a standard battle setting.
    # Specified as a dict similar to CONFIG_BATTLE_SETTINGS. Multiple options in any fields are not allowed.
    #
    # Practical usages: Specifying baseline weather conditions or dodge settings, to compare the improvement
    # of weather boost or dodging.
    # In this case, the best attacker with dodging may be scaled to below 1.0.
    #
    # This field can be overridden in each RaidEnsemble with its own baseline battle settings (as long as that
    # battle settings is being run somewhere).
    # Example: Suppose the raid ensembles are T5 raids (BF, no dodging), T5 raids (BF, dodging), T3 raids
    # (NF, no dodging), T3 raids (NF, dodging).
    # We want to use BF as the baseline battle settings for both T5s, and NF for both T3s.
    # In this case, the baseline settings for T3s can be specified in CONFIG_RAID_BOSS_ENSEMBLE.
    #
    # While this dict supports multiple sets of settings (multiple values for each parameter), a singular value
    # is strongly suggested (i.e. only one baseline), so that only one baseline exists for estimator scaling.
    # Currently, if the baseline BS for a single boss consists of multiple sets, they will be matched with the
    # corresponding multiple battle settings for that boss (wrap around) - see CountersListsMultiBSLevel.
    # For multiple baselines, consider using CONFIG_RAID_BOSS_ENSEMBLE.
    #
    # (Technical note: Unlike the other baseline items here, baseline battle settings are pushed directly
    # to each RaidEnsemble object, just like each raid's battle settings.)
    #
    # ----- End of documentation for this section -----

    "Enabled": False,  # Default: True
    "Baseline chosen before filter": False,  # Default: False
    "Baseline boss moveset": "random",  # "random", "easiest", "hardest"
    "Baseline attacker level": 40,  # Specific level, "min", "max", "average", "by level"/-1/None
    "Baseline battle settings": {
        "Weather": "Extreme",
        "Friendship": "Best",
        "Attack strategy": "No Dodging",
        "Dodge strategy": "Realistic Dodging",
    },
    "Consider required attackers": True,  # Default: False
}


CONFIG_PROCESSING_SETTINGS = {
    # TODO: Documentation
    # "Write lists for each boss unfiltered": False,
    # "Write lists for each boss filtered": False,
    # Other options for write_CSV_list to be included

    # CSV table settings
    "Include unscaled estimators": False,  # Default: False
    "Combine attacker movesets": False,  # Combine attacker moves (e.g. FS/BB and Counter/BB Blaziken), Default: True
    "Combine attacker fast moves": True,  # Combine attacker fast moves but not charged moves, Default: False
    "Include random boss movesets": True,  # Default: True
    "Include specific boss movesets": False,  # Default: False
    "Assign weights to specific boss movesets": False,  # Default: False
    "Include attacker IVs": False,  # Default: False
    "Include fast move type": True,  # Default: False
    "Include charged move type": True,  # Default: False
    "Fill blanks": False,  # Default: True

    "Attackers that should not be combined": [  # Will not combine these attackers' different movesets,
        # displaying each moveset separately. (Remember to INCLUDE SHADOWS & MEGAS separately here!!!)
        # "STARAPTOR", "STARAPTOR_SHADOW_FORM",
        #"BEEDRILL_MEGA", # Bug Bite legacy
        #"ALAKAZAM_MEGA", "ALAKAZAM", "ALAKAZAM_SHADOW_FORM",  # Psychic legacy

        #"VIKAVOLT", "GOLISOPOD",
        #"GENGAR", "GENGAR_MEGA", "ETERNATUS", "SALAZZLE", "SNEASLER", "GENGAR_SHADOW_FORM",
        #"TOGEKISS", "FLORGES", "TAPU_KOKO", "SYLVEON", "XERNEAS", "DIANCIE_MEGA"
        #"ALAKAZAM_MEGA", "ALAKAZAM", "ALAKAZAM_SHADOW_FORM", "NECROZMA_DAWN_WINGS_FORM", "NECROZMA_DUSK_MANE_FORM", "NECROZMA_ULTRA_FORM"

        # [Dark/Ghost]
        # "LUNALA", "MARSHADOW", "BLACEPHALON", "TYRANITAR", "TYRANITAR_SHADOW_FORM", "TYRANITAR_MEGA", "ABSOL",
        # "ABSOL_SHADOW_FORM", "ABSOL_MEGA", "KROOKODILE", "GRENINJA", "INCINEROAR", "ZARUDE", "DARKRAI", "ZOROARK",
        # "PANGORO", "HOOPA_UNBOUND_FORM", "GRIMMSNARL", "URSHIFU_SINGLE_STRIKE_FORM", "CALYREX_SHADOW_RIDER_FORM",
        # "GYARADOS_MEGA", "GIRATINA_ORIGIN_FORM", "DECIDUEYE", "DARKRAI_SHADOW_FORM",
        # "HONCHKROW", "HONCHKROW_SHADOW_FORM",
        #"SABLEYE_MEGA",

        # [Dragon]
        # "SALAMENCE", "SALAMENCE_SHADOW_FORM", "SALAMENCE_MEGA",  # For Salamence article analysis purposes only
        # "DRAGONITE", "DRAGONITE_SHADOW_FORM",  # For research purposes only (with all movesets turned on)
        # "GYARADOS_MEGA",  # Dragon Tail is exclusive
        # "CHARIZARD_MEGA_X", "CHARIZARD_MEGA_Y", "EXEGGUTOR_ALOLA_FORM", "EXEGGUTOR_ALOLA_SHADOW_FORM", "AMPHAROS_MEGA",
        # "SCEPTILE_MEGA", "ALTARIA_MEGA", "LATIOS_SHADOW_FORM", "LATIOS_MEGA", "DIALGA", "DIALGA_SHADOW_FORM",
        # "PALKIA", "PALKIA_SHADOW_FORM", "HAXORUS", "HAXORUS_SHADOW_FORM", "HYDREIGON", "HYDREIGON_SHADOW_FORM",
        # "KOMMO_O", "DURALUDON", "ETERNATUS",

        # [Electric]
        # "ZERAORA", "ZEKROM", "ZEKROM_SHADOW_FORM", "JOLTEON", "JOLTEON_SHADOW_FORM", "ZAPDOS", "ZAPDOS_SHADOW_FORM",
        # "AMPHAROS_MEGA", "LUXRAY", "LUXRAY_SHADOW_FORM", "THUNDURUS_THERIAN_FORM", "XURKITREE", "VIKAVOLT", "TAPU_KOKO",
        # "REGIELEKI",

        # [Fire]
        # "BLACEPHALON", "DARMANITAN_GALARIAN_ZEN_FORM", "RESHIRAM", "HEATRAN", "CHANDELURE", "ENTEI", "SALAZZLE",
        # "CAMERUPT_MEGA", "ENTEI_SHADOW_FORM", "VOLCARONA", "RESHIRAM_SHADOW_FORM",

        # [Fighting]
        # "MARSHADOW", "HITMONLEE", "HITMONLEE_SHADOW_FORM", "MEWTWO", "MEWTWO_SHADOW_FORM", "MEWTWO_MEGA_X",
        # "BLAZIKEN", "BLAZIKEN_SHADOW_FORM", "BLAZIKEN_MEGA", "GALLADE", "GALLADE_SHADOW_FORM", "GALLADE_MEGA",
        # "LOPUNNY_MEGA", "MIENSHAO", "KELDEO", "MELOETTA_PIROUETTE_FORM", "KOMMO_O", "BUZZWOLE", "ZAPDOS_GALARIAN_FORM",
        # "URSHIFU_SINGLE_STRIKE_FORM", "URSHIFU_RAPID_STRIKE_FORM", "SNEASLER", "MACHAMP", "MACHAMP_SHADOW_FORM",
        # "CONKELDURR", "CONKELDURR_SHADOW_FORM", "SIRFETCHD", "ZAPDOS_GALARIAN_FORM", "HERACROSS", "HERACROSS_MEGA",
        # "HARIYAMA", "HARIYAMA_SHADOW_FORM", "PANGORO",

        # [Grass]
        # "CHESNAUGHT", "DECIDUEYE", "ABOMASNOW_MEGA", "SCEPTILE", "VENUSAUR_MEGA", "RILLABOOM", "ROSERADE",
        # "ROSERADE_SHADOW_FORM", "SCEPTILE_SHADOW_FORM", "SCEPTILE_MEGA", "VENUSAUR_SHADOW_FORM", "SHAYMIN_SKY_FORM",
        # "ZARUDE", "TSAREENA", "VENUSAUR",

        # [Ground]
        # "URSALUNA", "URSALUNA_SHADOW_FORM", "MUDSDALE", "GROUDON", "GROUDON_SHADOW_FORM", "EXCADRILL", "RHYPERIOR",
        # "KROOKODILE", "KROOKODILE_SHADOW_FORM", "SWAMPERT", "SWAMPERT_SHADOW_FORM", "SWAMPERT_MEGA", "CAMERUPT_MEGA",
        # "MAMOSWINE", "MAMOSWINE_SHADOW_FORM", "LANDORUS_THERIAN_FORM", "GOLEM", "GOLEM_SHADOW_FORM", "STEELIX_MEGA",
        # "EXCADRILL_SHADOW_FORM", "RHYPERIOR_SHADOW_FORM",

        # [Ice]
        # "KYUREM", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "GLALIE_MEGA", "ABOMASNOW_MEGA", "AVALUGG_HISUIAN_FORM",
        # "CRABOMINABLE", "CALYREX_ICE_RIDER_FORM",

        # [Rock]
        # "RHYPERIOR",  # Also for beginners (Stone Edge), even without MB speculation
        # "RHYPERIOR_SHADOW_FORM", "ARCHEOPS", "AERODACTYL", "AERODACTYL_SHADOW_FORM", "AERODACTYL_MEGA",
        # "STONJOURNER", "STAKATAKA", "DIANCIE_MEGA", "TYRANITAR", "TYRANITAR_SHADOW_FORM", "TYRANITAR_MEGA",
        # "NIHILEGO", "ARCANINE_HISUIAN_FORM", "RAMPARDOS", "RAMPARDOS_SHADOW_FORM", "LYCANROC_MIDDAY_FORM",
        # Obsolete: "OMASTAR", "OMASTAR_SHADOW_FORM", "GOLEM_SHADOW_FORM", "GOLEM", "GOLEM_ALOLA_FORM",

        # [Steel]
        # "AGGRON_MEGA", "SOLGALEO", "NECROZMA_DUSK_MANE_FORM", "LUCARIO", "LUCARIO_MEGA", "GENESECT", "SCIZOR",
        # "SCIZOR_MEGA", "DIALGA", "EXCADRILL", "MELMETAL",
        
        # [Water]
        # "FERALIGATR", "FERALIGATR_SHADOW_FORM",  # Water Gun is exclusive
        # "KYOGRE", "KYOGRE_SHADOW_FORM", "GRENINJA", "PRIMARINA", "INTELEON", "PALKIA", "PALKIA_SHADOW_FORM",
        # "VOLCANION", "WISHIWASHI_SCHOOL_FORM", "BARRASKEWDA", "URSHIFU_RAPID_STRIKE_FORM", "SHARPEDO",
        # "SHARPEDO_SHADOW_FORM", "SHARPEDO_MEGA", "SLOWBRO_MEGA", "GYARADOS", "GYARADOS_SHADOW_FORM", "GYARADOS_MEGA",

        # "MEWTWO_SHADOW_FORM"
        # "RAYQUAZA", "RAYQUAZA_SHADOW_FORM",

        # [Utility Metric]
        "ZEKROM_SHADOW_FORM",  # Thunder Fang
    ],
}
