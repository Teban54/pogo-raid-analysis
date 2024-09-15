"""
Parameters.
"""


# ----------------- Input/Output -----------------


POKEBATTLER_SERVER = "https://fight.pokebattler.com/"  # End with /
JSON_DATA_PATH = "data/json/"
COUNTERS_DATA_PATH = "data/counters/"
OUTPUTS_DATA_PATH = "data/outputs/"

CONNECTION_RETRIES = 40 #20000  # In case aiohttp.get() fails
CONNECTION_WAIT_SEC = 20 #20000  # In case aiohttp.get() fails
CONCURRENCY = 20 #1000  # Now only for filling blanks


# ----------------- Ensembles -----------------


# The following forms are considered as a standalone Pokemon, not as a form of their base Pokemon.
# Therefore, they will receive a weight of 1 on their own,
# instead of all forms of the base Pokemon sharing a weight of 1 (e.g. Arceus).
# The only place where this is utilized is when assigning weights.
# Note: Shadows have not been considered in this, as shadows are not raid bosses yet.
FORMS_AS_SEPARATE_POKEMON_UNIVERSAL = [
    'ALOLA', 'GALARIAN', 'HISUIAN', 'PALDEAN',
]
FORMS_AS_SEPARATE_POKEMON_PER_POKEMON = {
    # <base codename>: [<form to be considered as separate>, (<two forms to be>, <combined as single pokemon>)]
    # All dict values here must be lists
    # For each element, if it's a single string, this form will become a standalone Pokemon with no forms
    # If it's a tuple or list, those forms will become (multiple) forms of a standalone Pokemon
    # All forms not mentioned here are treated as their own standalone Pokemon

    # For example:
    'DARMANITAN': [('GALARIAN_STANDARD', 'GALARIAN_ZEN')],
    # This makes G-Darmanitan Standard and G-Darmanitan Zen two forms of a Pokemon (G-Darmanitan)
    # The two forms not mentioned, Darmanitan Standard and Darmanitan Zen, are two forms of a Pokemon (U-Darmanitan)

    # Example of a single separate form (hypothetical):
    # 'NECROZMA': ['ULTRA', ('DUSK_MANE', 'DAWN_WINGS')]
    # This makes 3 standalone Pokemon: Regular form, Dusk Mane AND Dawn Wings forms, Ultra form
}


# If the raid boss is shadow, change the raid tier to the corresponding shadow raid tier
# (e.g. Tier 5 -> Shadow Tier 5)
CONVERT_SHADOW_RAID_TIERS = True


# ----------------- Ignored Pokemon and Raids -----------------


IGNORED_RAID_BOSSES = {  # Keys are raid tiers, no "legacy"
    "RAID_LEVEL_5": [#'MELOETTA_ARIA_FORM', 'MELOETTA_PIROUETTE_FORM',  # Already got from special research
                     'BIDOOF', 'KYOGRE_PRIMAL', 'GROUDON_PRIMAL', 'MEW_SHADOW_FORM'],
    'RAID_LEVEL_5_SHADOW': ['MEW_SHADOW_FORM'],
}

IGNORED_FORMS = {  # Forms and Pokemon that should not exist
    'URSHIFU': [''],  # Current GM has Urshifu "regular" form as mono Fighting
    'HONEDGE': [''],  # The Honedge line has no stats yet in either GM or Pokebattler
    'DOUBLADE': [''],
    'AEGISLASH': [''],  # No stats yet in either GM or Pokebattler
    'RAIKOU': ['S'],
    'ENTEI': ['S'],
    'SUICUNE': ['S'],
    'LUGIA': ['S'],
    'HO_OH': ['S'],
    'LATIAS': ['S'],
    'LATIOS': ['S'],
}
# [Reminder] When using any Pokemon above, make sure these forms are ignored

