"""
Configurations for running the script to generate plots and CSVs.

For convenience, this file stores (or will store) several pre-made "types" of configurations,
so that you don't have to change everything whenever you want to run something different.
"""

from params import *


CONFIG_WRITE_ALL_COUNTERS = True

CONFIG_BATTLE_SETTINGS = {
    # All battle settings that are allowed on Pokebattler counters list page, EXCEPT attacker level.
    # Can accept lists instead of a single value, e.g. "Weather": ["Extreme", "Rainy"],
    # In that case, simulations for all combinations of all specified options will be generated.
    "Friendship": "Best",  # No Friend, Good Friend, Great Friend, Ultra Friend, Best Friend (can omit "Friend")
                           # Default: Best Friend
    "Weather": "Extreme",  # Extreme/No Weather/Neutral, Sunny/Clear, Rainy, Partly Cloudy, Cloudy, Windy, Snow, Fog
                           # Default: Extreme
    "Attack strategy": "No Dodging",  # No Dodging, Dodge Specials PRO, Dodge All Weave
                                      # Default: No Dodging
    "Dodge strategy": "Realistic Dodging"  # Perfect Dodging, Realistic Dodging, Realistic Dodging Pro, 25% Dodging
                                           # Default: Realistic Dodging
}

CONFIG_SORT_OPTION = "Estimator"  # Sorting option as on Pokebattler:
# "Overall", "Power", "Win Rate", "Time to Win", "Potions", "Damage (TDO)", "Estimator"
# Recommended to use either Estimator or TTW; others may not be perfectly supported.

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
    # ----- End of documentation for this section -----

    {
        "Pokemon pool": "By raid tier",  # "All Pokemon", "All Pokemon except above", "By raid tier" or "By raid category"
        "Raid tier": "Tier 5",  # Here, "Tier 5" has all past/present/future bosses
        # "Raid category": "Legacy Tier 5",  # Here, "Tier 5" has only current bosses
        "Filters": {  # Only those without # at the start are applied
            "Weak to contender types": ["Grass"],
            #"Evolution stage": "Final",  # "Final", "Pre-evolution"
            #"Is shadow": False,  # This describes BOSSES, not attackers
            #"Is not shadow": True,
            #"Is mega": False,
            #"Is not mega": True,
            #"Is legendary": False,
            #"Is not legendary": False,
            #"Is mythical": False,
            #"Is not mythical": False,
            #"Is legendary or mythical": False,
            #"Is not legendary or mythical": False,
            # TODO: Add a filter for ignoring certain Pokemon or raids, identified by user
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 50,
        "Forms weight strategy": "combine",  # "combine" or "separate"
    },
    {
        "Pokemon pool": "By raid tier",
        "Raid tier": "Mega Tier",
        "Filters": {
            "Weak to contender types": ["Grass"],
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 25,
        "Forms weight strategy": "combine",
    },
    {
        "Pokemon pool": "By raid tier",
        "Raid tier": "Tier 3",
        "Filters": {
            "Weak to contender types": ["Grass"],
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 15,
        "Forms weight strategy": "combine",
    },
    {
        "Pokemon pool": "All Pokemon except above",
        "Raid tier": "Tier 3",
        # "Raid category": "Legacy Tier 5",
        "Filters": {
            "Weak to contender types": ["Grass"],
            "Evolution stage": "Final",  # "Final", "Pre-evolution"
            "Is not shadow": True,
            "Is not mega": True,
            "Is not legendary or mythical": True,  # Ignores Glastrier etc
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 10,
        "Forms weight strategy": "combine",
    },
]
