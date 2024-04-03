"""
Configurations for running the script to generate plots and CSVs.

For convenience, this file stores (or will store) several pre-made "types" of configurations,
so that you don't have to change everything whenever you want to run something different.
"""

from params import *


#CONFIG_WRITE_ALL_COUNTERS = True

SINGLE_TYPE_ATTACKER = ["Flying"]
MULTI_TYPE_ATTACKERS_COMPARE = ["Water", "Grass"]  # Use this for Dark/Ghost
# Ground/Steel, Ground/Fire, Ground/Fighting, Ground/Water/Rock, Water/Steel, Water/Grass
EXTRA_TYPE_ATTACKER = ["Dark"]  # Attacker types that use non-STAB moves, doesn't apply to moves
    # Dark/Ghost: Psychic (Mewtwo, Mega Alakazam)
    # Dragon: Fire, Water (Mega Charizard Y, Mega Gyarados)
    # Electric: Psychic, Water (Mewtwo, Primal Kyogre)
    # Fairy: Electric, Psychic, Ice, Ground (Xurkitree, Mega Alakazam, Lunala, Beartic, Donphan)
    # Fighting: Psychic (Mega Alakazam)
    # Fire: Psychic (Mewtwo)
    # Flying: Grass (Kartana AS/AA)
    # Grass: Electric, Ground (Xurkitree, Primal Groudon)
    # Ice: Psychic, Water (Mewtwo, Primal Kyogre)
    # Poison: Dark (Darkrai)
    # Rock: Ground (Landorus-I RT/RS)
MODE = "SINGLE"  # SINGLE, SINGLE+, MULTI, MULTI+  (Use MULTI+ for DARK GHOST)