COSMETIC_FORMS_UNIVERSAL = [  # Any Pokemon with these forms only have cosmetic changes
                              # (e.g. should not be considered a different raid boss)
    'FALL_2019', 'COPY_2019', 'COSTUME_2020', 'ADVENTURE_HAT_2020', 'WINTER_2020', 'GOFEST_2022', 'WCS_2022',
    # Note Pikachu Costume 2020 is Flying Pikachu with the move Fly, but it's the same as FLYING_5TH_ANNIV
    # VS_2019 is Pikachu Libre
    '2020', '2021', '2022', 'FLYING_OKINAWA', 'FLYING_01', 'FLYING_02', 'FLYING_03', 'TSHIRT_01', 'TSHIRT_02',
    'SUMMER_2023', 'SUMMER_2023_A', 'SUMMER_2023_B', 'SUMMER_2023_C', 'SUMMER_2023_D', 'SUMMER_2023_E', 'JEJU',

]
COSMETIC_FORMS_PER_POKEMON = {  # These specific Pokemon have these cosmetic forms (i.e. same as their normal form)
    'PIKACHU': ['KARIYUSHI'],
    'SHELLOS': ['WEST_SEA', 'EAST_SEA'],
    'GASTRODON': ['WEST_SEA', 'EAST_SEA'],
    'BASCULIN': ['RED_STRIPED', 'BLUE_STRIPED'],
    'KELDEO': ['ORDINARY', 'RESOLUTE'],
    'DEERLING': ['SPRING', 'SUMMER', 'AUTUMN', 'WINTER'],
    'SAWSBUCK': ['SPRING', 'SUMMER', 'AUTUMN', 'WINTER'],
    'FRILLISH': ['FEMALE'],
    'JELLICENT': ['FEMALE'],
    'PYROAR': ['FEMALE'],
    'FURFROU': ['NATURAL', 'HEART', 'STAR', 'DIAMOND', 'DEBUTANTE', 'MATRON', 'DANDY', 'LA_REINE', 'KABUKI', 'PHARAOH'],
    'MAGEARNA': ['ORIGINAL_COLOR'],
    'SINISTEA': ['PHONY', 'ANTIQUE'],
    'POLTEAGEIST': ['PHONY', 'ANTIQUE'],
    'SCATTERBUG': ['ARCHIPELAGO', 'CONTINENTAL', 'ELEGANT', 'FANCY', 'GARDEN', 'HIGH_PLAINS', 'ICY_SNOW', 'JUNGLE',
                 'MARINE', 'MEADOW', 'MODERN', 'MONSOON', 'OCEAN', 'POKEBALL', 'POLAR', 'RIVER', 'SANDSTORM', 'SAVANNA',
                 'SUN', 'TUNDRA'],
    'SPEWPA': ['ARCHIPELAGO', 'CONTINENTAL', 'ELEGANT', 'FANCY', 'GARDEN', 'HIGH_PLAINS', 'ICY_SNOW', 'JUNGLE',
                 'MARINE', 'MEADOW', 'MODERN', 'MONSOON', 'OCEAN', 'POKEBALL', 'POLAR', 'RIVER', 'SANDSTORM', 'SAVANNA',
                 'SUN', 'TUNDRA'],
    'VIVILLON': ['ARCHIPELAGO', 'CONTINENTAL', 'ELEGANT', 'FANCY', 'GARDEN', 'HIGH_PLAINS', 'ICY_SNOW', 'JUNGLE',
                 'MARINE', 'MEADOW', 'MODERN', 'MONSOON', 'OCEAN', 'POKEBALL', 'POLAR', 'RIVER', 'SANDSTORM', 'SAVANNA',
                 'SUN', 'TUNDRA'],
    'FLABEBE': ['RED', 'YELLOW', 'ORANGE', 'BLUE', 'WHITE'],
    'FLOETTE': ['RED', 'YELLOW', 'ORANGE', 'BLUE', 'WHITE'],
    'FLORGES': ['RED', 'YELLOW', 'ORANGE', 'BLUE', 'WHITE'],
    'MINIOR': ['BLUE', 'GREEN', 'INDIGO', 'ORANGE', 'RED', 'VIOLET', 'YELLOW'],  # CORE has different stats but not in GM
    'MIMIKYU': ['BUSTED', 'DISGUISED'],
    'MAUSHOLD': ['FAMILY_OF_THREE', 'FAMILY_OF_FOUR'],
    'SQUAWKABILLY': ['GREEN', 'BLUE', 'YELLOW', 'WHITE'],
    'TATSUGIRI': ['CURLY', 'DROOPY', 'SCRETCHY'],
    'DUDUNSPARCE': ['TWO', 'THREE'],
    'KORAIDON': ['APEX'],
    'MIRAIDON': ['ULTIMATE'],
    'ZYGARDE': ['COMPLETE_TEN_PERCENT', 'COMPLETE_FIFTY_PERCENT'],  # TODO: Remove cosmetic forms from attacker lists if their non-cosmetic forms are also listed
    # Toxtricity is not listed here in case abilities matter in the future

    # The following Pokemon have non-cosmetic forms, but one of them is identical to the "regular" form
    # (the one with no forms listed, which also appears in both Pokebattler and GM data),
    # hence this form is also considered cosmetic
    # [CAREFUL!!] Make sure the forms that Pokebattler uses on their Legacy T5 lists do NOT appear here!!!
    'BURMY': [''],
    'WORMADAM': [''],
    'SHAYMIN': [''],  # Raid boss list has both '' and Land, attacker list only has Land
    'CHERRIM': [''],
    'GIRATINA': [''],  # ['ALTERED'],
    'DARMANITAN': ['STANDARD'],  # Attacker list has ''; Galarian has no "regular" form, only Standard and Zen
    'TORNADUS': ['INCARNATE'],  # Raid boss list and attacker list both have ''
    'THUNDURUS': ['INCARNATE'],
    'LANDORUS': ['INCARNATE'],
    'ENAMORUS': ['INCARNATE'],
    'MELOETTA': [''],  # Pokebattler lists Aria Meloetta on their list
    'EISCUE': [''],
    'INDEEDEE': [''],
    'MORPEKO': [''],  # Considering Hangry as non-cosmetic since Aura Wheel could be added one day
    'ZACIAN': [''],  # ['HERO'],
    'ZAMAZENTA': [''],  # ['HERO'],
    'PUMPKABOO': ['SMALL'],
    'GOURGEIST': ['SMALL'],
    'HOOPA': [''],  # Future Elite Tier has Hoopa Confined
    'ORICORIO': [''],
    'CASTFORM': ['NORMAL'],
    'DEOXYS': ['NORMAL'],  # Pokebattler lists DEOXYS without forms
    'TOXTRICITY': [''],  # In case abilities matter in the future
    'LYCANROC': [''],
    'PALAFIN': [''],
}
# [Reminder] When using any Pokemon above, make sure only their regular forms are considered
#  (and not considered again if one of the cosmetic forms already is)

