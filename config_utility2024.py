"""
Configurations for running the script to generate plots and CSVs.

For convenience, this file stores (or will store) several pre-made "types" of configurations,
so that you don't have to change everything whenever you want to run something different.
"""

from params import *


TEMPORARY_MEGA_FIX = False  # Whether to turn off megas from default attacker criteria
TEMPORARY_FRIENDSHIP_DEFAULT = "Not"

#CONFIG_WRITE_ALL_COUNTERS = True

SINGLE_TYPE_ATTACKER = ["Fire"]
MULTI_TYPE_ATTACKERS_COMPARE = ["Fairy", "Dragon"]  # Use this for Dark/Ghost
# Ground/Steel, Ground/Fire, Ground/Fighting, Ground/Water/Rock, Water/Steel, Water/Grass
EXTRA_TYPE_ATTACKER = ["Psychic", "Fire", "Water", "Electric"]  # Attacker types that use non-STAB moves, doesn't apply to moves
    # Bug: Grass (Kartana)
    # Dark/Ghost: Psychic (Mewtwo, Mega Alakazam)
    # Dragon: Fire, Water (Mega Charizard Y, Mega Gyarados)
    # Electric: Psychic, Water (Mewtwo, Primal Kyogre)
    # Fairy: Electric, Psychic, Ice (Xurkitree, Mega Alakazam, Lunala, Beartic)
    # Fighting: Psychic (Mega Alakazam)
    # Fire: Psychic (Mewtwo)
    # Grass: Electric, Ground (Xurkitree, Primal Groudon)
    # Ice: Psychic, Water (Mewtwo, Mega Gardevoir, Primal Kyogre)
    # Poison: Dark (Darkrai)
    # Rock: Ground (Landorus-I RT/RS)
MODE = "MULTI+"  # SINGLE, SINGLE+, MULTI, MULTI+  (Use MULTI+ for DARK GHOST)