#CONFIG_SORT_OPTION = "Estimator"
CONFIG_SORT_OPTIONS = ["Estimator", "TTW"]
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
    {
        # Each block contains several filters. To meet the criteria for this particular {} block,
        # an attacker needs to pass all the filters (example: Ice charged move, levels 30-50, AND non-shadow).
        #"Charged move types": SINGLE_TYPE_ATTACKER,
        #"Charged move types": MULTI_TYPE_ATTACKERS_COMPARE,
        "Charged move types": get_move_types(),
                                          # This is an approximation for "attacker type",
                                          # and should be used primarily for type-based filtering.
                                          # Always put "" around type names!
        "Min level": 30,
        "Max level": 50,
        "Level step size": 5, #5,  # Can be as low as 0.5, but recommend 5 for efficiency
        # "Pokemon code names": [],  # Specific Pokemon to be considered,
            # e.g. "MEWTWO", "VENUSAUR_SHADOW_FORM", "RAICHU_ALOLA_FORM",
            # "SLOWBRO_GALARIAN_FORM", "CHARIZARD_MEGA_Y"
            # NOTE: This does NOT guarantee the required Pokemon will be on the counters list,
            # especially if the Pokemon is too weak to be in top 32 against bosses.
            # To guarantee results, use "Pokemon code names and moves" instead.
        #"Pokemon code names and moves": [],
            # Specific Pokemon and movesets to be considered, as a list of tuples. Possibly including IVs.
            # e.g. [
            #     ("URSALUNA", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
            #     ("URSALUNA", "TACKLE_FAST", "HIGH_HORSEPOWER"),
            #     ("GOLURK_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
            #     ("GARCHOMP_MEGA", "MUD_SHOT_FAST", "EARTH_POWER", "10/10/10"),
            #     ...
            # ]
            # This DOES guarantee the required Pokemon will be on the counters list.
            # Use this option if you want to test unreleased Pokemon or movesets, or Pokemon that are too weak
            # to appear on any of the top 32 lists.
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
        #"Pokemon types": SINGLE_TYPE_ATTACKER,  # Only use this if you know what you're doing
        #"Pokemon types": SINGLE_TYPE_ATTACKER + ["Psychic"],  # Only use this if you know what you're doing
        #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE,
        #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE + ["Psychic"],
        "Pokemon types": get_pokemon_types(),
        # "Fast move types": ["Flying"],  # Only use this if you know what you're doing
        "Exclude": ["LUCARIO_MEGA", "KYUREM_BLACK_FORM", "KYUREM_WHITE_FORM", "MEWTWO_MEGA_X", "MEWTWO_MEGA_Y",
                    "CALYREX_SHADOW_RIDER_FORM", "BLACEPHALON", "ETERNATUS", "ETERNATUS_ETERNAMAX_FORM"],
            # Specific Pokemon to be excluded,
            # in the same format as "Pokemon code names", e.g. "VENUSAUR_SHADOW_FORM"
    },
    # {
    #     "Trainer ID": 52719,
    #     #"Charged move types": SINGLE_TYPE_ATTACKER,
    #     #"Charged move types": MULTI_TYPE_ATTACKERS_COMPARE,
    #     "Charged move types": get_move_types(),
    #     #"Pokemon types": SINGLE_TYPE_ATTACKER,  # Only use this if you know what you're doing
    #     #"Pokemon types": SINGLE_TYPE_ATTACKER + ["Psychic"],  # Only use this if you know what you're doing
    #     #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE,
    #     #"Pokemon types": MULTI_TYPE_ATTACKERS_COMPARE + ["Psychic"],
    #     "Pokemon types": get_pokemon_types(),
    #     # "Fast move types": ["Fire"],  # Only use this if you know what you're doing
    # },
    {
        "Min level": 30,
        "Max level": 50,
        "Level step size": 5,
        "Pokemon code names and moves": [
            # ("ROSERADE", "RAZOR_LEAF_FAST", "GRASS_KNOT"),
            # ("VENUSAUR", "VINE_WHIP_FAST", "FRENZY_PLANT"),
            # ("ROSERADE_SHADOW_FORM", "RAZOR_LEAF_FAST", "GRASS_KNOT"),
            # ("VENUSAUR_SHADOW_FORM", "VINE_WHIP_FAST", "FRENZY_PLANT"),
            # ("VENUSAUR_MEGA", "VINE_WHIP_FAST", "FRENZY_PLANT"),
            # ("VICTREEBEL_SHADOW_FORM", "RAZOR_LEAF_FAST", "LEAF_BLADE"),
            # ("SHIFTRY_SHADOW_FORM", "RAZOR_LEAF_FAST", "LEAF_BLADE"),
            # ("ZARUDE", "RAZOR_LEAF_FAST", "LEAF_BLADE"),
            # ("TANGROWTH", "VINE_WHIP_FAST", "POWER_WHIP"),
            # ("SCEPTILE", "BULLET_SEED_FAST", "FRENZY_PLANT"),
            # ("TANGROWTH_SHADOW_FORM", "VINE_WHIP_FAST", "POWER_WHIP"),
            # ("SCEPTILE_SHADOW_FORM", "BULLET_SEED_FAST", "FRENZY_PLANT"),
            # ("TANGELA_SHADOW_FORM", "VINE_WHIP_FAST", "GRASS_KNOT"),
            # ("MEGANIUM_SHADOW_FORM", "VINE_WHIP_FAST", "FRENZY_PLANT"),
            # ("LEAFEON", "RAZOR_LEAF_FAST", "LEAF_BLADE"),
            # ("TORTERRA_SHADOW_FORM", "RAZOR_LEAF_FAST", "FRENZY_PLANT"),
            # ("TORTERRA", "RAZOR_LEAF_FAST", "FRENZY_PLANT"),
            # ("EXEGGUTOR_SHADOW_FORM", "BULLET_SEED_FAST", "SOLAR_BEAM"),
            # ("EXEGGUTOR", "BULLET_SEED_FAST", "SOLAR_BEAM"),
            # ("CELEBI", "MAGICAL_LEAF_FAST", "LEAF_STORM"),
            # ("CHESNAUGHT", "VINE_WHIP_FAST", "FRENZY_PLANT"),
            # ("BRELOOM", "BULLET_SEED_FAST", "GRASS_KNOT"),

            # ("CHARIZARD", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("CHARIZARD_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("CHARIZARD_MEGA_Y", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("BLAZIKEN", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("EMBOAR", "EMBER_FAST", "BLAST_BURN"),
            # ("INFERNAPE", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("BLAZIKEN_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("EMBOAR_SHADOW_FORM", "EMBER_FAST", "BLAST_BURN"),
            # ("INFERNAPE_SHADOW_FORM", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("BLAZIKEN_MEGA", "FIRE_SPIN_FAST", "BLAST_BURN"),
            # ("DARMANITAN_STANDARD_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
            # ("ENTEI", "FIRE_FANG_FAST", "OVERHEAT"),
            # ("ENTEI_SHADOW_FORM", "FIRE_FANG_FAST", "OVERHEAT"),
            # ("FLAREON", "FIRE_SPIN_FAST", "OVERHEAT"),
            # ("MOLTRES", "FIRE_SPIN_FAST", "OVERHEAT"),
            # ("HO_OH", "INCINERATE_FAST", "SACRED_FIRE"),
            # ("HO_OH", "INCINERATE_FAST", "SACRED_FIRE_PLUS"),
            # ("HO_OH", "INCINERATE_FAST", "SACRED_FIRE_PLUS_PLUS"),
            # ("MOLTRES_SHADOW_FORM", "FIRE_SPIN_FAST", "OVERHEAT"),
            # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE"),
            # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE_PLUS"),
            # ("HO_OH_SHADOW_FORM", "INCINERATE_FAST", "SACRED_FIRE_PLUS_PLUS"),
            # ("HOUNDOOM_SHADOW_FORM", "FIRE_FANG_FAST", "FLAMETHROWER"),
            # ("HOUNDOOM_MEGA", "FIRE_FANG_FAST", "FLAMETHROWER"),
            # ("TYPHLOSION", "INCINERATE_FAST", "BLAST_BURN"),
            # ("MAGMORTAR", "FIRE_SPIN_FAST", "FIRE_PUNCH"),
            # ("ARCANINE", "FIRE_FANG_FAST", "FLAMETHROWER"),
            # ("TYPHLOSION_SHADOW_FORM", "INCINERATE_FAST", "BLAST_BURN"),
            # ("MAGMORTAR_SHADOW_FORM", "FIRE_SPIN_FAST", "FIRE_PUNCH"),
            # ("ARCANINE_SHADOW_FORM", "FIRE_FANG_FAST", "FLAMETHROWER"),

            # ("SWAMPERT", "WATER_GUN_FAST", "HYDRO_CANNON"),
            # ("SWAMPERT_SHADOW_FORM", "WATER_GUN_FAST", "HYDRO_CANNON"),
            # ("SWAMPERT_MEGA", "WATER_GUN_FAST", "HYDRO_CANNON"),
            # ("BLASTOISE_MEGA", "WATER_GUN_FAST", "HYDRO_CANNON"),
            # ("FERALIGATR_SHADOW_FORM", "WATER_GUN_FAST", "HYDRO_CANNON"),
            # ("KYOGRE", "WATERFALL_FAST", "ORIGIN_PULSE"),
            # ("KYOGRE", "WATERFALL_FAST", "SURF"),
            # ("KINGLER", "BUBBLE_FAST", "CRABHAMMER"),
            # ("SAMUROTT", "WATERFALL_FAST", "HYDRO_CANNON"),
            # ("FERALIGATR", "WATERFALL_FAST", "HYDRO_CANNON"),
            # ("CLAWITZER", "WATER_GUN_FAST", "CRABHAMMER"),
            # ("BLASTOISE_SHADOW_FORM", "WATER_GUN_FAST", "HYDRO_CANNON"),
            # ("GYARADOS_MEGA", "WATERFALL_FAST", "AQUA_TAIL"),
            # ("CRAWDAUNT", "WATERFALL_FAST", "CRABHAMMER"),
            # ("GYARADOS", "WATERFALL_FAST", "HYDRO_PUMP"),
            # ("GYARADOS_SHADOW_FORM", "WATERFALL_FAST", "HYDRO_PUMP"),

            # ("XURKITREE", "THUNDER_SHOCK_FAST", "DISCHARGE"),
            # ("XURKITREE", "SPARK_FAST", "DISCHARGE"),
            # ("XURKITREE", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
            # ("XURKITREE", "SPARK_FAST", "WILD_CHARGE"),
            # ("RAIKOU", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
            # ("ELECTIVIRE", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
            # ("LUXRAY", "SPARK_FAST", "WILD_CHARGE"),
            # ("RAIKOU_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
            # ("ELECTIVIRE_SHADOW_FORM", "THUNDER_SHOCK_FAST", "WILD_CHARGE"),
            # ("LUXRAY_SHADOW_FORM", "SPARK_FAST", "WILD_CHARGE"),
            # ("MANECTRIC_MEGA", "THUNDER_FANG_FAST", "WILD_CHARGE"),
            # ("MANECTRIC_SHADOW_FORM", "THUNDER_FANG_FAST", "WILD_CHARGE"),
            # ("ZEKROM", "CHARGE_BEAM_FAST", "FUSION_BOLT"),
            # ("AMPHAROS_MEGA", "VOLT_SWITCH_FAST", "ZAP_CANNON"),
            # ("THUNDURUS_THERIAN_FORM", "VOLT_SWITCH_FAST", "THUNDERBOLT"),
            # ("ZAPDOS", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),
            # ("ZAPDOS_SHADOW_FORM", "THUNDER_SHOCK_FAST", "THUNDERBOLT"),
            # ("MAGNEZONE_SHADOW_FORM", "SPARK_FAST", "WILD_CHARGE"),
            # ("MAGNEZONE", "SPARK_FAST", "WILD_CHARGE"),
            # ("MAGNETON_SHADOW_FORM", "THUNDER_SHOCK_FAST", "DISCHARGE"),

            # ("MAMOSWINE_SHADOW_FORM", "POWDER_SNOW_FAST", "AVALANCHE"),
            # ("MAMOSWINE", "POWDER_SNOW_FAST", "AVALANCHE"),
            # ("PILOSWINE_SHADOW_FORM", "POWDER_SNOW_FAST", "AVALANCHE"),
            # ("WEAVILE_SHADOW_FORM", "ICE_SHARD_FAST", "AVALANCHE"),
            # ("WEAVILE", "ICE_SHARD_FAST", "AVALANCHE"),
            # ("SNEASEL_SHADOW_FORM", "ICE_SHARD_FAST", "AVALANCHE"),
            # ("DARMANITAN_GALARIAN_STANDARD_FORM", "ICE_FANG_FAST", "AVALANCHE"),
            # ("GLALIE_MEGA", "FROST_BREATH_FAST", "AVALANCHE"),
            # ("GLACEON", "FROST_BREATH_FAST", "AVALANCHE"),
            # ("AVALUGG", "ICE_FANG_FAST", "AVALANCHE"),
            # ("BEARTIC", "POWDER_SNOW_FAST", "ICE_PUNCH"),
            # ("ABOMASNOW_MEGA", "POWDER_SNOW_FAST", "WEATHER_BALL_ICE"),
            # ("ABOMASNOW_SHADOW_FORM", "POWDER_SNOW_FAST", "WEATHER_BALL_ICE"),
            # ("ARTICUNO_SHADOW_FORM", "FROST_BREATH_FAST", "ICE_BEAM"),
            # ("ARTICUNO", "FROST_BREATH_FAST", "ICE_BEAM"),

            # ("AERODACTYL", "ROCK_THROW_FAST", "ROCK_SLIDE"),
            # ("AERODACTYL_SHADOW_FORM", "ROCK_THROW_FAST", "ROCK_SLIDE"),
            # ("AERODACTYL_MEGA", "ROCK_THROW_FAST", "ROCK_SLIDE"),
            # ("TYRANITAR_SHADOW_FORM", "SMACK_DOWN_FAST", "STONE_EDGE"),
            # ("TYRANITAR", "SMACK_DOWN_FAST", "STONE_EDGE"),
            # ("RAMPARDOS", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            # ("GIGALITH", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            # ("GIGALITH", "SMACK_DOWN_FAST", "METEOR_BEAM"),
            # ("RAMPARDOS_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            # ("GIGALITH_SHADOW_FORM", "SMACK_DOWN_FAST", "ROCK_SLIDE"),
            # ("GIGALITH_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
            # ("AGGRON_SHADOW_FORM", "SMACK_DOWN_FAST", "METEOR_BEAM"),
            # ("AGGRON", "SMACK_DOWN_FAST", "METEOR_BEAM"),
            # ("GOLEM_SHADOW_FORM", "ROCK_THROW_FAST", "STONE_EDGE"),
            # ("RHYPERIOR", "SMACK_DOWN_FAST", "STONE_EDGE"),
            # ("RHYPERIOR", "SMACK_DOWN_FAST", "ROCK_WRECKER"),
            # ("GOLEM", "ROCK_THROW_FAST", "STONE_EDGE"),

            # ("MAMOSWINE_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("MAMOSWINE", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("GROUDON", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
            # ("GROUDON", "MUD_SHOT_FAST", "EARTHQUAKE"),
            # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "PRECIPICE_BLADES"),
            # ("GROUDON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE"),
            # ("DONPHAN", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("DONPHAN_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("SWAMPERT_MEGA", "MUD_SHOT_FAST", "EARTHQUAKE"),
            # ("SWAMPERT_SHADOW_FORM", "MUD_SHOT_FAST", "EARTHQUAKE"),
            # ("SWAMPERT", "MUD_SHOT_FAST", "EARTHQUAKE"),
            # ("GARCHOMP", "MUD_SHOT_FAST", "EARTH_POWER"),
            # ("GARCHOMP_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
            # ("FLYGON", "MUD_SHOT_FAST", "EARTH_POWER"),
            # ("FLYGON_SHADOW_FORM", "MUD_SHOT_FAST", "EARTH_POWER"),
            # ("GOLURK_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
            # ("GOLURK", "MUD_SLAP_FAST", "EARTH_POWER"),
            # ("RHYPERIOR", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("RHYDON", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("RHYPERIOR_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("RHYDON_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("GOLEM_SHADOW_FORM", "MUD_SLAP_FAST", "EARTHQUAKE"),
            # ("GOLEM", "MUD_SLAP_FAST", "EARTHQUAKE"),

            # ("METAGROSS_SHADOW_FORM", "BULLET_PUNCH_FAST", "METEOR_MASH"),
            # ("METAGROSS", "BULLET_PUNCH_FAST", "METEOR_MASH"),
            # ("GENESECT", "METAL_CLAW_FAST", "MAGNET_BOMB"),
            # ("SCIZOR", "BULLET_PUNCH_FAST", "IRON_HEAD"),
            # ("SCIZOR_SHADOW_FORM", "BULLET_PUNCH_FAST", "IRON_HEAD"),
            # ("SCIZOR_MEGA", "BULLET_PUNCH_FAST", "IRON_HEAD"),
            # ("DURANT", "METAL_CLAW_FAST", "IRON_HEAD"),
            # ("EXCADRILL", "METAL_CLAW_FAST", "IRON_HEAD"),
            # ("STEELIX_MEGA", "IRON_TAIL_FAST", "HEAVY_SLAM"),
            # ("AGGRON_SHADOW_FORM", "IRON_TAIL_FAST", "HEAVY_SLAM"),
            # ("AGGRON", "IRON_TAIL_FAST", "HEAVY_SLAM"),

            # ("GENESECT", "FURY_CUTTER_FAST", "X_SCISSOR"),
            # ("SCIZOR", "FURY_CUTTER_FAST", "X_SCISSOR"),
            # ("SCIZOR_SHADOW_FORM", "FURY_CUTTER_FAST", "X_SCISSOR"),
            # ("SCIZOR_MEGA", "FURY_CUTTER_FAST", "X_SCISSOR"),
            # ("DURANT", "BUG_BITE_FAST", "X_SCISSOR"),
            # ("BEEDRILL_MEGA", "BUG_BITE_FAST", "X_SCISSOR"),
            # ("VENOMOTH_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),
            # ("PINSIR", "BUG_BITE_FAST", "X_SCISSOR"),
            # ("ACCELGOR", "INFESTATION_FAST", "BUG_BUZZ"),
            # ("PINSIR_SHADOW_FORM", "BUG_BITE_FAST", "X_SCISSOR"),
            # ("ACCELGOR_SHADOW_FORM", "INFESTATION_FAST", "BUG_BUZZ"),
            # ("YANMEGA", "BUG_BITE_FAST", "BUG_BUZZ"),
            # ("SCYTHER", "FURY_CUTTER_FAST", "BUG_BUZZ"),
            # ("YANMEGA_SHADOW_FORM", "BUG_BITE_FAST", "BUG_BUZZ"),
            # ("SCYTHER_SHADOW_FORM", "FURY_CUTTER_FAST", "BUG_BUZZ"),

            # ("BEEDRILL_MEGA", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("SCOLIPEDE", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("ROSERADE", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("VICTREEBEL", "ACID_FAST", "SLUDGE_BOMB"),
            # ("VILEPLUME", "ACID_FAST", "SLUDGE_BOMB"),
            # ("ROSERADE_SHADOW_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("VICTREEBEL_SHADOW_FORM", "ACID_FAST", "SLUDGE_BOMB"),
            # ("VILEPLUME_SHADOW_FORM", "ACID_FAST", "SLUDGE_BOMB"),
            # ("OVERQWIL", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("SKUNTANK", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("SKUNTANK_SHADOW_FORM", "POISON_JAB_FAST", "SLUDGE_BOMB"),
            # ("DRAPION_SHADOW_FORM", "POISON_STING_FAST", "SLUDGE_BOMB"),

            ("MOLTRES_SHADOW_FORM", "WING_ATTACK_FAST", "SKY_ATTACK"),
            ("MOLTRES", "WING_ATTACK_FAST", "SKY_ATTACK"),
            ("STARAPTOR", "GUST_FAST", "BRAVE_BIRD"),
            ("BRAVIARY", "AIR_SLASH_FAST", "BRAVE_BIRD"),
            ("STARAPTOR_SHADOW_FORM", "GUST_FAST", "BRAVE_BIRD"),
            ("BRAVIARY_SHADOW_FORM", "AIR_SLASH_FAST", "BRAVE_BIRD"),
            ("PIDGEOT_MEGA", "GUST_FAST", "BRAVE_BIRD"),
            ("HONCHKROW_SHADOW_FORM", "PECK_FAST", "SKY_ATTACK"),
            ("HONCHKROW", "PECK_FAST", "SKY_ATTACK"),
            ("UNFEZANT", "AIR_SLASH_FAST", "SKY_ATTACK"),
            ("UNFEZANT_SHADOW_FORM", "AIR_SLASH_FAST", "SKY_ATTACK"),
            ("TOUCANNON", "PECK_FAST", "DRILL_PECK"),
            ("RAYQUAZA", "AIR_SLASH_FAST", "HURRICANE"),
            ("NOIVERN", "AIR_SLASH_FAST", "HURRICANE"),
            ("YVELTAL", "GUST_FAST", "HURRICANE"),
            ("MOLTRES_GALARIAN_FORM", "WING_ATTACK_FAST", "BRAVE_BIRD"),
            ("TORNADUS_INCARNATE_FORM", "AIR_SLASH_FAST", "HURRICANE"),
            ("TORNADUS_THERIAN_FORM", "GUST_FAST", "HURRICANE"),
            # Speculative
            ("CHARIZARD", "WING_ATTACK_FAST", "FLY"),
            ("CHARIZARD", "AIR_SLASH_FAST", "FLY"),
            ("CHARIZARD_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
            ("CHARIZARD_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
            ("CHARIZARD_MEGA_Y", "WING_ATTACK_FAST", "FLY"),
            ("CHARIZARD_MEGA_Y", "AIR_SLASH_FAST", "FLY"),
            ("AERODACTYL", "WING_ATTACK_FAST", "FLY"),
            ("AERODACTYL_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
            ("AERODACTYL_MEGA", "WING_ATTACK_FAST", "FLY"),
            ("DRAGONITE", "WING_ATTACK_FAST", "FLY"),
            ("DRAGONITE_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),
            ("ZAPDOS", "PECK_FAST", "DRILL_PECK"),
            ("ZAPDOS_SHADOW_FORM", "PECK_FAST", "DRILL_PECK"),
            ("LUGIA", "GUST_FAST", "AEROBLAST"),
            ("LUGIA", "GUST_FAST", "AEROBLAST_PLUS_PLUS"),
            ("LUGIA_SHADOW_FORM", "GUST_FAST", "AEROBLAST"),
            ("LUGIA_SHADOW_FORM", "GUST_FAST", "AEROBLAST_PLUS"),
            ("HO_OH", "GUST_FAST", "BRAVE_BIRD"),
            ("HO_OH_SHADOW_FORM", "GUST_FAST", "BRAVE_BIRD"),
            ("SALAMENCE", "AIR_SLASH_FAST", "FLY"),
            ("SALAMENCE_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
            ("SALAMENCE_MEGA", "AIR_SLASH_FAST", "FLY"),
            ("RAYQUAZA", "AIR_SLASH_FAST", "FLY"),
            ("RAYQUAZA_SHADOW_FORM", "AIR_SLASH_FAST", "FLY"),
            ("RAYQUAZA_MEGA", "AIR_SLASH_FAST", "FLY"),
            ("ARCHEOPS", "WING_ATTACK_FAST", "FLY"),
            ("ARCHEOPS_SHADOW_FORM", "WING_ATTACK_FAST", "FLY"),


            # ("RAYQUAZA", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("RAYQUAZA", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
            # ("SALAMENCE", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("SALAMENCE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
            # ("DRAGONITE", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
            # ("DRAGONITE", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
            # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("RAYQUAZA_SHADOW_FORM", "DRAGON_TAIL_FAST", "BREAKING_SWIPE"),
            # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("SALAMENCE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
            # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRACO_METEOR"),
            # ("DRAGONITE_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),
            # ("LATIOS", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
            # ("LATIAS", "DRAGON_BREATH_FAST", "OUTRAGE"),
            # ("LATIOS_SHADOW_FORM", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
            # ("LATIAS_SHADOW_FORM", "DRAGON_BREATH_FAST", "OUTRAGE"),
            # ("LATIOS_MEGA", "DRAGON_BREATH_FAST", "DRAGON_CLAW"),
            # ("LATIAS_MEGA", "DRAGON_BREATH_FAST", "OUTRAGE"),
            # ("GARCHOMP", "DRAGON_TAIL_FAST", "OUTRAGE"),
            # ("FLYGON_SHADOW_FORM", "DRAGON_TAIL_FAST", "DRAGON_CLAW"),

            # ("BLAZIKEN_MEGA", "COUNTER_FAST", "FOCUS_BLAST"),
            # ("BLAZIKEN_SHADOW_FORM", "COUNTER_FAST", "FOCUS_BLAST"),
            # ("BLAZIKEN", "COUNTER_FAST", "FOCUS_BLAST"),
            # ("EMBOAR", "LOW_KICK_FAST", "FOCUS_BLAST"),
            # ("KELDEO", "LOW_KICK_FAST", "SACRED_SWORD"),
            # ("POLIWRATH_SHADOW_FORM", "ROCK_SMASH_FAST", "DYNAMIC_PUNCH"),
            # ("CONKELDURR", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("MACHAMP", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("HARIYAMA", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("CONKELDURR_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("MACHAMP_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("HARIYAMA_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("LUCARIO", "COUNTER_FAST", "AURA_SPHERE"),
            # ("COBALION", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
            # ("LUCARIO_SHADOW_FORM", "COUNTER_FAST", "AURA_SPHERE"),
            # ("COBALION_SHADOW_FORM", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
            # ("BRELOOM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("VIRIZION", "DOUBLE_KICK_FAST", "SACRED_SWORD"),
            # ("BRELOOM_SHADOW_FORM", "COUNTER_FAST", "DYNAMIC_PUNCH"),
            # ("VIRIZION_SHADOW_FORM", "DOUBLE_KICK_FAST", "SACRED_SWORD"),

            # ("MEWTWO", "CONFUSION_FAST", "PSYSTRIKE"),
            # ("MEWTWO", "CONFUSION_FAST", "PSYCHIC"),
            # ("ESPEON", "CONFUSION_FAST", "PSYCHIC"),
            # ("ALAKAZAM", "CONFUSION_FAST", "PSYCHIC"),
            # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYSTRIKE"),
            # ("MEWTWO_SHADOW_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # ("ESPEON_SHADOW_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # ("ALAKAZAM_SHADOW_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # ("ALAKAZAM_MEGA", "CONFUSION_FAST", "PSYCHIC"),
            # ("LATIOS", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("LATIAS", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("LATIOS_SHADOW_FORM", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("LATIAS_SHADOW_FORM", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("LATIOS_MEGA", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("LATIAS_MEGA", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("GALLADE", "CONFUSION_FAST", "PSYCHIC"),
            # ("GALLADE_SHADOW_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # ("GALLADE_MEGA", "CONFUSION_FAST", "PSYCHIC"),
            # ("GARDEVOIR", "CONFUSION_FAST", "PSYCHIC"),
            # ("GARDEVOIR_SHADOW_FORM", "CONFUSION_FAST", "PSYCHIC"),
            # ("GARDEVOIR_MEGA", "CONFUSION_FAST", "PSYCHIC"),
            # ("METAGROSS", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("METAGROSS_SHADOW_FORM", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("METAGROSS_MEGA", "ZEN_HEADBUTT_FAST", "PSYCHIC"),
            # ("LUNALA", "CONFUSION_FAST", "PSYCHIC"),
            # ("HOOPA_CONFINED_FORM", "CONFUSION_FAST", "PSYCHIC"),

            # ("GENGAR_MEGA", "LICK_FAST", "SHADOW_BALL"),
            # ("GENGAR_MEGA", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("GENGAR_SHADOW_FORM", "LICK_FAST", "SHADOW_BALL"),
            # ("GENGAR_SHADOW_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("GENGAR", "LICK_FAST", "SHADOW_BALL"),
            # ("GENGAR", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("BANETTE", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("MISMAGIUS", "HEX_FAST", "SHADOW_BALL"),
            # ("BANETTE_SHADOW_FORM", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("BANETTE_MEGA", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("MISMAGIUS_SHADOW_FORM", "HEX_FAST", "SHADOW_BALL"),
            # ("GIRATINA_ORIGIN_FORM", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
            # ("GIRATINA_ALTERED_FORM", "SHADOW_CLAW_FAST", "SHADOW_FORCE"),
            # ("TREVENANT", "SHADOW_CLAW_FAST", "SHADOW_BALL"),
            # ("GOURGEIST_SMALL_FORM", "HEX_FAST", "SHADOW_BALL"),
            # ("GOURGEIST_AVERAGE_FORM", "HEX_FAST", "SHADOW_BALL"),
            # ("GOURGEIST_LARGE_FORM", "HEX_FAST", "SHADOW_BALL"),
            # ("GOURGEIST_SUPER_FORM", "HEX_FAST", "SHADOW_BALL"),

            # ("HOUNDOOM", "SNARL_FAST", "FOUL_PLAY"),
            # ("HOUNDOOM_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
            # ("HOUNDOOM_MEGA", "SNARL_FAST", "FOUL_PLAY"),
            # ("HYDREIGON", "BITE_FAST", "BRUTAL_SWING"),
            # ("GUZZLORD", "SNARL_FAST", "BRUTAL_SWING"),
            # ("TYRANITAR", "BITE_FAST", "CRUNCH"),
            # ("TYRANITAR_SHADOW_FORM", "BITE_FAST", "CRUNCH"),
            # ("TYRANITAR_MEGA", "BITE_FAST", "CRUNCH"),
            # ("WEAVILE", "SNARL_FAST", "FOUL_PLAY"),
            # ("WEAVILE_SHADOW_FORM", "SNARL_FAST", "FOUL_PLAY"),
            # ("ABSOL", "SNARL_FAST", "DARK_PULSE"),
            # ("ABSOL_SHADOW_FORM", "SNARL_FAST", "DARK_PULSE"),
            # ("ABSOL_MEGA", "SNARL_FAST", "DARK_PULSE"),
            # ("DARKRAI", "SNARL_FAST", "DARK_PULSE"),
            # ("ZOROARK", "SNARL_FAST", "FOUL_PLAY"),
            # ("YVELTAL", "SNARL_FAST", "DARK_PULSE"),
            # ("HONCHKROW", "SNARL_FAST", "DARK_PULSE"),
            # ("HONCHKROW_SHADOW_FORM", "SNARL_FAST", "DARK_PULSE"),

            # ("GARDEVOIR", "CHARM_FAST", "DAZZLING_GLEAM"),
            # ("GARDEVOIR_SHADOW_FORM", "CHARM_FAST", "DAZZLING_GLEAM"),
            # ("GARDEVOIR_MEGA", "CHARM_FAST", "DAZZLING_GLEAM"),
            # ("RAPIDASH_GALARIAN_FORM", "FAIRY_WIND_FAST", "PLAY_ROUGH"),
            # ("SYLVEON", "CHARM_FAST", "DAZZLING_GLEAM"),
            # ("GRANBULL", "CHARM_FAST", "PLAY_ROUGH"),
            # ("GRANBULL_SHADOW_FORM", "CHARM_FAST", "PLAY_ROUGH"),
            # ("CLEFABLE", "CHARM_FAST", "DAZZLING_GLEAM"),
            # ("SLURPUFF", "CHARM_FAST", "PLAY_ROUGH"),
            # ("SLURPUFF", "FAIRY_WIND_FAST", "PLAY_ROUGH"),
        ],
    },

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

    # [For all counters]
    # {
    #     "Min level": 30,
    #     "Max level": 50,
    #     "Level step size": 5, #5,  # Can be as low as 0.5, but recommend 5 for efficiency
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
    #     "Pokemon pool": ["TAPU_BULU"],
    #     "Raid tier": "Tier 5",  # Here, "Tier 5" has only current bosses
    #     "Weight of each Pokemon": 1,
    #     "Weight of whole group": 1,
    #     "Forms weight strategy": "combine",  # "combine" or "separate"
    # },
    # {
    #     "Pokemon pool": ["TAPU_BULU"],
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
        "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier"],  # Here, "Tier 5" has all past/present/future bosses
        #"Raid category": "Ultra Beast Tier",  # Here, "Tier 5" has only current bosses
        "Filters": {  # Only those without # at the start are applied
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            get_ensemble_weak_key(): get_move_types(),
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
        "Raid tiers": ["Tier 5", "Ultra Beast Tier", "Elite Tier"],
        "Filters": {
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            get_ensemble_weak_key(): get_move_types(),
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 0,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Attack strategy": "Dodge Specials PRO",
        },
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
    #         "Weather": "Cloudy",
    #     },
    # },

    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
        "Filters": {
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            get_ensemble_weak_key(): get_move_types(),
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 35,  #25,
        "Forms weight strategy": "combine",
    },
    {
        "Pokemon pool": "By raid tier",
        "Raid tiers": ["Mega Tier", "Mega Legendary Tier"],
        "Filters": {
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            get_ensemble_weak_key(): get_move_types(),
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 0,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Attack strategy": "Dodge Specials PRO",
        },
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
    #         "Weather": "Cloudy",
    #     },
    # },

    {
        "Pokemon pool": "By raid tier",
        "Raid tier": "Tier 3",
        "Filters": {
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            get_ensemble_weak_key(): get_move_types(),
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 15,  #25,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Friendship": "Not",
        },
        "Baseline battle settings": {
            "Friendship": "Not",
        }
    },
    {
        "Pokemon pool": "By raid tier",
        "Raid tier": "Tier 3",
        "Filters": {
            #"Weak to contender types": SINGLE_TYPE_ATTACKER,
            #"Weak to contender types simultaneously": MULTI_TYPE_ATTACKERS_COMPARE,
            get_ensemble_weak_key(): get_move_types(),
        },
        "Weight of each Pokemon": 1,
        "Weight of whole group": 0,
        "Forms weight strategy": "combine",
        "Battle settings": {
            "Friendship": "Not",
            "Attack strategy": "Dodge Specials PRO",
        },
        "Baseline battle settings": {
            "Friendship": "Not",
        }
    },
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
    #         "Weather": "Cloudy",
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

    "Enabled": True,  # Default: True
    "Baseline chosen before filter": False,  # Default: False
    "Baseline boss moveset": "random",  # "random", "easiest", "hardest"
    "Baseline attacker level": 40,  # Specific level, "min", "max", "average", "by level"/-1/None
    "Baseline battle settings": {
        "Weather": "Extreme",
        "Friendship": "Best",
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
    "Include unscaled estimators": False,  # Default: False
    "Combine attacker movesets": True,  # Combine attacker moves (e.g. FS/BB and Counter/BB Blaziken), Default: True
    "Include random boss movesets": True,  # Default: True
    "Include specific boss movesets": False,  # Default: False
    "Assign weights to specific boss movesets": False,  # Default: False
    "Include attacker IVs": False,  # Default: False
    "Fill blanks": True,  # Default: True

    "Attackers that should not be combined": [  # Will not combine these attackers' different movesets,
        # "ROSERADE", "VENUSAUR", "ROSERADE_SHADOW_FORM", "VENUSAUR_SHADOW_FORM", "VENUSAUR_MEGA", "VICTREEBEL_SHADOW_FORM",
        # "SHIFTRY_SHADOW_FORM", "ZARUDE", "TANGROWTH", "SCEPTILE", "TANGROWTH_SHADOW_FORM", "SCEPTILE_SHADOW_FORM",
        # "TANGELA_SHADOW_FORM", "MEGANIUM_SHADOW_FORM", "LEAFEON", "TORTERRA_SHADOW_FORM", "TORTERRA",
        # "EXEGGUTOR_SHADOW_FORM", "EXEGGUTOR", "CELEBI", "CHESNAUGHT", "BRELOOM",

        # "CHARIZARD", "CHARIZARD_SHADOW_FORM", "CHARIZARD_MEGA_Y", "BLAZIKEN", "EMBOAR", "INFERNAPE", "BLAZIKEN_SHADOW_FORM",
        # "EMBOAR_SHADOW_FORM", "INFERNAPE_SHADOW_FORM", "BLAZIKEN_MEGA", "DARMANITAN_STANDARD_FORM", "ENTEI",
        # "ENTEI_SHADOW_FORM", "FLAREON", "MOLTRES", "HO_OH", "MOLTRES_SHADOW_FORM", "HO_OH_SHADOW_FORM",
        # "HOUNDOOM_SHADOW_FORM", "HOUNDOOM_MEGA", "TYPHLOSION", "MAGMORTAR", "ARCANINE", "TYPHLOSION_SHADOW_FORM",
        # "MAGMORTAR_SHADOW_FORM", "ARCANINE_SHADOW_FORM",

        # "SWAMPERT", "SWAMPERT_SHADOW_FORM", "SWAMPERT_MEGA", "BLASTOISE_MEGA", "FERALIGATR_SHADOW_FORM", "KYOGRE",
        # "KINGLER", "SAMUROTT", "FERALIGATR", "CLAWITZER","BLASTOISE_SHADOW_FORM", "GYARADOS_MEGA", "CRAWDAUNT",
        # "GYARADOS", "GYARADOS_SHADOW_FORM",

        # "XURKITREE", "RAIKOU", "ELECTIVIRE", "LUXRAY", "RAIKOU_SHADOW_FORM", "ELECTIVIRE_SHADOW_FORM",
        # "LUXRAY_SHADOW_FORM", "MANECTRIC_MEGA", "MANECTRIC_SHADOW_FORM", "ZEKROM", "AMPHAROS_MEGA",
        # "THUNDURUS_THERIAN_FORM", "ZAPDOS", "ZAPDOS_SHADOW_FORM", "MAGNEZONE_SHADOW_FORM", "MAGNEZONE", "MAGNETON_SHADOW_FORM",

        # "MAMOSWINE_SHADOW_FORM", "MAMOSWINE", "PILOSWINE_SHADOW_FORM", "WEAVILE_SHADOW_FORM", "WEAVILE",
        # "DARMANITAN_GALARIAN_STANDARD_FORM", "GLALIE_MEGA", "GLACEON", "AVALUGG", "BEARTIC","ABOMASNOW_MEGA",
        # "ABOMASNOW_SHADOW_FORM", "ARTICUNO_SHADOW_FORM", "ARTICUNO",

        # "AERODACTYL", "AERODACTYL_SHADOW_FORM", "AERODACTYL_MEGA", "TYRANITAR_SHADOW_FORM", "TYRANITAR",
        # "RAMPARDOS", "GIGALITH", "RAMPARDOS_SHADOW_FORM", "GIGALITH_SHADOW_FORM", "AGGRON_SHADOW_FORM", "AGGRON",
        # "GOLEM_SHADOW_FORM", "RHYPERIOR", "GOLEM",

        # "MAMOSWINE_SHADOW_FORM", "MAMOSWINE", "GROUDON", "GROUDON_SHADOW_FORM", "DONPHAN", "DONPHAN_SHADOW_FORM",
        # "SWAMPERT_MEGA", "SWAMPERT_SHADOW_FORM", "SWAMPERT", "GARCHOMP", "GARCHOMP_SHADOW_FORM", "FLYGON",
        # "FLYGON_SHADOW_FORM", "GOLURK_SHADOW_FORM", "GOLURK", "RHYPERIOR", "RHYDON", "RHYPERIOR_SHADOW_FORM",
        # "RHYDON_SHADOW_FORM", "GOLEM_SHADOW_FORM", "GOLEM",

        # "METAGROSS_SHADOW_FORM", "METAGROSS", "GENESECT", "SCIZOR", "SCIZOR_SHADOW_FORM", "SCIZOR_MEGA", "DURANT",
        # "EXCADRILL", "STEELIX_MEGA", "AGGRON_SHADOW_FORM", "AGGRON",

        # "GENESECT", "SCIZOR", "SCIZOR_SHADOW_FORM", "SCIZOR_MEGA", "DURANT", "BEEDRILL_MEGA", "VENOMOTH_SHADOW_FORM",
        # "PINSIR", "ACCELGOR", "PINSIR_SHADOW_FORM", "ACCELGOR_SHADOW_FORM", "YANMEGA", "SCYTHER",
        # "YANMEGA_SHADOW_FORM", "SCYTHER_SHADOW_FORM",

        # "BEEDRILL_MEGA", "SCOLIPEDE", "ROSERADE", "VICTREEBEL", "VILEPLUME", "ROSERADE_SHADOW_FORM", "VICTREEBEL_SHADOW_FORM",
        # "VILEPLUME_SHADOW_FORM", "OVERQWIL", "SKUNTANK", "SKUNTANK_SHADOW_FORM", "DRAPION_SHADOW_FORM",

        "MOLTRES_SHADOW_FORM", "MOLTRES", "STARAPTOR", "BRAVIARY", "STARAPTOR_SHADOW_FORM", "BRAVIARY_SHADOW_FORM",
        "PIDGEOT_MEGA", "HONCHKROW_SHADOW_FORM", "HONCHKROW", "UNFEZANT", "UNFEZANT_SHADOW_FORM", "TOUCANNON",
        "RAYQUAZA", "NOIVERN", "YVELTAL", "MOLTRES_GALARIAN_FORM", "TORNADUS_INCARNATE_FORM", "TORNADUS_THERIAN_FORM",
        # Speculative
        "CHARIZARD", "CHARIZARD_SHADOW_FORM", "CHARIZARD_MEGA_Y", "AERODACTYL", "AERODACTYL_SHADOW_FORM",
        "AERODACTYL_MEGA", "DRAGONITE", "DRAGONITE_SHADOW_FORM", "ZAPDOS", "ZAPDOS_SHADOW_FORM", "LUGIA",
        "LUGIA_SHADOW_FORM", "HO_OH", "HO_OH_SHADOW_FORM", "SALAMENCE", "SALAMENCE_SHADOW_FORM", "SALAMENCE_MEGA",
        "RAYQUAZA", "RAYQUAZA_SHADOW_FORM", "RAYQUAZA_MEGA", "ARCHEOPS", "ARCHEOPS_SHADOW_FORM",

        # "RAYQUAZA", "SALAMENCE", "DRAGONITE", "RAYQUAZA_SHADOW_FORM", "SALAMENCE_SHADOW_FORM", "DRAGONITE_SHADOW_FORM",
        # "SALAMENCE_MEGA", "LATIOS", "LATIAS", "LATIOS_SHADOW_FORM", "LATIAS_SHADOW_FORM", "LATIOS_MEGA", "LATIAS_MEGA",
        # "GARCHOMP", "FLYGON_SHADOW_FORM",

        # "BLAZIKEN_MEGA", "BLAZIKEN_SHADOW_FORM", "BLAZIKEN", "EMBOAR", "KELDEO", "POLIWRATH_SHADOW_FORM",
        # "CONKELDURR", "MACHAMP", "HARIYAMA", "CONKELDURR_SHADOW_FORM", "MACHAMP_SHADOW_FORM", "HARIYAMA_SHADOW_FORM",
        # "LUCARIO", "COBALION", "LUCARIO_SHADOW_FORM", "COBALION_SHADOW_FORM", "BRELOOM", "VIRIZION",
        # "BRELOOM_SHADOW_FORM", "VIRIZION_SHADOW_FORM",

        # "MEWTWO", "ESPEON", "ALAKAZAM", "MEWTWO_SHADOW_FORM", "ESPEON_SHADOW_FORM", "ALAKAZAM_SHADOW_FORM",
        # "ALAKAZAM_MEGA", "LATIOS", "LATIAS", "LATIOS_SHADOW_FORM", "LATIAS_SHADOW_FORM", "LATIOS_MEGA", "LATIAS_MEGA",
        # "GALLADE", "GALLADE_SHADOW_FORM", "GALLADE_MEGA", "GARDEVOIR", "GARDEVOIR_SHADOW_FORM", "GARDEVOIR_MEGA",
        # "METAGROSS", "METAGROSS_SHADOW_FORM", "METAGROSS_MEGA", "LUNALA", "HOOPA_CONFINED_FORM",

        # "GENGAR_MEGA", "GENGAR_SHADOW_FORM", "GENGAR", "BANETTE", "MISMAGIUS", "BANETTE_SHADOW_FORM", "BANETTE_MEGA",
        # "MISMAGIUS_SHADOW_FORM", "GIRATINA_ORIGIN_FORM", "GIRATINA_ALTERED_FORM", "TREVENANT", "GOURGEIST_SMALL_FORM",
        # "GOURGEIST_AVERAGE_FORM", "GOURGEIST_LARGE_FORM", "GOURGEIST_SUPER_FORM",

        # "HOUNDOOM", "HOUNDOOM_SHADOW_FORM", "HOUNDOOM_MEGA", "HYDREIGON", "GUZZLORD", "TYRANITAR",
        # "TYRANITAR_SHADOW_FORM", "TYRANITAR_MEGA", "WEAVILE", "WEAVILE_SHADOW_FORM", "ABSOL", "ABSOL_SHADOW_FORM",
        # "ABSOL_MEGA", "DARKRAI", "ZOROARK", "YVELTAL", "HONCHKROW", "HONCHKROW_SHADOW_FORM",

        # "GARDEVOIR", "GARDEVOIR_SHADOW_FORM", "GARDEVOIR_MEGA", "RAPIDASH_GALARIAN_FORM", "SYLVEON", "GRANBULL",
        # "GRANBULL_SHADOW_FORM", "CLEFABLE", "SLURPUFF",
    ],
}