IGNORE_INVALID_RAID_BOSSES = True  # Remove a raid boss listed on Pokebattler automatically when
                                   # the corresponding Pokemon object does not exist (e.g. Giratina-Altered)


# ----------------- Types -----------------


POKEMON_TYPES = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying",
                 "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]  # Natural language
TYPE_EFFECTIVENESS = [  # Axis 0 is attacker, Axis 1 is defender
    # Values are exponents to be applied to SE multiplier (-2,-1,0,1,2)
    # +---> This axis is defender
    # |
    # V   This axis is attacker
    #N Fr Wt Ec Gs Ic Ft Pi Gd Fy Pc Bg Rk Gh Dr Dk St Fa
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1,-2, 0, 0,-1, 0],  # Normal attack
    [0,-1,-1, 0, 1, 1, 0, 0, 0, 0, 0, 1,-1, 0,-1, 0, 1, 0],  # Fire attack
    [0, 1,-1, 0,-1, 0, 0, 0, 1, 0, 0, 0, 1, 0,-1, 0, 0, 0],  # Water attack
    [0, 0, 1,-1,-1, 0, 0, 0,-2, 1, 0, 0, 0, 0,-1, 0, 0, 0],  # Electric attack
    [0,-1, 1, 0,-1, 0, 0,-1, 1,-1, 0,-1, 1, 0,-1, 0,-1, 0],  # Grass attack
    [0,-1,-1, 0, 1,-1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0,-1, 0],  # Ice attack
    [1, 0, 0, 0, 0, 1, 0,-1, 0,-1,-1,-1, 1,-2, 0, 1, 1,-1],  # Fighting attack
    [0, 0, 0, 0, 1, 0, 0,-1,-1, 0, 0, 0,-1,-1, 0, 0,-2, 1],  # Poison attack
    [0, 1, 0, 1,-1, 0, 0, 1, 0,-2, 0,-1, 1, 0, 0, 0, 1, 0],  # Ground attack
    [0, 0, 0,-1, 1, 0, 1, 0, 0, 0, 0, 1,-1, 0, 0, 0,-1, 0],  # Flying attack
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0,-1, 0, 0, 0, 0,-2,-1, 0],  # Psychic attack
    [0,-1, 0, 0, 1, 0,-1,-1, 0,-1, 1, 0, 0,-1, 0, 1,-1,-1],  # Bug attack
    [0, 1, 0, 0, 0, 1,-1, 0,-1, 1, 0, 1, 0, 0, 0, 0,-1, 0],  # Rock attack
    [-2,0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,-1, 0, 0],  # Ghost attack
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,-1,-2],  # Dragon attack
    [0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 1, 0, 0, 1, 0,-1, 0,-1],  # Dark attack
    [0,-1,-1,-1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,-1, 1],  # Steel attack
    [0,-1, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 1, 1,-1, 0],  # Fairy attack
]
TYPE_EFFECTIVENESS_TRANSPOSE = [  # Axis 0 is defender, Axis 1 is attacker
    [TYPE_EFFECTIVENESS[i][j] for i in range(len(TYPE_EFFECTIVENESS))]
    for j in range(len(TYPE_EFFECTIVENESS[0]))
]
SE_MULTIPLIER = 1.6  # Don't think will be needed for my project, but...?