#CONFIG_SORT_OPTION = "Estimator"
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
    # "Friendship": "Best",  # Not Friend, New Friend, Good Friend, Great Friend, Ultra Friend, Best Friend (can omit "Friend")
                           # Default: Best Friend
    "Friendship": TEMPORARY_FRIENDSHIP_DEFAULT,  # TEMPORARY
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
    #         #     ("GARCHOMP_MEGA", "MUD_SHOT_FAST", "EARTH_POWER", "10\\10\\10"),
    #         #     ("SCIZOR_MEGA", "FURY_CUTTER_FAST", "X_SCISSOR", "15\\15\\15", True),  # True = Participate in estimator scaling
    #         #     ...
    #         # ]
    #         # This DOES guarantee the required Pokemon will be on the counters list.
    #         # Use this option if you want to test unreleased Pokemon or movesets, or Pokemon that are too weak
    #         # to appear on any of the top 32 lists.
    #
    #         # Use 4 args if you want to specify IVs.
    #         # Use 5 args if you want to specify whether this attacker participates in estimator scaling,
    #         # overriding "Consider required attackers" in CONFIG_ESTIMATOR_SCALING_SETTINGS
    #         # (If you want to specify this, MUST give IVs)
    #
    #     # "Trainer ID": 52719,  # Pokebattler trainer ID
    #     #                       # If this is provided, only Pokemon from that Trainer's Pokebox are used
    #     # "Must be shadow": False,  # This describes attackers, not bosses
    #     # "Must be non shadow": True,
    #     # "Must be mega": True,
    #     "Must be non mega": TEMPORARY_MEGA_FIX,
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
    #                 "CALYREX_SHADOW_RIDER_FORM", "BLACEPHALON", "ETERNATUS", "ETERNATUS_ETERNAMAX_FORM",
    #                 "PALKIA_SHADOW_FORM", "RESHIRAM_SHADOW_FORM", "ZEKROM_SHADOW_FORM", "KYUREM_SHADOW_FORM",
    #                 "TERRAKION_SHADOW_FORM"],
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
    #         # [Bug]
    #         # ("BEEDRILL_MEGA", "BUG_BITE_FAST", "X_SCISSOR", "15\\15\\15", True),  # Megas (force to participate in scaling)
    #         # ("BEEDRILL_MEGA", "INFESTATION_FAST", "X_SCISSOR", "15\\15\\15", True),
    #         # ("BEEDRILL_MEGA", "POISON_JAB_FAST", "X_SCISSOR", "15\\15\\15", True),
    #         # ("SCIZOR_MEGA", "BULLET_PUNCH_FAST", "X_SCISSOR", "15\\15\\15", True),
    #         # ("SCIZOR_MEGA", "FURY_CUTTER_FAST", "X_SCISSOR", "15\\15\\15", True),
    #         # ("VOLCARONA", "BUG_BITE_FAST", "BUG_BUZZ"),  # Now
    #         # ("KLEAVOR", "QUICK_ATTACK_FAST", "X_SCISSOR"),
    #         # ("KLEAVOR", "AIR_SLASH_FAST", "X_SCISSOR"),
    #         # ("PINSIR_MEGA", "BUG_BITE_FAST", "X_SCISSOR"),
    #         # ("PINSIR_MEGA", "FURY_CUTTER_FAST", "X_SCISSOR"),
    #         # ("CENTISKORCH", "BUG_BITE_FAST", "BUG_BUZZ"),  # Future Pokemon
    #         # ("FROSMOTH", "BUG_BITE_FAST", "BUG_BUZZ"),
    #         # ("YANMEGA_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),  # Future shadows
    #         # ("HERACROSS_MEGA", "STRUGGLE_BUG_FAST", "MEGAHORN"),  # Future megas
    #         # ("HERACROSS_MEGA", "COUNTER_FAST", "MEGAHORN"),
    #         # ("VIKAVOLT", "BUG_BITE_FAST", "BUG_BUZZ"),  # Better moves
    #         # ("GOLISOPOD", "FURY_CUTTER_FAST", "BUG_BUZZ"),
    #         # ("HERACROSS", "STRUGGLE_BUG_FAST", "BUG_BUZZ"),
    #         # ("HERACROSS", "COUNTER_FAST", "BUG_BUZZ"),
    #         # ("HERACROSS_MEGA", "STRUGGLE_BUG_FAST", "BUG_BUZZ"),
    #         # ("HERACROSS_MEGA", "COUNTER_FAST", "BUG_BUZZ"),
    #         # ("GENESECT", "FURY_CUTTER_FAST", "BUG_BUZZ"),
    #         # ("SCIZOR", "FURY_CUTTER_FAST", "BUG_BUZZ"),
    #         # ("SCIZOR_SHADOW_FORM", "FURY_CUTTER_FAST", "BUG_BUZZ"),
    #         # ("SCIZOR_MEGA", "FURY_CUTTER_FAST", "BUG_BUZZ"),
    #         # ("KLEAVOR", "FURY_CUTTER_FAST", "X_SCISSOR"),
    #         # ("KLEAVOR", "FURY_CUTTER_FAST", "BUG_BUZZ"),
    #         # Signature moves
    #
    #         # [Bug] Comparisons
    #         # ("VOLCARONA", "BUG_BITE_FAST", "BUG_BUZZ"),  # Now
    #         # ("KLEAVOR", "QUICK_ATTACK_FAST", "X_SCISSOR"),
    #         # ("KLEAVOR", "AIR_SLASH_FAST", "X_SCISSOR"),
    #         # ("PINSIR_MEGA", "BUG_BITE_FAST", "X_SCISSOR"),
    #         # ("PINSIR_MEGA", "FURY_CUTTER_FAST", "X_SCISSOR"),
    #         # ("PHEROMOSA", "BUG_BITE_FAST", "BUG_BUZZ"),
    #         # ("PINSIR_SHADOW_FORM", "BUG_BITE_FAST", "X_SCISSOR"),
    #         # ("PINSIR_SHADOW_FORM", "FURY_CUTTER_FAST", "X_SCISSOR"),
    #         # ("SCIZOR_SHADOW_FORM", "FURY_CUTTER_FAST", "X_SCISSOR"),
    #
    #         # [Bug Dark Ghost] Comparisons
    #         # ("CHANDELURE", "HEX_FAST", "SHADOW_BALL"),
    #         # ("GHOLDENGO", "HEX_FAST", "SHADOW_BALL"),
    #         # ("HYDREIGON", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "CRUNCH"),
    #         # ("HYDREIGON", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("WEAVILE_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("DARKRAI", "SNARL_FAST", "DARK_PULSE"),
    #         # ("DARKRAI", "SNARL_FAST", "SHADOW_BALL"),
    #         # ("GIRATINA_ORIGIN_FORM", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
    #
    #         # [Dark Ghost]  TODO: Add Gen 9 mons
    #         # ("TYPHLOSION_HISUIAN_FORM", "HEX_FAST", "SHADOW_BALL"),  # Now
    #         # ("DHELMISE", "SHADOW_CLAW_FAST", "SHADOW_BALL"),  # Future Pokemon
    #         # ("MARSHADOW", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
    #         # ("MARSHADOW", "SHADOW_CLAW_FAST", "SHADOW_PUNCH"),
    #         # ("MARSHADOW", "ASTONISH_FAST", "SHADOW_BALL"),
    #         # ("BLACEPHALON", "ASTONISH_FAST", "SHADOW_BALL"),
    #         # ("POLTEAGEIST", "HEX_FAST", "SHADOW_BALL"),
    #         # ("GRIMMSNARL", "BITE_FAST", "FOUL_PLAY"),
    #         # ("GRIMMSNARL", "SUCKER_PUNCH_FAST", "FOUL_PLAY"),
    #         # ("CURSOLA", "HEX_FAST", "SHADOW_BALL"),
    #         # ("DRAGAPULT", "HEX_FAST", "SHADOW_BALL"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "SUCKER_PUNCH_FAST", "PAYBACK"),
    #         # ("CALYREX_SHADOW_RIDER_FORM", "CONFUSION_FAST", "SHADOW_BALL"),  # (Spectrier no fast move)
    #         # ("KINGAMBIT", "SNARL_FAST", "DARK_PULSE"),
    #         # ("CHIENPAO", "SNARL_FAST", "DARK_PULSE"),
    #         # ("CHIYU", "SNARL_FAST", "DARK_PULSE"),
    #         # ("FLUTTERMANE", "HEX_FAST", "SHADOW_BALL"),  # (TODO: The rest of Gen 9 has not been added)
    #         # ("FLUTTERMANE", "ASTONISH_FAST", "SHADOW_BALL"),
    #         # ("GENGAR_SHADOW_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),  # Future shadows
    #         # ("GENGAR_SHADOW_FORM", "LICK_FAST", "SHADOW_BALL"),
    #         # ("CHANDELURE_SHADOW_FORM", "HEX_FAST", "SHADOW_BALL"),
    #         # ("HYDREIGON_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "DARK_PULSE"),
    #         # ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "SHADOW_BALL"),
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),  # Future megas
    #         # ("SHARPEDO_MEGA", "BITE_FAST", "CRUNCH"),  # (Mega Sableye ignored due to low power)
    #         # ("TYRANITAR", "SNARL_FAST", "BRUTAL_SWING"),  # Better moves
    #         # ("TYRANITAR_SHADOW_FORM", "SNARL_FAST", "BRUTAL_SWING"),
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
    #         # ("CHIENPAO", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("CHIYU", "SNARL_FAST", "BRUTAL_SWING"),
    #         # ("NECROZMA_DAWN_WINGS_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),  # Signature moves (Ghost) (Most of them already have Shadow Ball elsewhere)
    #         # # ("MARSHADOW", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
    #         # # ("CALYREX_SHADOW_RIDER_FORM", "HEX_FAST", "SHADOW_FORCE"),
    #
    #         # [DarkGhost] for boss movesets
    #         # ("TYRANITAR", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR", "SMACK_DOWN_FAST", "BRUTAL_SWING"),
    #         # ("HYDREIGON", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("WEAVILE_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
    #         # ("DARKRAI", "SNARL_FAST", "DARK_PULSE"),
    #         # ("DARKRAI", "SNARL_FAST", "SHADOW_BALL"),
    #         # ("GIRATINA_ORIGIN_FORM", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
    #         # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "BRUTAL_SWING"),
    #         # ("GENGAR_SHADOW_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
    #         # ("GENGAR_SHADOW_FORM", "LICK_FAST", "SHADOW_BALL"),
    #         # ("GENGAR_SHADOW_FORM", "HEX_FAST", "SHADOW_BALL"),
    #         # ("CHANDELURE_SHADOW_FORM", "HEX_FAST", "SHADOW_BALL"),
    #
    #         # [Dragon]
    #         # ("KYUREM", "DRAGON_BREATH_FAST", "GLACIATE"),  # PERMANENT!!!!
    #         # ("BAXCALIBUR", "ICE_FANG_FAST", "AVALANCHE"),  # PERMANENT!!!!
    #         # ("BAXCALIBUR", "DRAGON_BREATH_FAST", "AVALANCHE"),  # PERMANENT!!!!
    #         # ("DIALGA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),  # Now
    #         # ("DIALGA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),  # (In case of last-minute moveset changes)
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "SPACIAL_REND"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "6\\6\\6"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE", "6\\6\\6"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future Pokemon
    #         # ("KYUREM_WHITE_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
    #         # ("DRAMPA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("NECROZMA_ULTRA_FORM", "PSYCHO_CUT_FAST", "OUTRAGE"),
    #         # ("DURALUDON", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGAPULT", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("ETERNATUS", "DRAGON_TAIL_FAST", "DRAGON_PULSE"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "SPACIAL_REND"),  # (I think they will happen, but seemingly not Sinnoh Tour)
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("KORAIDON", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("KORAIDON", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("MIRAIDON", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future shadows
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
    #         # ("RESHIRAM_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("GARCHOMP_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Future megas
    #         # ("CHARIZARD_MEGA_X", "DRAGON_BREATH_FAST", "OUTRAGE"),  # Better moves
    #         # ("CHARIZARD_MEGA_X", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("CHARIZARD_MEGA_Y", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("CHARIZARD_MEGA_Y", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("EXEGGUTOR_ALOLA_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("EXEGGUTOR_ALOLA_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("EXEGGUTOR_ALOLA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("EXEGGUTOR_ALOLA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("DRAGONITE", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("AMPHAROS_MEGA", "DRAGON_TAIL_FAST", "DRAGON_PULSE"),
    #         # ("AMPHAROS_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SCEPTILE_MEGA", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # # ("SCEPTILE_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("ALTARIA_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # # ("SALAMENCE", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("LATIOS_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("LATIOS_SHADOW_FORM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("LATIOS_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("LATIOS_MEGA", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # # ("GARCHOMP", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("GARCHOMP_MEGA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("DIALGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # # ("DIALGA", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # # ("PALKIA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # # ("PALKIA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("HYDREIGON", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("HYDREIGON", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("RESHIRAM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("RESHIRAM_SHADOW_FORM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("ZEKROM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "BREAKING_SWIPE"),
    #         # ("KOMMO_O", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DURALUDON", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("ETERNATUS", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("GARCHOMP", "DRAGON_TAIL_FAST", "SPACIAL_REND"),  # Signature moves
    #         # ("GARCHOMP", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("GARCHOMP_MEGA", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("GARCHOMP_MEGA", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("EXEGGUTOR_ALOLA_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("EXEGGUTOR_ALOLA_FORM", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("EXEGGUTOR_ALOLA_SHADOW_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("EXEGGUTOR_ALOLA_SHADOW_FORM", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("KOMMO_O", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("KOMMO_O", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("DRAGAPULT", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DRAGAPULT", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("ETERNATUS", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("ETERNATUS", "DRAGON_TAIL_FAST", "ROAR_OF_TIME"),
    #         # ("BAXCALIBUR", "DRAGON_BREATH_FAST", "SPACIAL_REND"),
    #         # ("BAXCALIBUR", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #
    #         # [Dragon] For boss movesets
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "6\\6\\6"),
    #         # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE", "6\\6\\6"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
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
    #         # ("HAXORUS", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE_MEGA", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #
    #         # [Dragon] Custom IVs
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "14\\14\\4"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "14\\8\\15"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "11\\14\\15"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "12\\12\\15"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "15\\12\\5"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "11\\14\\11"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "14\\10\\6"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE", "15\\4\\10"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW", "11\\14\\11"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW", "14\\10\\6"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW", "15\\4\\10"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #
    #         # [Electric]
    #         # ("THUNDURUS_THERIAN_FORM", "VOLT_SWITCH_FAST", "WILDBOLT_STORM"),  # Now
    #         # ("THUNDURUS_INCARNATE_FORM", "THUNDER_SHOCK_FAST", "WILDBOLT_STORM"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "FUSION_BOLT"),  # Future Pokemon
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "FUSION_BOLT"),
    #         # ("ZERAORA", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("ZERAORA", "VOLT_SWITCH_FAST", "WILD_CHARGE"),
    #         # ("MIRAIDON", "THUNDER_SHOCK_FAST", "THUNDER"),
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
    #         # ("MIRAIDON", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),  # Signature moves
    #         # ("MIRAIDON", "THUNDER_SHOCK_FAST", "FUSION_BOLT"),
    #         # ("MIRAIDON", "THUNDER_SHOCK_FAST", "WILDBOLT_STORM"),
    #         # ("ZERAORA", "SPARK_FAST", "FUSION_BOLT"),
    #         # ("ZERAORA", "SPARK_FAST", "WILDBOLT_STORM"),
    #
    #         # [Electric] For boss movesets
    #         # ("RAIKOU_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("RAIKOU_SHADOW_FORM", "VOLT_SWITCH_FAST", "WILD_CHARGE"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "ZAP_CANNON"),
    #         # ("ELECTIVIRE_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("MAGNEZONE_SHADOW_FORM", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("MAGNEZONE_SHADOW_FORM", "VOLT_SWITCH_FAST", "WILD_CHARGE"),
    #         # ("MAGNEZONE_SHADOW_FORM", "CHARGE_BEAM_FAST", "WILD_CHARGE"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "DISCHARGE"),
    #         # ("XURKITREE", "SPARK_FAST", "DISCHARGE"),
    #         # ("ZEKROM", "CHARGE_BEAM_FAST", "FUSION_BOLT"),
    #         # ("ZEKROM", "CHARGE_BEAM_FAST", "WILD_CHARGE"),
    #         # ("THUNDURUS_THERIAN_FORM", "VOLT_SWITCH_FAST", "WILDBOLT_STORM"),
    #         # ("RAIKOU_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE", "10\\10\\10"),
    #         # ("RAIKOU_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE", "11\\11\\11"),
    #         # ("RAIKOU_SHADOW_FORM", "VOLT_SWITCH_FAST", "WILD_CHARGE", "10\\10\\10"),
    #         # ("RAIKOU_SHADOW_FORM", "VOLT_SWITCH_FAST", "WILD_CHARGE", "11\\11\\11"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "THUNDERBOLT", "10\\10\\10"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "THUNDERBOLT", "11\\11\\11"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "ZAP_CANNON", "10\\10\\10"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "ZAP_CANNON", "11\\11\\11"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "DISCHARGE", "13\\13\\13"),
    #         # ("XURKITREE", "SPARK_FAST", "DISCHARGE", "13\\13\\13"),
    #
    #         # [Fairy]
    #         # ("TOGEKISS", "CHARM_FAST", "AURA_SPHERE"),  # PERMANENT!!!!
    #         # ("XERNEAS", "GEOMANCY_FAST", "MOONBLAST"),  # Now
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "MOONBLAST"),
    #         # ("DIANCIE_MEGA", "TACKLE_FAST", "MOONBLAST"),
    #         # ("MAGEARNA", "LOCK_ON_FAST", "PLAY_ROUGH"),  # Future Pokemon
    #         # ("HATTERENE", "CHARM_FAST", "DAZZLING_GLEAM"),  # (Ignores Grimmsnarl due to no fast move and mediocre stats)
    #         # ("ALCREMIE", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "METAL_CLAW_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "SNARL_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "QUICK_ATTACK_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "FIRE_FANG_FAST", "PLAY_ROUGH"),
    #         # ("IRONVALIANT", "FURY_CUTTER_FAST", "DAZZLING_GLEAM"),  # (TODO: The rest of Gen 9 has not been added)
    #         # ("IRONVALIANT", "PSYCHO_CUT_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "LOW_KICK_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "CHARGE_BEAM_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "FURY_CUTTER_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "PSYCHO_CUT_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "LOW_KICK_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "CHARGE_BEAM_FAST", "MOONBLAST"),
    #         # ("FLUTTERMANE", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("FLUTTERMANE", "CHARM_FAST", "MOONBLAST"),
    #         # ("TOGEKISS_SHADOW_FORM", "CHARM_FAST", "DAZZLING_GLEAM"),  # Future shadows
    #         # ("TOGEKISS_SHADOW_FORM", "CHARM_FAST", "AURA_SPHERE"),  # Future shadows
    #         # ("MAWILE_MEGA", "FAIRY_WIND_FAST", "PLAY_ROUGH"),  # Future megas
    #         # ("TOGEKISS", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),  # Better moves
    #         # ("TOGEKISS", "FAIRY_WIND_FAST", "AURA_SPHERE"),
    #         # ("TOGEKISS_SHADOW_FORM", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS_SHADOW_FORM", "FAIRY_WIND_FAST", "AURA_SPHERE"),
    #         # ("FLORGES", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("SYLVEON", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("XERNEAS", "GEOMANCY_FAST", "PLAY_ROUGH"),
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "PLAY_ROUGH"),
    #         # ("DIANCIE_MEGA", "TACKLE_FAST", "PLAY_ROUGH"),
    #         # ("DIANCIE_MEGA", "CHARM_FAST", "MOONBLAST"),
    #         # ("DIANCIE_MEGA", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("PRIMARINA", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("TAPU_KOKO", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("TAPU_KOKO", "GEOMANCY_FAST", "DAZZLING_GLEAM"),
    #         # ("TAPU_LELE", "CHARM_FAST", "MOONBLAST"),
    #         # ("TAPU_LELE", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TAPU_LELE", "FAIRY_WIND_FAST", "MOONBLAST"),  # Hypothetical fast moves
    #         # ("TAPU_LELE", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("TAPU_LELE", "GEOMANCY_FAST", "MOONBLAST"),
    #         # ("TAPU_LELE", "GEOMANCY_FAST", "DAZZLING_GLEAM"),
    #         # ("TAPU_BULU", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("TAPU_BULU", "GEOMANCY_FAST", "DAZZLING_GLEAM"),
    #         # ("MAGEARNA", "FAIRY_WIND_FAST", "PLAY_ROUGH"),
    #         # ("MAGEARNA", "GEOMANCY_FAST", "PLAY_ROUGH"),
    #         # ("GRIMMSNARL", "FAIRY_WIND_FAST", "PLAY_ROUGH"),
    #         # ("GRIMMSNARL", "GEOMANCY_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "FAIRY_WIND_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "GEOMANCY_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "FAIRY_WIND_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "GEOMANCY_FAST", "PLAY_ROUGH"),
    #         # ("IRONVALIANT", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "FAIRY_WIND_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "GEOMANCY_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "GEOMANCY_FAST", "MOONBLAST"),
    #
    #         # [Fairy] For boss movesets
    #         # ("XERNEAS", "GEOMANCY_FAST", "MOONBLAST"),
    #         # ("GARDEVOIR", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("GARDEVOIR_SHADOW_FORM", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS", "CHARM_FAST", "AURA_SPHERE"),  # Now
    #         # ("ZACIAN", "METAL_CLAW_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "SNARL_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "QUICK_ATTACK_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "FIRE_FANG_FAST", "PLAY_ROUGH"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "DAZZLING_GLEAM"),
    #         # ("GRANBULL", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("GRANBULL_SHADOW_FORM", "CHARM_FAST", "PLAY_ROUGH"),
    #
    #         # [Fairy vs Dragon] Filling blanks
    #         # ("XERNEAS", "GEOMANCY_FAST", "MOONBLAST"),
    #         # ("XERNEAS", "GEOMANCY_FAST", "PLAY_ROUGH"),  # Hypothetical
    #         # ("GARDEVOIR", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("GARDEVOIR_SHADOW_FORM", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS", "CHARM_FAST", "AURA_SPHERE"),
    #         # ("ZACIAN", "METAL_CLAW_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "SNARL_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "QUICK_ATTACK_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "FIRE_FANG_FAST", "PLAY_ROUGH"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "DAZZLING_GLEAM"),
    #         # ("GRANBULL", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("GRANBULL_SHADOW_FORM", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("SALAMENCE", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("GARCHOMP", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("ZEKROM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("HAXORUS", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("IRONVALIANT", "FURY_CUTTER_FAST", "DAZZLING_GLEAM"),  # (TODO: The rest of Gen 9 has not been added)
    #         # ("IRONVALIANT", "PSYCHO_CUT_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "LOW_KICK_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "CHARGE_BEAM_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "FURY_CUTTER_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "PSYCHO_CUT_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "LOW_KICK_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "CHARGE_BEAM_FAST", "MOONBLAST"),
    #         # ("FLUTTERMANE", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("FLUTTERMANE", "CHARM_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "FAIRY_WIND_FAST", "MOONBLAST"),
    #         # ("IRONVALIANT", "GEOMANCY_FAST", "DAZZLING_GLEAM"),
    #         # ("IRONVALIANT", "GEOMANCY_FAST", "MOONBLAST"),
    #
    #         # [Fairy vs Fighting] Filling blanks
    #         # ("GARDEVOIR", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("GARDEVOIR_SHADOW_FORM", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("GARDEVOIR_MEGA", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS", "CHARM_FAST", "DAZZLING_GLEAM"),
    #         # ("TOGEKISS", "CHARM_FAST", "AURA_SPHERE"),  # Now
    #         # ("ZACIAN", "METAL_CLAW_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "SNARL_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "QUICK_ATTACK_FAST", "PLAY_ROUGH"),
    #         # ("ZACIAN", "FIRE_FANG_FAST", "PLAY_ROUGH"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "DAZZLING_GLEAM"),
    #         # ("GRANBULL", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("GRANBULL_SHADOW_FORM", "CHARM_FAST", "PLAY_ROUGH"),
    #         # ("TERRAKION", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
    #         # ("MACHAMP_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("HARIYAMA_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("CONKELDURR", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("LUCARIO", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("MACHAMP", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("BRELOOM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("HARIYAMA", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("BLAZIKEN_MEGA", "COUNTER_FAST", "FOCUS_BLAST"),
    #
    #         # [Fighting]
    #         # ("MELOETTA_PIROUETTE_FORM", "LOW_KICK_FAST", "CLOSE_COMBAT"),  # Future Pokemon (missing Paldea)
    #         # ("HAWLUCHA", "LOW_KICK_FAST", "FLYING_PRESS"),
    #         # ("MARSHADOW", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("MARSHADOW", "COUNTER_FAST", "CLOSE_COMBAT"),
    #         # ("MARSHADOW", "LOW_KICK_FAST", "BRICK_BREAK"),
    #         # ("URSHIFU_SINGLE_STRIKE_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("KORAIDON", "ROCK_SMASH_FAST", "CLOSE_COMBAT"),
    #         # ("DECIDUEYE_HISUIAN_FORM", "PSYCHO_CUT_FAST", "AURA_SPHERE"),
    #         # ("DECIDUEYE_HISUIAN_FORM", "MAGICAL_LEAF_FAST", "AURA_SPHERE"),
    #         # ("IRONVALIANT", "LOW_KICK_FAST", "AURA_SPHERE"),  # (TODO: The rest of Gen 9 has not been added)
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
    #         # ("GALLADE", "LOW_KICK_FAST", "SACRED_SWORD"),
    #         # ("GALLADE_SHADOW_FORM", "LOW_KICK_FAST", "SACRED_SWORD"),
    #         # ("GALLADE_MEGA", "LOW_KICK_FAST", "SACRED_SWORD"),
    #         # ("LOPUNNY_MEGA", "DOUBLE_KICK_FAST", "AURA_SPHERE"),
    #         # ("MIENSHAO", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("MIENSHAO_SHADOW_FORM", "LOW_KICK_FAST", "AURA_SPHERE"),
    #         # ("KELDEO", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
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
    #         # ("DECIDUEYE_HISUIAN_FORM", "LOW_KICK_FAST", "AURA_SPHERE"),
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
    #         # ("KORAIDON", "ROCK_SMASH_FAST", "SACRED_SWORD"),
    #         # ("KORAIDON", "ROCK_SMASH_FAST", "AURA_SPHERE"),
    #
    #         # [Fighting] For boss movesets
    #         # ("CONKELDURR", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("LUCARIO", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("HARIYAMA_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
    #         # ("LUCARIO_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
    #         # ("TERRAKION", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
    #
    #         # [Fire]
    #         # ("TYPHLOSION_HISUIAN_FORM", "EMBER_FAST", "OVERHEAT"),  # (in case not added to Pokebattler yet)
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE_PLUS"),  # Now
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE"),
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE", "11\\11\\11"),
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE", "6\\6\\6"),
    #         # ("INFERNAPE_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("BLACEPHALON", "INCINERATE_FAST", "MYSTICAL_FIRE"),  # Future Pokemon
    #         # ("BLACEPHALON", "INCINERATE_FAST", "OVERHEAT"),
    #         # ("INCINEROAR", "FIRE_FANG_FAST", "BLAST_BURN"),
    #         # ("CINDERACE", "EMBER_FAST", "BLAST_BURN"),
    #         # ("SKELEDIRGE", "INCINERATE_FAST", "BLAST_BURN"),
    #         # ("TYPHLOSION_HISUIAN_FORM", "EMBER_FAST", "BLAST_BURN"),
    #         # ("DARMANITAN_ZEN_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "TACKLE_FAST", "OVERHEAT"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "OVERHEAT"),
    #         # ("VOLCANION", "INCINERATE_FAST", "OVERHEAT"),
    #         # ("KYUREM_WHITE_FORM", "DRAGON_BREATH_FAST", "FUSION_FLARE"),
    #         # ("KYUREM_WHITE_FORM", "STEEL_WING_FAST", "FUSION_FLARE"),
    #         # ("ARMAROUGE", "INCINERATE_FAST", "FLAMETHROWER"),
    #         # ("CERULEDGE", "INCINERATE_FAST", "FLAMETHROWER"),
    #         # # ("SCOVILLAIN", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("CHIYU", "INCINERATE_FAST", "FLAME_CHARGE"),
    #         # ("CHIYU", "INCINERATE_FAST", "FLAME_WHEEL"),
    #         # ("IRONMOTH", "FIRE_SPIN_FAST", "OVERHEAT"),  # (TODO: The rest of Gen 9 has not been added)
    #         # ("IRONMOTH", "EMBER_FAST", "FLAMETHROWER"),
    #         # ("HEATRAN_SHADOW_FORM", "FIRE_SPIN_FAST", "MAGMA_STORM"),  # Future shadows
    #         # ("EMBOAR_SHADOW_FORM", "EMBER_FAST", "BLAST_BURN"),
    #         # ("FLAREON_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("RESHIRAM_SHADOW_FORM", "FIRE_FANG_FAST", "FUSION_FLARE"),
    #         # ("VOLCARONA_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "OVERHEAT"),  # Future megas
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "FLAMETHROWER"),
    #         # ("GROUDON_PRIMAL", "MUD_SHOT_FAST", "OVERHEAT"),  # Better regular moves
    #         # ("GROUDON_PRIMAL", "DRAGON_TAIL_FAST", "OVERHEAT"),
    #         # ("GROUDON_PRIMAL", "INCINERATE_FAST", "FIRE_BLAST"),
    #         # ("GROUDON_PRIMAL", "INCINERATE_FAST", "FIRE_PUNCH"),
    #         # ("GROUDON_PRIMAL", "INCINERATE_FAST", "OVERHEAT"),
    #         # ("GROUDON_PRIMAL", "FIRE_FANG_FAST", "FIRE_BLAST"),
    #         # ("GROUDON_PRIMAL", "FIRE_FANG_FAST", "FIRE_PUNCH"),
    #         # ("GROUDON_PRIMAL", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("CHANDELURE", "FIRE_SPIN_FAST", "MYSTICAL_FIRE"),
    #         # ("DARMANITAN", "FIRE_FANG_FAST", "MYSTICAL_FIRE"),
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "MYSTICAL_FIRE"),
    #         # ("MOLTRES", "FIRE_SPIN_FAST", "MYSTICAL_FIRE"),
    #         # ("MOLTRES_SHADOW_FORM", "FIRE_SPIN_FAST", "MYSTICAL_FIRE"),
    #         # ("CHANDELURE", "FIRE_SPIN_FAST", "BLAST_BURN"),  # Signature moves
    #         # ("CHANDELURE", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("CHANDELURE_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("CHANDELURE_SHADOW_FORM", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("BLACEPHALON", "INCINERATE_FAST", "BLAST_BURN"),
    #         # ("BLACEPHALON", "INCINERATE_FAST", "V_CREATE"),
    #         # ("ENTEI", "FIRE_FANG_FAST", "BLAST_BURN"),
    #         # ("ENTEI", "FIRE_FANG_FAST", "V_CREATE"),
    #         # ("ENTEI_SHADOW_FORM", "FIRE_FANG_FAST", "BLAST_BURN"),
    #         # ("ENTEI_SHADOW_FORM", "FIRE_FANG_FAST", "V_CREATE"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "BLAST_BURN"),
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "V_CREATE"),
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("VOLCARONA_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("VOLCARONA_SHADOW_FORM", "FIRE_SPIN_FAST", "V_CREATE"),
    #         # ("IRONMOTH", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("IRONMOTH", "FIRE_SPIN_FAST", "V_CREATE"),
    #
    #         # [Fire] For boss movesets
    #         # ("CHANDELURE_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("HEATRAN_SHADOW_FORM", "FIRE_SPIN_FAST", "MAGMA_STORM"),
    #         # ("VOLCARONA_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("RESHIRAM", "FIRE_FANG_FAST", "FUSION_FLARE"),
    #         # ("RESHIRAM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("MOLTRES_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("MOLTRES_SHADOW_FORM", "WING_ATTACK_FAST", "OVERHEAT"),
    #         # ("ENTEI_SHADOW_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE_PLUS"),
    #         # ("BLAZIKEN_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("BLAZIKEN_SHADOW_FORM", "COUNTER_FAST", "BLAST_BURN"),
    #         # ("BLAZIKEN_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAZE_KICK"),
    #         # ("BLAZIKEN_SHADOW_FORM", "COUNTER_FAST", "BLAZE_KICK"),
    #
    #         # ("CHANDELURE", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("VOLCARONA", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # # Darmanitan
    #         # ("MOLTRES", "FIRE_SPIN_FAST", "OVERHEAT"),
    #         # ("MOLTRES", "WING_ATTACK_FAST", "OVERHEAT"),
    #         # ("ENTEI", "FIRE_FANG_FAST", "OVERHEAT"),
    #         # ("BLAZIKEN", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("BLAZIKEN", "COUNTER_FAST", "BLAST_BURN"),
    #         # ("BLAZIKEN", "FIRE_SPIN_FAST", "BLAZE_KICK"),
    #         # ("BLAZIKEN", "COUNTER_FAST", "BLAZE_KICK"),
    #         # ("TYPHLOSION_HISUIAN_FORM", "EMBER_FAST", "BLAST_BURN"),
    #         # ("DELPHOX", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #         # ("EMBOAR", "EMBER_FAST", "BLAST_BURN"),
    #         # ("CHARIZARD", "FIRE_SPIN_FAST", "BLAST_BURN"),
    #
    #         # [Flying]
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "DRAGON_ASCENT"),  # Now
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "DRAGON_ASCENT", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE", "11\\11\\11"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "DRAGON_ASCENT", "6\\6\\6"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE", "6\\6\\6"),
    #         # ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE", "6\\6\\6"),
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "BRAVE_BIRD"),
    #         # ("HO_OH_SHADOW_FORM", "EXTRASENSORY_FAST", "BRAVE_BIRD"),
    #         # ("HO_OH_SHADOW_FORM", "HIDDEN_POWER_FLYING_FAST", "BRAVE_BIRD"),
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "BRAVE_BIRD", "11\\11\\11"),
    #         # ("HO_OH_SHADOW_FORM", "EXTRASENSORY_FAST", "BRAVE_BIRD", "11\\11\\11"),
    #         # ("HO_OH_SHADOW_FORM", "HIDDEN_POWER_FLYING_FAST", "BRAVE_BIRD", "11\\11\\11"),
    #         # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "BRAVE_BIRD", "6\\6\\6"),
    #         # ("HO_OH_SHADOW_FORM", "EXTRASENSORY_FAST", "BRAVE_BIRD", "6\\6\\6"),
    #         # ("HO_OH_SHADOW_FORM", "HIDDEN_POWER_FLYING_FAST", "BRAVE_BIRD", "6\\6\\6"),
    #         # ("FLAMIGO", "WING_ATTACK_FAST", "BRAVE_BIRD"),  # Future Pokemon
    #         # ("YANMEGA_SHADOW_FORM", "WING_ATTACK_FAST", "AERIAL_ACE"),  # Future shadows
    #         # ("BRAVIARY_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("TOGEKISS_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # # Future megas
    #         # ("SALAMENCE", "AIR_SLASH_FAST", "FLY"),  # Better moves
    #         # ("SALAMENCE", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("SALAMENCE", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("SALAMENCE_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("SALAMENCE_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("SALAMENCE_SHADOW_FORM", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("SALAMENCE_MEGA", "AIR_SLASH_FAST", "FLY"),
    #         # ("SALAMENCE_MEGA", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("SALAMENCE_MEGA", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("AERODACTYL", "WING_ATTACK_FAST", "FLY"),
    #         # ("AERODACTYL", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("AERODACTYL_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
    #         # ("AERODACTYL_SHADOW_FORM", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("AERODACTYL_MEGA", "WING_ATTACK_FAST", "FLY"),
    #         # ("AERODACTYL_MEGA", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("CHARIZARD", "WING_ATTACK_FAST", "FLY"),
    #         # ("CHARIZARD", "WING_ATTACK_FAST", "ACROBATICS"),
    #         # ("CHARIZARD", "WING_ATTACK_FAST", "HURRICANE"),
    #         # ("CHARIZARD", "AIR_SLASH_FAST", "FLY"),
    #         # ("CHARIZARD", "AIR_SLASH_FAST", "ACROBATICS"),
    #         # ("CHARIZARD", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("CHARIZARD_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
    #         # ("CHARIZARD_SHADOW_FORM", "WING_ATTACK_FAST", "ACROBATICS"),
    #         # ("CHARIZARD_SHADOW_FORM", "WING_ATTACK_FAST", "HURRICANE"),
    #         # ("CHARIZARD_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("CHARIZARD_SHADOW_FORM", "AIR_SLASH_FAST", "ACROBATICS"),
    #         # ("CHARIZARD_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("CHARIZARD_MEGA_Y", "WING_ATTACK_FAST", "FLY"),
    #         # ("CHARIZARD_MEGA_Y", "WING_ATTACK_FAST", "ACROBATICS"),
    #         # ("CHARIZARD_MEGA_Y", "WING_ATTACK_FAST", "HURRICANE"),
    #         # ("CHARIZARD_MEGA_Y", "AIR_SLASH_FAST", "FLY"),
    #         # ("CHARIZARD_MEGA_Y", "AIR_SLASH_FAST", "ACROBATICS"),
    #         # ("CHARIZARD_MEGA_Y", "AIR_SLASH_FAST", "HURRICANE"),
    #         # ("ARCHEOPS", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("ARCHEOPS", "WING_ATTACK_FAST", "ACROBATICS"),
    #         # ("ARCHEOPS_SHADOW_FORM", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("ARCHEOPS_SHADOW_FORM", "WING_ATTACK_FAST", "ACROBATICS"),
    #         # ("PIDGEOT_MEGA", "GUST_FAST", "FLY"),
    #         # # Skipped Tornadus-I here to put it under signature moves
    #         # ("DRAGONITE", "WING_ATTACK_FAST", "FLY"),
    #         # # ("DRAGONITE", "AIR_SLASH_FAST", "FLY"),
    #         # ("DRAGONITE_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
    #         # # ("DRAGONITE_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("SHAYMIN_SKY_FORM", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("ZAPDOS", "PECK_FAST", "DRILL_PECK"),
    #         # ("ZAPDOS", "PECK_FAST", "FLY"),
    #         # ("ZAPDOS", "PECK_FAST", "SKY_ATTACK"),
    #         # ("ZAPDOS_SHADOW_FORM", "PECK_FAST", "DRILL_PECK"),
    #         # ("ZAPDOS_SHADOW_FORM", "PECK_FAST", "FLY"),
    #         # ("ZAPDOS_SHADOW_FORM", "PECK_FAST", "SKY_ATTACK"),
    #         # ("ZAPDOS_GALARIAN_FORM", "PECK_FAST", "BRAVE_BIRD"),
    #         # ("ZAPDOS_GALARIAN_FORM", "PECK_FAST", "DRILL_PECK"),
    #         # ("ZAPDOS_GALARIAN_FORM", "PECK_FAST", "FLY"),
    #         # ("MOLTRES", "WING_ATTACK_FAST", "FLY"),
    #         # # ("MOLTRES", "GUST_FAST", "SKY_ATTACK"),
    #         # # ("MOLTRES", "GUST_FAST", "FLY"),
    #         # ("MOLTRES_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
    #         # # ("MOLTRES_SHADOW_FORM", "GUST_FAST", "SKY_ATTACK"),
    #         # # ("MOLTRES_SHADOW_FORM", "GUST_FAST", "FLY"),
    #         # ("ARTICUNO_GALARIAN_FORM", "GUST_FAST", "BRAVE_BIRD"),
    #         # ("ARTICUNO_GALARIAN_FORM", "GUST_FAST", "FLY"),
    #         # # ("ARTICUNO_GALARIAN_FORM", "AIR_SLASH_FAST", "BRAVE_BIRD"),
    #         # # ("ARTICUNO_GALARIAN_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("HONCHKROW", "PECK_FAST", "FLY"),
    #         # # ("HONCHKROW", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # # ("HONCHKROW", "WING_ATTACK_FAST", "FLY"),
    #         # ("HONCHKROW", "GUST_FAST", "SKY_ATTACK"),
    #         # ("HONCHKROW", "GUST_FAST", "FLY"),
    #         # ("HONCHKROW_SHADOW_FORM", "PECK_FAST", "FLY"),
    #         # # ("HONCHKROW_SHADOW_FORM", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # # ("HONCHKROW_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
    #         # ("HONCHKROW_SHADOW_FORM", "GUST_FAST", "SKY_ATTACK"),
    #         # ("HONCHKROW_SHADOW_FORM", "GUST_FAST", "FLY"),
    #         # ("HO_OH", "GUST_FAST", "BRAVE_BIRD"),
    #         # ("HO_OH", "GUST_FAST", "SKY_ATTACK"),
    #         # ("HO_OH", "GUST_FAST", "FLY"),
    #         # # ("HO_OH", "AIR_SLASH_FAST", "BRAVE_BIRD"),
    #         # # ("HO_OH", "AIR_SLASH_FAST", "SKY_ATTACK"),
    #         # # ("HO_OH", "AIR_SLASH_FAST", "FLY"),
    #         # ("HO_OH_SHADOW_FORM", "GUST_FAST", "BRAVE_BIRD"),
    #         # ("HO_OH_SHADOW_FORM", "GUST_FAST", "SKY_ATTACK"),
    #         # ("HO_OH_SHADOW_FORM", "GUST_FAST", "FLY"),
    #         # # ("HO_OH_SHADOW_FORM", "AIR_SLASH_FAST", "BRAVE_BIRD"),
    #         # # ("HO_OH_SHADOW_FORM", "AIR_SLASH_FAST", "SKY_ATTACK"),
    #         # # ("HO_OH_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("UNFEZANT", "AIR_SLASH_FAST", "FLY"),
    #         # # ("UNFEZANT", "GUST_FAST", "SKY_ATTACK"),
    #         # # ("UNFEZANT", "GUST_FAST", "FLY"),
    #         # ("UNFEZANT_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # # ("UNFEZANT_SHADOW_FORM", "GUST_FAST", "SKY_ATTACK"),
    #         # # ("UNFEZANT_SHADOW_FORM", "GUST_FAST", "FLY"),
    #         # ("TOGEKISS", "AIR_SLASH_FAST", "SKY_ATTACK"),
    #         # ("TOGEKISS", "AIR_SLASH_FAST", "FLY"),
    #         # ("TOGEKISS_SHADOW_FORM", "AIR_SLASH_FAST", "SKY_ATTACK"),
    #         # ("TOGEKISS_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
    #         # ("TOUCANNON", "PECK_FAST", "FLY"),
    #         # ("TOUCANNON", "PECK_FAST", "BRAVE_BIRD"),
    #         # ("TOUCANNON", "PECK_FAST", "SKY_ATTACK"),
    #         # ("LUGIA", "GUST_FAST", "AEROBLAST"),
    #         # ("LUGIA", "GUST_FAST", "AEROBLAST_PLUS_PLUS"),
    #         # ("LUGIA_SHADOW_FORM", "GUST_FAST", "AEROBLAST"),
    #         # ("LUGIA_SHADOW_FORM", "GUST_FAST", "AEROBLAST_PLUS"),
    #
    #         # [Flying] Boss movesets
    #         # ("RAYQUAZA", "AIR_SLASH_FAST", "DRAGON_ASCENT"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "DRAGON_ASCENT"),
    #         # ("RAYQUAZA", "AIR_SLASH_FAST", "AERIAL_ACE"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "AERIAL_ACE"),
    #         # ("MOLTRES_SHADOW_FORM", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("MOLTRES_SHADOW_FORM", "FIRE_SPIN_FAST", "SKY_ATTACK"),
    #         # ("YVELTAL", "GUST_FAST", "OBLIVION_WING"),
    #         # ("YVELTAL", "GUST_FAST", "HURRICANE"),
    #         # ("HONCHKROW_SHADOW_FORM", "PECK_FAST", "SKY_ATTACK"),
    #         # ("HONCHKROW_SHADOW_FORM", "SNARL_FAST", "SKY_ATTACK"),
    #         # ("HONCHKROW", "PECK_FAST", "SKY_ATTACK"),
    #         # ("HONCHKROW", "SNARL_FAST", "SKY_ATTACK"),
    #         # ("STARAPTOR_SHADOW_FORM", "GUST_FAST", "FLY"),
    #         # ("STARAPTOR_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
    #         # ("MOLTRES", "WING_ATTACK_FAST", "SKY_ATTACK"),
    #         # ("MOLTRES", "FIRE_SPIN_FAST", "SKY_ATTACK"),
    #
    #         # ("BRAVIARY", "AIR_SLASH_FAST", "FLY"),
    #         # ("STARAPTOR", "GUST_FAST", "FLY"),
    #         # ("STARAPTOR", "WING_ATTACK_FAST", "FLY"),
    #         # ("TORNADUS", "AIR_SLASH_FAST", "BLEAKWIND_STORM"),
    #         # ("TORNADUS_THERIAN_FORM", "GUST_FAST", "BLEAKWIND_STORM"),
    #
    #         # [Grass]
    #         # ("DECIDUEYE_HISUIAN_FORM", "MAGICAL_LEAF_FAST", "TRAILBLAZE"),  # Now
    #         # ("DECIDUEYE_HISUIAN_FORM", "MAGICAL_LEAF_FAST", "ENERGY_BALL"),
    #         # ("SHAYMIN_SKY_FORM", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),  # Missing data from Pokebattler
    #         # ("SHAYMIN_LAND_FORM", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("RILLABOOM", "RAZOR_LEAF_FAST", "GRASS_KNOT"),  # Future Pokemon
    #         # ("RILLABOOM", "RAZOR_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("MEOWSCARADA", "LEAFAGE_FAST", "FRENZY_PLANT"),
    #         # ("DECIDUEYE_HISUIAN_FORM", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("BRAMBLEGHAST", "BULLET_SEED_FAST", "POWER_WHIP"),
    #         # ("SCOVILLAIN", "LEAFAGE_FAST", "GRASS_KNOT"),
    #         # ("ARBOLIVA", "MAGICAL_LEAF_FAST", "SEED_BOMB"),
    #         # ("ROSERADE_SHADOW_FORM", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),  # Future shadows
    #         # ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "GRASS_KNOT"),
    #         # # ("SCEPTILE", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),  # Better regular moves (removed excess Magical Leaf users)
    #         # # ("SCEPTILE_SHADOW_FORM", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # # ("SCEPTILE_MEGA", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # # ("ABOMASNOW_MEGA", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # # ("VENUSAUR", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # # ("VENUSAUR_SHADOW_FORM", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # # ("VENUSAUR_MEGA", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # # ("ZARUDE", "MAGICAL_LEAF_FAST", "POWER_WHIP"),
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "GRASS_KNOT"),
    #         # ("TSAREENA", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),  # Signature moves
    #         # ("ZARUDE", "VINE_WHIP_FAST", "FRENZY_PLANT"),
    #
    #         # [Grass] For boss movesets
    #         # ("SHAYMIN_SKY_FORM", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("TANGROWTH_SHADOW_FORM", "VINE_WHIP_FAST", "POWER_WHIP"),
    #         # ("ZARUDE", "VINE_WHIP_FAST", "POWER_WHIP"),
    #         # ("VENUSAUR_SHADOW_FORM", "VINE_WHIP_FAST", "FRENZY_PLANT"),
    #         # ("SCEPTILE_SHADOW_FORM", "BULLET_SEED_FAST", "FRENZY_PLANT"),
    #         # ("TORTERRA_SHADOW_FORM", "RAZOR_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("KARTANA", "RAZOR_LEAF_FAST", "LEAF_BLADE"),
    #         #
    #         # ("ROSERADE", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("DECIDUEYE", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("DECIDUEYE_HISUIAN_FORM", "MAGICAL_LEAF_FAST", "FRENZY_PLANT"),
    #         # ("TSAREENA", "MAGICAL_LEAF_FAST", "GRASS_KNOT"),
    #         # ("TAPU_BULU", "BULLET_SEED_FAST", "GRASS_KNOT"),
    #         # ("CHESNAUGHT", "VINE_WHIP_FAST", "FRENZY_PLANT"),
    #         # ("TANGROWTH", "VINE_WHIP_FAST", "POWER_WHIP"),
    #         # ("SCEPTILE", "BULLET_SEED_FAST", "FRENZY_PLANT"),
    #         # ("MEOWSCARADA", "LEAFAGE_FAST", "GRASS_KNOT"),
    #
    #         # [Ground]
    #         # ("LANDORUS_THERIAN_FORM", "MUD_SHOT_FAST", "SANDSEAR_STORM"),  # (not yet added to Pokebattler)
    #         # ("LANDORUS_INCARNATE_FORM", "MUD_SHOT_FAST", "SANDSEAR_STORM"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE"),  # Now
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE", "11\\11\\11"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES", "11\\11\\11"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE", "6\\6\\6"),
    #         # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES", "6\\6\\6"),
    #         # ("MUDSDALE", "MUD_SLAP_FAST", "EARTHQUAKE"),  # Future Pokemon
    #         # ("KROOKODILE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),  # Future shadows
    #         # ("CAMERUPT_MEGA", "INCINERATE_FAST", "EARTH_POWER"),  # Future megas
    #         # ("CAMERUPT_MEGA", "ROCK_SMASH_FAST", "EARTH_POWER"),
    #         # ("CAMERUPT_MEGA", "EMBER_FAST", "EARTH_POWER"),
    #         # ("RHYPERIOR", "MUD_SLAP_FAST", "EARTH_POWER"),  # Better moves
    #         # ("RHYPERIOR", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("RHYPERIOR", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # # ("MAMOSWINE", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # # ("MAMOSWINE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # # ("EXCADRILL", "MUD_SLAP_FAST", "EARTH_POWER"),  # Consider taking out next time
    #         # # ("EXCADRILL", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # # ("EXCADRILL", "METAL_CLAW_FAST", "EARTH_POWER"),
    #         # # ("EXCADRILL", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # # ("EXCADRILL", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
    #         # # ("EXCADRILL", "METAL_CLAW_FAST", "HIGH_HORSEPOWER"),
    #         # # ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # # ("EXCADRILL_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "EARTH_POWER"),
    #         # # ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # # ("EXCADRILL_SHADOW_FORM", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
    #         # # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "HIGH_HORSEPOWER"),
    #         # ("KROOKODILE", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("KROOKODILE", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("KROOKODILE", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # ("KROOKODILE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("KROOKODILE_SHADOW_FORM", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("KROOKODILE_SHADOW_FORM", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # ("MUDSDALE", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("MUDSDALE", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("STEELIX_MEGA", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("STEELIX_MEGA", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # ("STEELIX_MEGA", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("STEELIX_MEGA", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # ("GARCHOMP", "MUD_SHOT_FAST", "SCORCHING_SANDS"),
    #         # ("GARCHOMP_SHADOW_FORM", "MUD_SHOT_FAST", "SCORCHING_SANDS"),
    #         # ("GARCHOMP_MEGA", "MUD_SHOT_FAST", "SCORCHING_SANDS"),
    #         # ("CAMERUPT_MEGA", "MUD_SLAP_FAST", "EARTH_POWER"),
    #         # # Signature moves (ignored as there's no more)
    #
    #         # [Ground] Boss Movesets
    #         # ("MAMOSWINE", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("GARCHOMP", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("GARCHOMP", "DRAGON_TAIL_FAST", "EARTH_POWER"),
    #         # ("EXCADRILL", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # ("EXCADRILL", "MUD_SHOT_FAST", "SCORCHING_SANDS"),
    #         # ("EXCADRILL", "METAL_CLAW_FAST", "SCORCHING_SANDS"),
    #         # ("EXCADRILL", "MUD_SLAP_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL", "MUD_SHOT_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL", "METAL_CLAW_FAST", "DRILL_RUN"),
    #         # ("RHYPERIOR", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("RHYPERIOR", "SMACK_DOWN_FAST", "EARTHQUAKE"),
    #
    #         # ("MAMOSWINE_SHADOW_FORM", "MUD_SLAP_FAST", "HIGH_HORSEPOWER"),
    #         # ("GARCHOMP_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "EARTH_POWER"),
    #         # ("GARCHOMP_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE"),
    #         # ("GARCHOMP_SHADOW_FORM", "DRAGON_TAIL_FAST", "EARTHQUAKE"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "SCORCHING_SANDS"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SHOT_FAST", "SCORCHING_SANDS"),
    #         # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "SCORCHING_SANDS"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SLAP_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL_SHADOW_FORM", "MUD_SHOT_FAST", "DRILL_RUN"),
    #         # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "DRILL_RUN"),
    #         # ("LANDORUS_THERIAN_FORM", "MUD_SHOT_FAST", "SANDSEAR_STORM"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
    #         # ("RHYPERIOR_SHADOW_FORM", "SMACK_DOWN_FAST", "EARTHQUAKE"),
    #         # ("GROUDON", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
    #
    #         # [Ice]
    #         # ("BAXCALIBUR", "ICE_FANG_FAST", "AVALANCHE"),  # Now
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "BLIZZARD"),  # Future Pokemon
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "BLIZZARD"),
    #         # ("KYUREM_WHITE_FORM", "DRAGON_BREATH_FAST", "BLIZZARD"),
    #         # ("KYUREM_WHITE_FORM", "STEEL_WING_FAST", "BLIZZARD"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("FROSMOTH", "POWDER_SNOW_FAST", "ICE_BEAM"),
    #         # ("CALYREX_ICE_RIDER_FORM", "CONFUSION_FAST", "AVALANCHE"),
    #         # ("CHIENPAO", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("GLACEON_SHADOW_FORM", "FROST_BREATH_FAST", "AVALANCHE"),  # Future shadows
    #         # ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "ICE_BEAM"),  # Future megas
    #         # ("KYUREM", "ICE_SHARD_FAST", "GLACIATE"),  # Better regular moves
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "ICE_BEAM"),
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "ICE_BEAM"),
    #         # ("KYUREM_BLACK_FORM", "ICE_SHARD_FAST", "BLIZZARD"),
    #         # ("KYUREM_BLACK_FORM", "ICE_SHARD_FAST", "ICE_BEAM"),
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
    #         # [Ice] Boss movesets
    #         # ("MAMOSWINE", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("MAMOSWINE_SHADOW_FORM", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("DARMANITAN_GALARIAN_STANDARD_FORM", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("WEAVILE", "ICE_SHARD_FAST", "AVALANCHE"),
    #         # ("WEAVILE", "SNARL_FAST", "AVALANCHE"),
    #         # ("WEAVILE_SHADOW_FORM", "ICE_SHARD_FAST", "AVALANCHE"),
    #         # ("WEAVILE_SHADOW_FORM", "SNARL_FAST", "AVALANCHE"),
    #         # ("MEWTWO", "PSYCHO_CUT_FAST", "ICE_BEAM"),
    #         # ("MEWTWO_SHADOW_FORM", "PSYCHO_CUT_FAST", "ICE_BEAM"),
    #         # ("GLACEON", "FROST_BREATH_FAST", "AVALANCHE"),
    #         # ("KYUREM", "DRAGON_BREATH_FAST", "GLACIATE"),
    #         # ("KYUREM", "STEEL_WING_FAST", "GLACIATE"),
    #
    #         # [Ice Dragon] Dragons for boss movesets
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),  # Manually "fill blanks"
    #         # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("RAYQUAZA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("SALAMENCE", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("SALAMENCE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("GARCHOMP", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("PALKIA", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("PALKIA_ORIGIN_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
    #         # ("DIALGA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
    #         # ("ZEKROM", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "OUTRAGE"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
    #         # ("DRAGONITE", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
    #         # ("HAXORUS", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
    #         # ("MAMOSWINE", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("MAMOSWINE_SHADOW_FORM", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("BAXCALIBUR", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("DARMANITAN_ZEN_FORM", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "AVALANCHE"),
    #         # ("CHIENPAO", "POWDER_SNOW_FAST", "AVALANCHE"),
    #         # ("KYUREM", "DRAGON_BREATH_FAST", "GLACIATE"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "BLIZZARD"),
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "BLIZZARD"),
    #         # ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "GLACIATE"),
    #         # ("KYUREM_BLACK_FORM", "SHADOW_CLAW_FAST", "GLACIATE"),
    #
    #         # [Ice Rock Electric]
    #         # ("RAIKOU_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("XURKITREE", "THUNDER_SHOCK_FAST", "DISCHARGE"),
    #         # ("XURKITREE", "SPARK_FAST", "DISCHARGE"),
    #         # ("MANECTRIC_MEGA", "THUNDER_FANG_FAST", "WILD_CHARGE"),
    #         # ("ELECTIVIRE_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),
    #         # ("MAGNEZONE_SHADOW_FORM", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("LUXRAY_SHADOW_FORM", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("ZEKROM", "CHARGE_BEAM_FAST", "FUSION_BOLT"),
    #         # ("ZEKROM", "CHARGE_BEAM_FAST", "WILD_CHARGE"),
    #         # ("THUNDURUS_THERIAN_FORM", "VOLT_SWITCH_FAST", "THUNDERBOLT"),
    #         # ("RAIKOU", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("ELECTIVIRE", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
    #         # ("ZAPDOS", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),
    #         # ("MAGNEZONE", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("LUXRAY", "SPARK_FAST", "WILD_CHARGE"),
    #         # ("AERODACTYL_MEGA", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #         # ("RAMPARDOS", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("RHYPERIOR", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("TYRANTRUM", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("TERRAKION", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("GIGALITH", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("TYRANITAR", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #
    #         # [Poison]
    #         # ("NAGANADEL", "POISON_JAB_FAST", "SLUDGE_BOMB"),  # Future Pokemon
    #         # ("ETERNATUS", "POISON_JAB_FAST", "CROSS_POISON"),
    #         # ("REVAVROOM", "POISON_JAB_FAST", "GUNK_SHOT"),
    #         # ("GENGAR_SHADOW_FORM", "LICK_FAST", "SLUDGE_BOMB"),  # Future shadows
    #         # ("GENGAR_SHADOW_FORM", "HEX_FAST", "SLUDGE_BOMB"),
    #         # ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("GENGAR", "POISON_JAB_FAST", "SLUDGE_BOMB"),  # Better moves
    #         # ("GENGAR_SHADOW_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("GENGAR_MEGA", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("ARCEUS_POISON_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("SALAZZLE", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("SNEASLER", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("SNEASLER", "POISON_JAB_FAST", "GUNK_SHOT"),
    #         # ("TOXTRICITY", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("ETERNATUS", "POISON_JAB_FAST", "SLUDGE_BOMB"),
    #         # ("ETERNATUS", "POISON_JAB_FAST", "GUNK_SHOT"),
    #         # Signature moves (None because no better moves than Sludge Bomb)
    #
    #         # [Psychic]
    #         # ("GARDEVOIR_MEGA", "CONFUSION_FAST", "PSYCHIC"),  # Now
    #         # ("GARDEVOIR_MEGA", "CONFUSION_FAST", "SYNCHRONOISE"),
    #         # ("NECROZMA_ULTRA_FORM", "CONFUSION_FAST", "PSYCHIC"),  # Future Pokemon
    #         # ("NECROZMA_ULTRA_FORM", "PSYCHO_CUT_FAST", "FUTURESIGHT"),
    #         # ("NECROZMA_DAWN_WINGS_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("NECROZMA_DAWN_WINGS_FORM", "PSYCHO_CUT_FAST", "FUTURESIGHT"),
    #         # ("NECROZMA_DUSK_MANE_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("NECROZMA_DUSK_MANE_FORM", "PSYCHO_CUT_FAST", "FUTURESIGHT"),
    #         # ("NECROZMA", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("CALYREX_SHADOW_RIDER_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("HATTERENE", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("ESPEON_SHADOW_FORM", "CONFUSION_FAST", "PSYCHIC"),  # Future shadows
    #         # ("GALLADE_MEGA", "CONFUSION_FAST", "PSYCHIC"),  # Future megas
    #         # ("GALLADE_MEGA", "CONFUSION_FAST", "SYNCHRONOISE"),
    #         # ("MEDICHAM_MEGA", "PSYCHO_CUT_FAST", "PSYCHIC"),
    #         # ("METAGROSS_MEGA", "ZEN_HEADBUTT_FAST", "PSYCHIC"),  # (Mewtwo in its own section with level treatments)
    #         # ("DEOXYS", "ZEN_HEADBUTT_FAST", "PSYCHIC"),  # Better moves
    #         # ("DEOXYS_ATTACK_FORM", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
    #         # ("ARTICUNO_GALARIAN_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("TAPU_LELE", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("AZELF", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("MELOETTA_ARIA_FORM", "CONFUSION_FAST", "PSYCHIC"),
    #         # ("DARMANITAN_ZEN_FORM", "EXTRASENSORY_FAST", "PSYCHIC"),
    #         # ("DEOXYS", "ZEN_HEADBUTT_FAST", "PSYSTRIKE"),  # Signature moves
    #         # ("DEOXYS_ATTACK_FORM", "ZEN_HEADBUTT_FAST", "PSYSTRIKE"),
    #         # ("HOOPA", "CONFUSION_FAST", "PSYSTRIKE"),  # (Confined)
    #         # ("NECROZMA_ULTRA_FORM", "CONFUSION_FAST", "PSYSTRIKE"),
    #         # ("NECROZMA_DAWN_WINGS_FORM", "CONFUSION_FAST", "PSYSTRIKE"),
    #         # ("NECROZMA", "CONFUSION_FAST", "PSYSTRIKE"),
    #         # ("HATTERENE", "CONFUSION_FAST", "PSYSTRIKE"),
    #
    #         # [Psychic] Shadow Mewtwo IVs
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
    #
    #         # [Rock]
    #         # ("TYRANITAR_MEGA", "SMACK_DOWN_FAST", "STONE_EDGE"),  # Now
    #         # ("STONJOURNER", "ROCK_THROW_FAST", "ROCK_SLIDE"),  # Future Pokemon
    #         # ("STONJOURNER", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #         # ("STAKATAKA", "ROCK_THROW_FAST", "STONE_EDGE"),
    #         # ("GLIMMORA", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("RHYPERIOR_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_WRECKER"),  # Future shadows
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("GIGALITH_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("TERRAKION_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "ROCK_SLIDE"),  # Future megas
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
    #         # ("KLEAVOR", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("RAMPARDOS", "SMACK_DOWN_FAST", "METEOR_BEAM"),  # Signature moves
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("KLEAVOR", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("KLEAVOR", "SMACK_DOWN_FAST", "METEOR_BEAM"),
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "ROCK_WRECKER"),  # (MB above)
    #         # ("LYCANROC_MIDDAY_FORM", "ROCK_THROW_FAST", "ROCK_WRECKER"),
    #         # ("LYCANROC_MIDDAY_FORM", "ROCK_THROW_FAST", "METEOR_BEAM"),
    #
    #         # [Rock] for boss movesets
    #         # ("DIANCIE_MEGA", "ROCK_THROW_FAST", "ROCK_SLIDE"),
    #         # ("TYRANITAR_MEGA", "SMACK_DOWN_FAST", "STONE_EDGE"),
    #         # ("RHYPERIOR_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "ROCK_WRECKER"),
    #         # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #         # ("RHYPERIOR", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
    #         # ("RHYPERIOR", "MUD_SLAP_FAST", "ROCK_WRECKER"),
    #         # ("RAMPARDOS", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
    #
    #         # [Steel]
    #         # ("MELMETAL", "THUNDER_SHOCK_FAST", "DOUBLE_IRON_BASH"),  # Now
    #         # ("NECROZMA_DUSK_MANE_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),  # Future Pokemon
    #         # ("MAGEARNA", "LOCK_ON_FAST", "HEAVY_SLAM"),
    #         # ("ZACIAN_CROWNED_SWORD_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),
    #         # ("ZAMAZENTA_CROWNED_SHIELD_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),
    #         # ("DURALUDON", "METAL_CLAW_FAST", "FLASH_CANNON"),
    #         # ("KINGAMBIT", "METAL_CLAW_FAST", "IRON_HEAD"),
    #         # ("DIALGA_SHADOW_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),  # Future shadows
    #         # ("EXCADRILL_SHADOW_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),
    #         # ("METAGROSS_MEGA", "BULLET_PUNCH_FAST", "METEOR_MASH"),  # Future megas
    #         # ("LUCARIO_MEGA", "BULLET_PUNCH_FAST", "FLASH_CANNON"),
    #         # ("LUCARIO", "BULLET_PUNCH_FAST", "METEOR_MASH"),  # Better moves
    #         # ("LUCARIO_SHADOW_FORM", "BULLET_PUNCH_FAST", "METEOR_MASH"),
    #         # ("LUCARIO_MEGA", "BULLET_PUNCH_FAST", "METEOR_MASH"),
    #         # ("SOLGALEO", "METAL_CLAW_FAST", "IRON_HEAD"),
    #         # ("HEATRAN", "METAL_CLAW_FAST", "IRON_HEAD"),
    #         # # ("GHOLDENGO", "HEX_FAST", "DOUBLE_IRON_BASH"),  # Signature moves
    #         # ("GHOLDENGO", "HEX_FAST", "METEOR_MASH"),
    #         # ("GHOLDENGO", "HEX_FAST", "DOOM_DESIRE"),
    #         # # ("SOLGALEO", "METAL_CLAW_FAST", "DOUBLE_IRON_BASH"),
    #         # ("SOLGALEO", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # # ("NECROZMA_DUSK_MANE_FORM", "METAL_CLAW_FAST", "DOUBLE_IRON_BASH"),
    #         # ("NECROZMA_DUSK_MANE_FORM", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # # ("KLINKLANG", "THUNDER_SHOCK_FAST", "DOUBLE_IRON_BASH"),
    #         # # ("KLINKLANG", "THUNDER_SHOCK_FAST", "METEOR_MASH"),
    #         # # ("KLINKLANG", "THUNDER_SHOCK_FAST", "DOOM_DESIRE"),
    #         # ("AGGRON", "IRON_TAIL_FAST", "METEOR_MASH"),  # Meteor Mash what-ifs
    #         # ("AGGRON_SHADOW_FORM", "IRON_TAIL_FAST", "METEOR_MASH"),
    #         # ("AGGRON_MEGA", "IRON_TAIL_FAST", "METEOR_MASH"),
    #         # ("GENESECT", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # ("SCIZOR", "BULLET_PUNCH_FAST", "METEOR_MASH"),
    #         # ("SCIZOR_SHADOW_FORM", "BULLET_PUNCH_FAST", "METEOR_MASH"),
    #         # ("SCIZOR_MEGA", "BULLET_PUNCH_FAST", "METEOR_MASH"),
    #         # ("DIALGA", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # ("DIALGA_ORIGIN_FORM", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # ("EXCADRILL", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # ("MELMETAL", "THUNDER_SHOCK_FAST", "METEOR_MASH"),
    #         # ("KARTANA", "RAZOR_LEAF_FAST", "METEOR_MASH"),
    #         # ("KARTANA", "PSYCHO_CUT_FAST", "METEOR_MASH"),
    #         # ("MELMETAL", "METAL_CLAW_FAST", "DOUBLE_IRON_BASH"),  # Fast move what-ifs
    #         # ("MELMETAL", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # ("GHOLDENGO", "METAL_CLAW_FAST", "DOUBLE_IRON_BASH"),
    #         # ("GHOLDENGO", "METAL_CLAW_FAST", "METEOR_MASH"),
    #         # ("GHOLDENGO", "METAL_CLAW_FAST", "DOOM_DESIRE"),
    #
    #         # [Steel] Custom IVs
    #         # ("METAGROSS_SHADOW_FORM", "BULLET_PUNCH_FAST", "METEOR_MASH", "15\\1\\15"),
    #         # ("METAGROSS_SHADOW_FORM", "BULLET_PUNCH_FAST", "METEOR_MASH", "14\\14\\13"),
    #         # ("METAGROSS_SHADOW_FORM", "BULLET_PUNCH_FAST", "METEOR_MASH", "13\\15\\15"),
    #
    #         # [Water]
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "SURF"),  # Now
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "ORIGIN_PULSE"),
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "SURF", "11\\11\\11"),
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "ORIGIN_PULSE", "11\\11\\11"),
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "SURF", "6\\6\\6"),
    #         # ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "ORIGIN_PULSE", "6\\6\\6"),
    #         # ("EMPOLEON_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("EMPOLEON_SHADOW_FORM", "METAL_CLAW_FAST", "HYDRO_CANNON"),
    #         # ("VOLCANION", "WATER_GUN_FAST", "HYDRO_PUMP"),  # Future Pokemon
    #         # ("PRIMARINA", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("WISHIWASHI_SCHOOL_FORM", "WATERFALL_FAST", "SURF"),
    #         # ("WISHIWASHI_SCHOOL_FORM", "WATERFALL_FAST", "HYDRO_PUMP"),
    #         # ("INTELEON", "WATER_GUN_FAST", "SURF"),
    #         # ("INTELEON", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # ("QUAQUAVAL", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # # ("BARRASKEWDA", "WATERFALL_FAST", "AQUA_JET"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "WATERFALL_FAST", "AQUA_JET"),
    #         # # ("TATSUGIRI", "WATER_GUN_FAST", "SURF"),
    #         # ("PALAFIN_HERO_FORM", "WATERFALL_FAST", "WATER_PULSE"),
    #         # ("KINGLER_SHADOW_FORM", "BUBBLE_FAST", "CRABHAMMER"),  # Future shadows
    #         # ("SAMUROTT_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_SHADOW_FORM", "FURY_CUTTER_FAST", "HYDRO_CANNON"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "AQUA_TAIL"),
    #         # ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "HYDRO_PUMP"),
    #         # ("SHARPEDO_MEGA", "WATERFALL_FAST", "HYDRO_PUMP"),  # Future megas
    #         # ("GYARADOS", "WATERFALL_FAST", "SURF"),  # Better regular moves
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
    #         # ("PALKIA_ORIGIN_FORM", "WATERFALL_FAST", "AQUA_TAIL"),
    #         # ("PALKIA_ORIGIN_FORM", "WATERFALL_FAST", "HYDRO_PUMP"),
    #         # ("PALKIA_ORIGIN_FORM", "WATERFALL_FAST", "SURF"),
    #         # ("SAMUROTT_HISUIAN_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_HISUIAN_FORM", "FURY_CUTTER_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_HISUIAN_FORM", "SNARL_FAST", "HYDRO_CANNON"),
    #         # # ("BARRASKEWDA", "WATERFALL_FAST", "SURF"),
    #         # ("VOLCANION", "WATER_GUN_FAST", "CRABHAMMER"),  # Signature moves
    #         # ("VOLCANION", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "WATERFALL_FAST", "CRABHAMMER"),
    #         # ("URSHIFU_RAPID_STRIKE_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #
    #         # [Water] For boss movesets
    #         # ("GRENINJA", "WATER_SHURIKEN_FAST", "HYDRO_CANNON"),
    #         # ("SWAMPERT", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # ("KINGLER", "BUBBLE_FAST", "CRABHAMMER"),
    #         # ("SAMUROTT", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("EMPOLEON", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("FERALIGATR", "WATER_GUN_FAST", "HYDRO_CANNON"),
    #         # ("FERALIGATR", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_HISUIAN_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_HISUIAN_FORM", "FURY_CUTTER_FAST", "HYDRO_CANNON"),
    #         # ("SAMUROTT_HISUIAN_FORM", "SNARL_FAST", "HYDRO_CANNON"),
    #     ],
    # },
    #
    # # Replacing unnerfed megas on Pokebattler
    # # {
    # #     "Min level": 25,  # Unnerfed 25 = Nerfed 30
    # #     "Max level": 25,
    # #     "Level step size": 5,
    # #     "Pokemon code names and moves": [
    # #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    # #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    # #     ],
    # # },
    # # {
    # #     "Min level": 27.5,  # Unnerfed 27.5 = Nerfed 35
    # #     "Max level": 27.5,
    # #     "Level step size": 5,
    # #     "Pokemon code names and moves": [
    # #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    # #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    # #     ],
    # # },
    # # {
    # #     "Min level": 29.5,  # Unnerfed 29.5 = Nerfed 40
    # #     "Max level": 29.5,
    # #     "Level step size": 5,
    # #     "Pokemon code names and moves": [
    # #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    # #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    # #     ],
    # # },
    # # {
    # #     "Min level": 32.5,  # Unnerfed 32.5 = Nerfed 45
    # #     "Max level": 32.5,
    # #     "Level step size": 5,
    # #     "Pokemon code names and moves": [
    # #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    # #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    # #     ],
    # # },
    # # {
    # #     "Min level": 36.5,  # Unnerfed 36.5 = Nerfed 50
    # #     "Max level": 36.5,
    # #     "Level step size": 5,
    # #     "Pokemon code names and moves": [
    # #         # ("RAYQUAZA_MEGA", "DRAGON_TAIL_FAST", "OUTRAGE"),
    # #         ("MEWTWO_MEGA_Y", "PSYCHO_CUT_FAST", "SHADOW_BALL"),
    # #     ],
    # # },
    #
    # # [For all counters]
    # # {
    # #     "Min level": 30,
    # #     "Max level": 50,
    # #     "Level step size": 5, #5,  # Can be as low as 0.5, but recommend 5 for efficiency
    # # },
    #
    # # Add more {} blocks here if needed
    # # {
    # #     "Charged move types": ["Ice"],
    # #     "Min level": 40,
    # #     "Max level": 50,
    # #     "Level step size": 10,
    # # },

    # Below is for the utility metric
    {
        "Min level": 40,
        "Max level": 40,
        "Level step size": 5,
        "Must be non mega": True,
        "Exclude": ["LUCARIO_MEGA", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "MEWTWO_MEGA_X", "MEWTWO_MEGA_Y",
                    "CALYREX_SHADOW_RIDER_FORM", "BLACEPHALON", "ETERNATUS", "ETERNATUS_ETERNAMAX_FORM",
                    "PALKIA_SHADOW_FORM", "RESHIRAM_SHADOW_FORM", "ZEKROM_SHADOW_FORM", "KYUREM_SHADOW_FORM",
                    "TERRAKION_SHADOW_FORM"],
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
            ("VOLCARONA_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),
            ("YANMEGA_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),
            # [Dark/Ghost]
            ("BLACEPHALON", "ASTONISH_FAST", "SHADOW_BALL"),
            ("HYDREIGON_SHADOW_FORM", "BITE_FAST", "BRUTAL_SWING"),
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "DARK_PULSE"),
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "SHADOW_BALL"),
            ("FLUTTERMANE", "HEX_FAST", "SHADOW_BALL"),
            ("FLUTTERMANE", "ASTONISH_FAST", "SHADOW_BALL"),
            # [Dragon]
            ("KYUREM_BLACK_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
            ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
            ("DIALGA_SHADOW_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
            ("HAXORUS_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
            ("HYDREIGON_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_PULSE"),
            ("RESHIRAM_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRACO_METEOR"),
            ("ZEKROM_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
            ("DIALGA_ORIGIN_FORM", "DRAGON_BREATH_FAST", "ROAR_OF_TIME"),
            ("PALKIA_ORIGIN_FORM", "DRAGON_TAIL_FAST", "SPACIAL_REND"),
            # [Electric]
            ("ZEKROM_SHADOW_FORM", "CHARGE_BEAM_FAST", "FUSION_BOLT"),
            ("ZEKROM_SHADOW_FORM", "CHARGE_BEAM_FAST", "WILD_CHARGE"),
            # [Fairy]
            ("FLUTTERMANE", "CHARM_FAST", "DAZZLING_GLEAM"),
            ("FLUTTERMANE", "CHARM_FAST", "MOONBLAST"),
            ("IRONVALIANT", "FAIRY_WIND_FAST", "DAZZLING_GLEAM"),
            ("IRONVALIANT", "FAIRY_WIND_FAST", "MOONBLAST"),
            ("IRONVALIANT", "GEOMANCY_FAST", "DAZZLING_GLEAM"),
            ("IRONVALIANT", "GEOMANCY_FAST", "MOONBLAST"),
            # [Fighting]
            ("LUCARIO_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
            ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            ("TERRAKION_SHADOW_FORM", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
            ("MARSHADOW", "COUNTER_FAST", "AURA_SPHERE"),
            ("IRONVALIANT", "LOW_KICK_FAST", "AURA_SPHERE"),
            # [Fire]
            ("BLACEPHALON", "INCINERATE_FAST", "OVERHEAT"),
            ("BLACEPHALON", "INCINERATE_FAST", "MYSTICAL_FIRE"),
            ("IRONMOTH", "FIRE_SPIN_FAST", "OVERHEAT"),
            ("HEATRAN_SHADOW_FORM", "FIRE_SPIN_FAST", "MAGMA_STORM"),
            ("RESHIRAM_SHADOW_FORM", "FIRE_FANG_FAST", "FUSION_FLARE"),
            ("VOLCARONA_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
            # [Flying]
            ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "DRAGON_ASCENT"),
            ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "HURRICANE"),
            ("BRAVIARY_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
            # [Grass]
            ("ROSERADE_SHADOW_FORM", "RAZOR_LEAF_FAST", "GRASS_KNOT"),
            ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "GRASS_KNOT"),
            # [Ground]
            ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
            ("LANDORUS_THERIAN_FORM", "MUD_SHOT_FAST", "SANDSEAR_STORM"),
            # [Ice]
            ("DARMANITAN_GALARIAN_ZEN_FORM", "ICE_FANG_FAST", "AVALANCHE"),
            ("CHIENPAO", "POWDER_SNOW_FAST", "AVALANCHE"),
            # [Poison]
            ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            ("NAGANADEL", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            ("ETERNATUS", "POISON_JAB_FAST", "CROSS_POISON"),
            # [Psychic]
            ("NECROZMA_ULTRA_FORM", "CONFUSION_FAST", "PSYCHIC"),
            ("CALYREX_SHADOW_RIDER_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # [Rock]
            ("TERRAKION_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            # [Steel]
            ("DIALGA_SHADOW_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),
            ("ZACIAN_CROWNED_SWORD_FORM", "METAL_CLAW_FAST", "IRON_HEAD"),
            # [Water]
            ("INTELEON", "WATER_GUN_FAST", "HYDRO_CANNON"),
            ("KYOGRE_SHADOW_FORM", "WATERFALL_FAST", "ORIGIN_PULSE"),
            ("KINGLER_SHADOW_FORM", "BUBBLE_FAST", "CRABHAMMER"),
            ("EMPOLEON_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
            ("SAMUROTT_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_CANNON"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "AQUA_TAIL"),
            ("PALKIA_SHADOW_FORM", "DRAGON_TAIL_FAST", "HYDRO_PUMP"),

            # [Speculative moves]
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
            ("DARKRAI_SHADOW_FORM", "SNARL_FAST", "BRUTAL_SWING"),
            ("ZEKROM_SHADOW_FORM", "THUNDER_FANG_FAST", "FUSION_BOLT"),
            ("ZEKROM_SHADOW_FORM", "THUNDER_FANG_FAST", "WILD_CHARGE"),
            ("XURKITREE", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
        ]
    }
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
    #     "Raid categories": ["Tier 5", "Ultra Beast Tier"],  # Here, "Tier 5" has only current bosses
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",  # "combine" or "separate"
    #     # "Filters": {  # Only those without # at the start are applied
    #     #     "Weak to contender types": ["Dragon"],
    #     # }
    # },

    # [For counters against specific boss]
    # {
    #     "Pokemon pool": ["XURKITREE"],
    #     "Raid tier": "Tier 5",  # Here, "Tier 5" has only current bosses
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 1,
    #     "Forms weight strategy": "combine",  # "combine" or "separate"
    # },
    # {
    #     "Pokemon pool": ["XURKITREE"],
    #     "Raid tier": "Tier 5",  # Here, "Tier 5" has only current bosses
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",  # "combine" or "separate"
    #     "Battle settings": {
    #         "Attack strategy": "Dodge Specials PRO",
    #     },
    # },

    {
        "Pokemon pool": "By raid tier",  # "All Pokemon", "All Pokemon except above", "By raid tier" or "By raid category"
                # Can also specify a list of Pokemon (code names), e.g. ["TAPU_BULU", "XERNEAS"]
        "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier", "Shadow Tier 5"],  # Here, "Tier 5" has all past/present/future bosses
        #"Raid category": "Ultra Beast Tier",  # Here, "Tier 5" has only current bosses
        "Filters": {  # Only those without # at the start are applied
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            # get_ensemble_weak_key(): get_move_types(),
            #"Evolution stage": "Final",  # "Final", "Pre-evolution"
            #"Must be shadow": False,  # This describes BOSSES, not attackers
            #"Must be non shadow": True,
            #"Must be mega": False,
            #"Must be non mega": True,
            #"Must be legendary": False,
            #"Must be non legendary": False,
            #"Must be mythical": False,
            #"Must be non mythical": False,
            #"Must be legendary or mythical": False,
            #"Must be non legendary or mythical": False,
            # TODO: Add a filter for ignoring certain Pokemon or raids, identified by user
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 65,
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
    #     "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier", "Shadow Tier 5"],
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
    #     "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier", "Shadow Tier 5"],
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 0,
    #     "Forms weight strategy": "combine",
    #     "Battle settings": {
    #         "Weather": "Rainy",
    #     },
    # },

    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
        "Filters": {
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            # get_ensemble_weak_key(): get_move_types(),
        },
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
    #         "Weather": "Rainy",
    #     },
    # },

    # {
    #     "Pokemon pool": "By raid tier",
    #     "Raid tiers": ["Tier 3", "Shadow Tier 3"],
    #     "Filters": {
    #         #"Weak to contender types": SINGLE_TYPE_ATTACKER,
    #         #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
    #         get_ensemble_weak_key(): get_move_types(),
    #     },
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
    #     "Raid tiers": ["Tier 3", "Shadow Tier 3"],
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
    #     "Raid tiers": ["Tier 3", "Shadow Tier 3"],
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
    #         "Weather": "Rainy",
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
    # [Consider required attackers]
    #
    # Whether all required attackers participate in estimator scaling.
    # Typically set to False, so that 1.0 is only for the best current attacker.
    # These can be overridden for individual required attackers, by providing a True/False as their 5th arg
    # in the tuple.
    #
    # ----- End of documentation for this section -----

    "Enabled": False,  # Default: True
    "Baseline chosen before filter": False,  # Default: False
    "Baseline boss moveset": "random",  # "random", "easiest", "hardest"
    "Baseline attacker level": 40,  # Specific level, "min", "max", "average", "by level"/-1/None
    "Baseline battle settings": {
        "Weather": "Extreme",
        "Friendship": TEMPORARY_FRIENDSHIP_DEFAULT,
        "Attack strategy": "No Dodging",
        "Dodge strategy": "Realistic Dodging",
    },
    "Consider required attackers": False,  # Default: False
}


CONFIG_PROCESSING_SETTINGS = {
    # TODO: Documentation
    # "Write lists for each boss unfiltered": False,
    # "Write lists for each boss filtered": False,
    # Other options for write_CSV_list to be included

    # CSV table settings
    "Include unscaled estimators": False,  # Default: False  # [MAMOSWINE]
    "Combine attacker movesets": False,  # Combine attacker moves (e.g. FS/BB and Counter/BB Blaziken), Default: True
    "Combine attacker fast moves": True,
    "Include random boss movesets": True,  # Default: True
    "Include specific boss movesets": False,  # Default: False
    "Assign weights to specific boss movesets": False,  # Default: False
    "Include attacker IVs": False,  # Default: False
    "Include fast move type": True,  # Default: False
    "Include charged move type": True,  # Default: False
    "Fill blanks": False,  # Default: True

    "Attackers that should not be combined": [  # Will not combine these attackers' different movesets,
        # displaying each moveset separately. (Remember to INCLUDE SHADOWS & MEGAS separately here!!!)

        # [Bug]
        # "BEEDRILL_MEGA",  # Bug Bite legacy
        # "PINSIR_MEGA",  # One-time only
        # "VIKAVOLT", "GOLISOPOD", "HERACROSS", "HERACROSS_MEGA", "GENESECT", "SCIZOR", "SCIZOR_SHADOW_FORM",
        # "SCIZOR_MEGA", "KLEAVOR",

        # [Dark/Ghost]
        # "GIRATINA_ORIGIN_FORM",  # Permanent
        # "LUNALA", "MARSHADOW", "TYRANITAR", "TYRANITAR_SHADOW_FORM", "TYRANITAR_MEGA", "ABSOL",
        # "ABSOL_SHADOW_FORM", "ABSOL_MEGA", "KROOKODILE", "GRENINJA", "INCINEROAR", "ZARUDE", "DARKRAI", "ZOROARK",
        # "PANGORO", "HOOPA_UNBOUND_FORM", "GRIMMSNARL", "URSHIFU_SINGLE_STRIKE_FORM", "CALYREX_SHADOW_RIDER_FORM",
        # "GYARADOS_MEGA", "DARKRAI_SHADOW_FORM", "HONCHKROW", "HONCHKROW_SHADOW_FORM", "CHIENPAO", "CHIYU",
        # "FLUTTERMANE",

        # [Dragon]
        # "RAYQUAZA_SHADOW_FORM", "PALKIA_SHADOW_FORM", "DIALGA_SHADOW_FORM",  # Mvsts
        # "RAYQUAZA_SHADOW_FORM",  # One-time only
        # "GYARADOS_MEGA",  # Permanent (Dragon Tail is exclusive)
        # "DIALGA_ORIGIN_FORM", "PALKIA_ORIGIN_FORM",  # Permanent? (Depending on how common RoT and SR are)
        # "CHARIZARD_MEGA_X", "CHARIZARD_MEGA_Y", "EXEGGUTOR_ALOLA_FORM", "EXEGGUTOR_ALOLA_SHADOW_FORM", "AMPHAROS_MEGA",
        # "SCEPTILE_MEGA", "ALTARIA_MEGA", "LATIOS_SHADOW_FORM", "LATIOS_MEGA", "DIALGA", "DIALGA_SHADOW_FORM",
        # "PALKIA", "PALKIA_SHADOW_FORM", "HYDREIGON", "HYDREIGON_SHADOW_FORM", "KOMMO_O", "DURALUDON", "ETERNATUS",
        # "RESHIRAM", "RESHIRAM_SHADOW_FORM", "ZEKROM", "ZEKROM_SHADOW_FORM",
        # "GARCHOMP", "GARCHOMP_SHADOW_FORM", "GARCHOMP_MEGA", "DRAGAPULT", "BAXCALIBUR",  # Signature moves
        # # Obsolete: "DRAGONITE", "DRAGONITE_SHADOW_FORM", "SALAMENCE", "SALAMENCE_SHADOW_FORM", "SALAMENCE_MEGA",
        # # Obsolete: "GARCHOMP", "GARCHOMP_SHADOW_FORM", "GARCHOMP_MEGA",

        # [Electric]
        # "THUNDURUS_THERIAN_FORM",  # Permanent?
        # "THUNDURUS_INCARNATE_FORM",  # One-time only?
        # "ZEKROM", "ZEKROM_SHADOW_FORM",   # Permanent (non-legacy moves)
        # "ZAPDOS", "ZAPDOS_SHADOW_FORM",  # Permanent? (non-legacy moves)
        # "JOLTEON", "JOLTEON_SHADOW_FORM", "ZERAORA", "MIRAIDON",
        # "AMPHAROS_MEGA", "LUXRAY", "LUXRAY_SHADOW_FORM", "XURKITREE", "VIKAVOLT", "TAPU_KOKO", "REGIELEKI",

        # [Fairy]
        # "TOGEKISS", "TOGEKISS_SHADOW_FORM", "FLORGES", "SYLVEON", "DIANCIE_MEGA", "PRIMARINA", "TAPU_KOKO", "TAPU_LELE",
        # "XERNEAS", "TAPU_BULU", "MAGEARNA", "GRIMMSNARL", "ZACIAN", "ZACIAN_CROWNED_SWORD_FORM", "IRONVALIANT",
        # "FLUTTERMANE",

        # [Fighting]
        # "MARSHADOW", "HITMONLEE", "HITMONLEE_SHADOW_FORM", "MEWTWO", "MEWTWO_SHADOW_FORM", "MEWTWO_MEGA_X",
        # "BLAZIKEN", "BLAZIKEN_SHADOW_FORM", "BLAZIKEN_MEGA", "GALLADE", "GALLADE_SHADOW_FORM", "GALLADE_MEGA",
        # "LOPUNNY_MEGA", "MIENSHAO", "KELDEO", "MELOETTA_PIROUETTE_FORM", "KOMMO_O", "BUZZWOLE", "ZAPDOS_GALARIAN_FORM",
        # "URSHIFU_SINGLE_STRIKE_FORM", "URSHIFU_RAPID_STRIKE_FORM", "SNEASLER", "MACHAMP", "MACHAMP_SHADOW_FORM",
        # "CONKELDURR", "CONKELDURR_SHADOW_FORM", "SIRFETCHD", "ZAPDOS_GALARIAN_FORM", "HERACROSS", "HERACROSS_MEGA",
        # "HARIYAMA", "HARIYAMA_SHADOW_FORM", "PANGORO", "KORAIDON", "DECIDUEYE_HISUIAN_FORM",

        # [Fire]
        # "HO_OH_SHADOW_FORM",  # One-time only
        # "RESHIRAM", "HEATRAN", "GROUDON_PRIMAL",  # Permanent (non-legacy moves)
        # "BLAZIKEN_MEGA", "CHARIZARD_MEGA_Y",  # Permanent?
        # "BLACEPHALON", "DARMANITAN_GALARIAN_ZEN_FORM", "CHANDELURE", "ENTEI",
        # "CAMERUPT_MEGA", "ENTEI_SHADOW_FORM", "VOLCARONA", "CHANDELURE_SHADOW_FORM", "VOLCARONA_SHADOW_FORM",
        # "GROUDON_PRIMAL", "DARMANITAN", "MOLTRES", "MOLTRES_SHADOW_FORM", "TYPHLOSION_HISUIAN_FORM", "IRONMOTH",

        # [Flying]
        # "HO_OH_SHADOW_FORM",  # One-time only
        # "RAYQUAZA", "RAYQUAZA_SHADOW_FORM", "YVELTAL", "PIDGEOT_MEGA",  # Permanent (maybe except Pidgeot)
        # "HO_OH", "HO_OH_SHADOW_FORM", "LUGIA", "LUGIA_SHADOW_FORM",  # Keep for non-Hidden Power and non-Apex moves
        # "TORNADUS", "TORNADUS_THERIAN_FORM",  # For the Nov'23 run that doesn't include any other speculative moves
        # "SALAMENCE", "SALAMENCE_SHADOW_FORM", "SALAMENCE_MEGA", "AERODACTYL", "AERODACTYL_SHADOW_FORM",
        # "AERODACTYL_MEGA", "CHARIZARD", "CHARIZARD_SHADOW_FORM", "CHARIZARD_MEGA_Y", "ARCHEOPS", "ARCHEOPS_SHADOW_FORM",
        # "PIDGEOT_MEGA", "DRAGONITE", "DRAGONITE_SHADOW_FORM", "ZAPDOS", "ZAPDOS_SHADOW_FORM", "ZAPDOS_GALARIAN_FORM",
        # "MOLTRES", "MOLTRES_SHADOW_FORM", "ARTICUNO_GALARIAN_FORM", "HONCHKROW", "HONCHKROW_SHADOW_FORM",
        # "UNFEZANT", "UNFEZANT_SHADOW_FORM", "TOGEKISS", "TOGEKISS_SHADOW_FORM", "TOUCANNON",
        # "LUGIA", "LUGIA_SHADOW_FORM", "TORNADUS",

        # [Grass]
        # "SCEPTILE_MEGA",  # Permanent?
        # "DECIDUEYE_HISUIAN_FORM",  # One-time only?
        # "RILLABOOM", "TSAREENA", "ZARUDE", "MEOWSCARADA",
        # # Obsolete: "ROSERADE", "ROSERADE_SHADOW_FORM", "SCEPTILE_SHADOW_FORM", "SCEPTILE_MEGA", "SCEPTILE",
        # # Obsolete: "ABOMASNOW_MEGA", "VENUSAUR_MEGA", "VENUSAUR_SHADOW_FORM", "SHAYMIN_SKY_FORM",  "VENUSAUR", "DECIDUEYE",

        # [Ground]
        # "GROUDON", "GROUDON_SHADOW_FORM", "GROUDON_PRIMAL",  # Permanent
        # "GARCHOMP", "GARCHOMP_SHADOW_FORM", "GARCHOMP_MEGA",  # Permanent?
        # "LANDORUS_THERIAN_FORM", "LANDORUS_INCARNATE_FORM",  # Permanent? (At least Therian)
        # "MUDSDALE", "GROUDON_SHADOW_FORM", "RHYPERIOR", "KROOKODILE", "KROOKODILE_SHADOW_FORM",
        # "CAMERUPT_MEGA", "STEELIX_MEGA", "RHYPERIOR_SHADOW_FORM",
        # "GARCHOMP", "GARCHOMP_SHADOW_FORM",
        # # Obsolete: "MAMOSWINE", "MAMOSWINE_SHADOW_FORM", "GOLEM", "GOLEM_SHADOW_FORM", "SWAMPERT",
        # # Obsolete: "SWAMPERT_SHADOW_FORM", "SWAMPERT_MEGA",

        # [Ice]
        # "KYUREM", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "ABOMASNOW_MEGA", "AVALUGG_HISUIAN_FORM",
        # "CRABOMINABLE", "CALYREX_ICE_RIDER_FORM",

        # [Poison]
        # "GENGAR", "GENGAR_SHADOW_FORM", "GENGAR_MEGA", "ETERNATUS", "SALAZZLE", "SNEASLER",

        # [Psychic]
        # "GARDEVOIR_MEGA", "GALLADE_MEGA", "GARDEVOIR_SHADOW_FORM", "GALLADE_SHADOW_FORM", "GARDEVOIR", "GALLADE",  # Synchronoise (one-time only)
        # "NECROZMA", "NECROZMA_DAWN_WINGS_FORM", "NECROZMA_DUSK_MANE_FORM", "NECROZMA_ULTRA_FORM", "DEOXYS",
        # "DEOXYS_ATTACK_FORM", "ARTICUNO_GALARIAN_FORM", "TAPU_LELE", "AZELF", "MELOETTA_ARIA_FORM", "HOOPA",
        # "HATTERENE",

        # [Rock]
        # "RHYPERIOR",  # Also for beginners (Stone Edge), even without MB speculation
        # "RHYPERIOR_SHADOW_FORM", "ARCHEOPS", "AERODACTYL", "AERODACTYL_SHADOW_FORM", "AERODACTYL_MEGA",
        # "STONJOURNER", "DIANCIE_MEGA", "TYRANITAR", "TYRANITAR_SHADOW_FORM", "TYRANITAR_MEGA",
        # "NIHILEGO", "ARCANINE_HISUIAN_FORM", "RAMPARDOS", "RAMPARDOS_SHADOW_FORM", "LYCANROC_MIDDAY_FORM",
        # "KLEAVOR",
        # # Obsolete: "OMASTAR", "OMASTAR_SHADOW_FORM", "GOLEM_SHADOW_FORM", "GOLEM", "GOLEM_ALOLA_FORM",

        # [Steel]
        # "MAGEARNA", "LUCARIO", "LUCARIO_SHADOW_FORM", "LUCARIO_MEGA", "SOLGALEO", "HEATRAN", "GHOLDENGO",
        # "NECROZMA_DUSK_MANE_FORM", "KLINKLANG", "AGGRON", "AGGRON_SHADOW_FORM", "AGGRON_MEGA", "GENESECT", "SCIZOR",
        # "SCIZOR_SHADOW_FORM", "SCIZOR_MEGA", "DIALGA", "DIALGA_ORIGIN_FORM", "EXCADRILL", "MELMETAL", "KARTANA",

        # [Water]
        # "KYOGRE", "KYOGRE_SHADOW_FORM", "KYOGRE_PRIMAL",  # Permanent (non-legacy moves)
        # "FERALIGATR", "FERALIGATR_SHADOW_FORM",  # Water Gun is exclusive
        # "PRIMARINA", "INTELEON", "PALKIA", "PALKIA_SHADOW_FORM", "PALKIA_ORIGIN_FORM", "VOLCANION", "WISHIWASHI_SCHOOL_FORM",
        # "URSHIFU_RAPID_STRIKE_FORM", "SHARPEDO", "SHARPEDO_SHADOW_FORM", "SHARPEDO_MEGA",
        # "GYARADOS", "GYARADOS_SHADOW_FORM", "GYARADOS_MEGA", "SAMUROTT_HISUIAN_FORM",

        # [Utility Metric]
        "ZEKROM_SHADOW_FORM",  # Thunder Fang
        "FLUTTERMANE", "IRONVALIANT",  # Speculative movesets
    ],
}
