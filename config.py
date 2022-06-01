"""
Configurations for running the script to generate plots and CSVs.

For convenience, this file stores (or will store) several pre-made "types" of configurations,
so that you don't have to change everything whenever you want to run something different.
"""

from params import *


#CONFIG_WRITE_ALL_COUNTERS = True

SINGLE_TYPE_ATTACKER = ["Dragon"]
MULTI_TYPE_ATTACKERS_COMPARE = ["Bug", "Ghost", "Dark"]

CONFIG_BATTLE_SETTINGS = {
    # All battle settings that are allowed on Pokebattler counters list page, EXCEPT attacker level.
    # Can accept lists instead of a single value, e.g. "Weather": ["Extreme", "Rainy"],
    # In that case, simulations for all combinations of all specified options will be generated.
    "Weather": "Extreme",  # "Extreme",  # Extreme/No Weather/Neutral, Sunny/Clear, Rainy, Partly Cloudy, Cloudy, Windy, Snow, Fog
                           # Default: Extreme
    "Friendship": "Best",  # No Friend, Good Friend, Great Friend, Ultra Friend, Best Friend (can omit "Friend")
                           # Default: Best Friend
    "Attack strategy": "No Dodging",  # No Dodging, Dodge Specials PRO, Dodge All Weave
                                      # Default: No Dodging
    "Dodge strategy": "Realistic Dodging"  # Perfect Dodging, Realistic Dodging, Realistic Dodging Pro, 25 Percent Dodging
                                           # Default: Realistic Dodging
}

CONFIG_SORT_OPTION = "Estimator"  # Sorting option as on Pokebattler:
# "Overall", "Power", "Win Rate", "Time to Win", "Potions", "Damage (TDO)", "Estimator"
# Recommended to use either Estimator or TTW; others may not be perfectly supported.