# ----------------- Pokemon -----------------


SPECIAL_BASE_DISPLAY_NAMES = {  # Default: Replace _ with space (Tapu Koko)
    'NIDORAN_FEMALE': 'Nidoran♀',
    'NIDORAN_MALE': 'Nidoran♂',
    'MR_MIME': 'Mr. Mime',
    'MIME_JR': 'Mime Jr.',
    'MR_RIME': 'Mr. Rime',
    'HO_OH': 'Ho-Oh',
    'PORYGON_Z': 'Porygon-Z',
    'FARFETCHD': 'Farfetch\'d',
    'SIRFETCHD': 'Sirfetch\'d',
    'FLABEBE': 'Flabébé',
    'JANGMO_O': 'Jangmo-o',
    'HAKAMO_O': 'Hakamo-o',
    'KOMMO_O': 'Kommo-o',
    'GREATTUSK': 'Great Tusk',
    'SCREAMTAIL': 'Scream Tail',
    'BRUTEBONNET': 'Brute Bonnet',
    'FLUTTERMANE': 'Flutter Mane',
    'SLITHERWING': 'Slither Wing',
    'SANDYSHOCKS': 'Sandy Shocks',
    'IRONTREADS': 'Iron Treads',
    'IRONBUNDLE': 'Iron Bundle',
    'IRONHANDS': 'Iron Hands',
    'IRONJUGULIS': 'Iron Jugulis',
    'IRONMOTH': 'Iron Moth',
    'IRONTHORNS': 'Iron Thorns',
    'WOCHIEN': 'Wo-Chien',
    'CHIENPAO': 'Chien-Pao',
    'TINGLU': 'Ting-Lu',
    'CHIYU': 'Chi-Yu',
    'ROARINGMOON': 'Roaring Moon',
    'IRONVALIANT': 'Iron Valiant',
}
SPECIAL_FORM_DISPLAY_NAMES = {
    'A': 'Armored',
    'VS_2019': 'Libre',
    'S': 'Apex',  # Not accurate for legendary beasts, but whatever
    'POMPOM': 'Pom-Pom',
    'PAU': 'Pa\'u',
}


# ----------------- Raid Bosses -----------------


RAID_TIERS_CODE2STR = {
    "RAID_LEVEL_1": "Tier 1",
    "RAID_LEVEL_2": "Tier 2",
    "RAID_LEVEL_3": "Tier 3",
    "RAID_LEVEL_4": "Tier 4",
    "RAID_LEVEL_4_5": "Tier 4.5",
    "RAID_LEVEL_5": "Tier 5",
    "RAID_LEVEL_6": "Tier 6",
    "RAID_LEVEL_MEGA": "Mega Tier",
    "RAID_LEVEL_MEGA_5": "Mega Legendary Tier",
    "RAID_LEVEL_ULTRA_BEAST": "Ultra Beast Tier",
    "RAID_LEVEL_ELITE": "Elite Tier",
    "RAID_LEVEL_1_SHADOW": "Shadow Tier 1",
    "RAID_LEVEL_3_SHADOW": "Shadow Tier 3",
    "RAID_LEVEL_5_SHADOW": "Shadow Tier 5",
}
RAID_CATEGORIES_CODE2STR = {  # Shouldn't be needed for this project, but just in case
    "RAID_LEVEL_1": "Tier 1",
    "RAID_LEVEL_1_LEGACY": "Legacy Tier 1",
    "RAID_LEVEL_1_FUTURE": "Future Tier 1",  # In case
    "RAID_LEVEL_2": "Tier 2",
    "RAID_LEVEL_2_LEGACY": "Legacy Tier 2",
    "RAID_LEVEL_2_FUTURE": "Future Tier 2",  # In case
    "RAID_LEVEL_3": "Tier 3",
    "RAID_LEVEL_3_LEGACY": "Legacy Tier 3",
    "RAID_LEVEL_3_FUTURE": "Future Tier 3",  # In case
    "RAID_LEVEL_4": "Tier 4",
    "RAID_LEVEL_4_LEGACY": "Legacy Tier 4",
    "RAID_LEVEL_4_FUTURE": "Future Tier 4",  # In case
    "RAID_LEVEL_4_5": "Tier 4.5",
    "RAID_LEVEL_4_5_LEGACY": "Legacy Tier 4.5",
    "RAID_LEVEL_4_5_FUTURE": "Future Tier 4.5",  # In case
    "RAID_LEVEL_5": "Tier 5",
    "RAID_LEVEL_5_LEGACY": "Legacy Tier 5",
    "RAID_LEVEL_5_FUTURE": "Future Tier 5",
    "RAID_LEVEL_6": "Tier 6",
    "RAID_LEVEL_6_LEGACY": "Legacy Tier 6",
    "RAID_LEVEL_6_FUTURE": "Future Tier 6",  # In case
    "RAID_LEVEL_MEGA": "Mega Tier",
    "RAID_LEVEL_MEGA_LEGACY": "Legacy Mega Tier",
    "RAID_LEVEL_MEGA_FUTURE": "Future Mega Tier",
    "RAID_LEVEL_MEGA_5": "Mega Legendary Tier",
    "RAID_LEVEL_MEGA_5_LEGACY": "Legacy Mega Legendary Tier",
    "RAID_LEVEL_MEGA_5_FUTURE": "Future Mega Legendary Tier",
    "RAID_LEVEL_ULTRA_BEAST": "Ultra Beast Tier",
    "RAID_LEVEL_ULTRA_BEAST_LEGACY": "Legacy Ultra Beast Tier",
    "RAID_LEVEL_ULTRA_BEAST_FUTURE": "Future Ultra Beast Tier",
    "RAID_LEVEL_ELITE": "Elite Tier",
    "RAID_LEVEL_ELITE_LEGACY": "Legacy Elite Tier",  # In case
    "RAID_LEVEL_ELITE_FUTURE": "Future Elite Tier",  # In case
    "RAID_LEVEL_1_SHADOW": "Shadow Tier 1",
    "RAID_LEVEL_1_SHADOW_LEGACY": "Legacy Shadow Tier 1",
    "RAID_LEVEL_1_SHADOW_FUTURE": "Future Shadow Tier 1",  # In case
    "RAID_LEVEL_3_SHADOW": "Shadow Tier 3",
    "RAID_LEVEL_3_SHADOW_LEGACY": "Legacy Shadow Tier 3",
    "RAID_LEVEL_3_SHADOW_FUTURE": "Future Shadow Tier 3",  # In case
    "RAID_LEVEL_5_SHADOW": "Shadow Tier 5",
    "RAID_LEVEL_5_SHADOW_LEGACY": "Legacy Shadow Tier 5",
    "RAID_LEVEL_5_SHADOW_FUTURE": "Future Shadow Tier 5",  # In case
    "RAID_LEVEL_UNSET": "Tier ?",  # Should be ignored when reading JSON
}
# Reminder - If encountered a tier not listed above, do not report an error, only a warning!!
# This is to easily adapt in future if Niantic adds a new tier or Pokebattler adds a new category


# ----------------- Moves -----------------


IGNORED_MOVES = {
    "DODGE",
    "MOVE_NONE",
    "RANDOM",
}

SPECIAL_MOVE_DISPLAY_NAMES = {
    'VICE_GRIP': 'Vise Grip',
    'X_SCISSOR': 'X-Scissor',
    #'SCALD_BLASTOISE': 'Scald',
    #'HYDRO_PUMP_BLASTOISE': 'Hydro Pump',
    #'WRAP_GREEN': 'Wrap',
    #'WRAP_PINK': 'Wrap',
    'WATER_GUN_FAST_BLASTOISE': 'Water Gun Blastoise',
    'MUD_SLAP_FAST': 'Mud-Slap',
    'SUPER_POWER': 'Superpower',
    'POWER_UP_PUNCH': 'Power-Up Punch',
    'LOCK_ON_FAST': 'Lock-On',
    'V_CREATE': 'V-Create',
    #'TRI_ATTACK': 'Tri-Attack',
    'FUTURESIGHT': 'Future Sight',
    'AEROBLAST_PLUS': 'Aeroblast+',
    'AEROBLAST_PLUS_PLUS': 'Aeroblast++',
    'SACRED_FIRE_PLUS': 'Sacred Fire+',
    'SACRED_FIRE_PLUS_PLUS': 'Sacred Fire++',
    'NATURES_MADNESS': "Nature's Madness",
}


# ----------------- Default Settings -----------------


MIN_LEVEL_DEFAULT = 30
MAX_LEVEL_DEFAULT = 50
LEVEL_STEP_DEFAULT = 5