CONFIG_ATTACKER_CRITERIA = [
    # Lists of attackers you want to view for analysis.
    # You can specify several sets of criteria, each enclosed by a {} with the format shown below.
    # An attacker will be considered if it satisfies any single {} block.
    # To use a filter, delete the first # at the start of the line, and then change the value as you wish.
    # To drop a filter, add back the # at the start of the line.
    {
        # Each block contains several filters. To meet the criteria for this particular {} block,
        # an attacker needs to pass all the filters (example: Ice charged move, levels 30-50, AND non-shadow).
        "Charged move types": SINGLE_TYPE_ATTACKER,
        #"Charged move types": MULTI_TYPE_ATTACKERS_COMPARE,
                                          # This is an approximation for "attacker type",
                                          # and should be used primarily for type-based filtering.
                                          # Always put "" around type names!
        "Min level": 40,
        "Max level": 40,
        "Level step size": 5,  # Can be as low as 0.5, but recommend 5 for efficiency
        # "Pokemon code names": [],  # Specific Pokemon to be considered,
            # e.g. "MEWTWO", "VENUSAUR_SHADOW_FORM", "RAICHU_ALOLA_FORM",
            # "SLOWBRO_GALARIAN_FORM", "CHARIZARD_MEGA_Y"
            # NOTE: This does NOT guarantee the required Pokemon will be on the counters list,
            # especially if the Pokemon is too weak to be in top 32 against bosses.
            # To guarantee results, add it to your Pokebox and use "Trainer ID" option instead.
        # "Trainer ID": 52719,  # Pokebattler trainer ID
        #                       # If this is provided, only Pokemon from that Trainer's Pokebox are used
        # "Must be shadow": False,  # This describes attackers, not bosses
        # "Must be non shadow": True,
        # "Must be mega": True,
        # "Must be non mega": True,
        # "Must be legendary": False,
        # "Must be non legendary": True,
        # "Must be mythical": False,
        # "Must be non mythical": True,
        # "Must be legendary or mythical": False,
        # "Must be non legendary or mythical": False,
        "Pokemon types": SINGLE_TYPE_ATTACKER,  # Only use this if you know what you're doing
        #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE,
        # "Fast move types": ["Flying"],  # Only use this if you know what you're doing
        "Exclude": ["LUCARIO_MEGA", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "MEWTWO_MEGA_X", "MEWTWO_MEGA_Y",
                    "LATIAS_MEGA", "LATIOS_MEGA"],  # Specific Pokemon to be excluded,
            # in the same format as "Pokemon code names", e.g. "VENUSAUR_SHADOW_FORM"
    },
    {
        "Trainer ID": 52719,
        "Charged move types": SINGLE_TYPE_ATTACKER,
        #"Charged move types": MULTI_TYPE_ATTACKERS_COMPARE,
        "Pokemon types": SINGLE_TYPE_ATTACKER,  # Only use this if you know what you're doing
        #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE,
        # "Fast move types": ["Fire"],  # Only use this if you know what you're doing
    },

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

    {
        "Pokemon pool": "By raid tier",  # "All Pokemon", "All Pokemon except above", "By raid tier" or "By raid category"
        #"Raid tier": "Tier 5",  # Here, "Tier 5" has all past/present/future bosses
        "Raid tiers": ["Tier 5", "Ultra Beast Tier"],
        # "Raid category": "Legacy Tier 5",  # Here, "Tier 5" has only current bosses
        "Filters": {  # Only those without # at the start are applied
            "Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
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
        "Weight of whole group": 50,
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
    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Tier 5", "Ultra Beast Tier"],
        "Filters": {
            "Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 0,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Attack strategy": "Dodge Specials PRO",
        },
    },

    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
        "Filters": {
            "Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 35,  #25,
        "Forms weight strategy": "combine",
    },
    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
        "Filters": {
            "Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 0,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Attack strategy": "Dodge Specials PRO",
        },
    },

    {
        "Pokemon pool": "By raid tier",
        "Raid tier": "Tier 3",
        "Filters": {
            "Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 15,  #25,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Friendship": "No",
        },
        "Baseline battle settings": {
            "Friendship": "No",
        }
    },
    {
        "Pokemon pool": "By raid tier",
        "Raid tier": "Tier 3",
        "Filters": {
            "Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 0,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Friendship": "No",
            "Attack strategy": "Dodge Specials PRO",
        },
        "Baseline battle settings": {
            "Friendship": "No",
        }
    },

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
    #         "Friendship": "No",
    #     },
    # },

    {
        "Pokemon pool": "All Pokemon except above",
        "Raid tiers": ["Tier 3", "Tier 5"],
        # "Raid category": "Legacy Tier 5",
        "Filters": {
            "Weak to contender types": ["Dragon"],
            "Evolution stage": "Final",  # "Final", "Pre-evolution"
            "Must be non shadow": True,
            "Must be non mega": True,
            "Must be non legendary or mythical": True,  # Ignores Glastrier etc
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 10,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Friendship": "No",
        },
    },
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
    # ----- End of documentation for this section -----

    "Enabled": True,  # Default: True
    "Baseline chosen before filter": False,  # Default: False
    "Baseline boss moveset": "random",  # "random", "easiest", "hardest"
    "Baseline attacker level": 40,  # Specific level, "min", "max", "average", "by level"/-1/None
    "Baseline battle settings": {
        "Weather": "Extreme",
        "Friendship": "Best",
        "Attack strategy": "No Dodging",
        "Dodge strategy": "Realistic Dodging",
    }
}


CONFIG_PROCESSING_SETTINGS = {
    # TODO: Documentation
    # "Write lists for each boss unfiltered": False,
    # "Write lists for each boss filtered": False,
    # Other options for write_CSV_list to be included

    # CSV table settings
    "Include unscaled estimators": True, #False,  # Default: False
    "Combine attacker movesets": False,  # Combine attacker moves (e.g. FS/BB and Counter/BB Blaziken), Default: True
    "Include random boss movesets": True,  # Default: True
    "Include specific boss movesets": False,  # Default: False
    "Include attacker IVs": False,  # Default: False
}
