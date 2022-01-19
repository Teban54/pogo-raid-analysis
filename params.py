"""
Parameters.
"""


# ----------------- Input/Output -----------------


JSON_DATA_PATH = "data/json/"
COUNTERS_DATA_PATH = "data/counters/"
OUTPUTS_DATA_PATH = "data/outputs/"


# ----------------- Ensembles -----------------


# The following forms are considered as a standalone Pokemon, not as a form of their base Pokemon.
# Therefore, they will receive a weight of 1 on their own,
# instead of all forms of the base Pokemon sharing a weight of 1 (e.g. Arceus).
# The only place where this is utilized is when assigning weights.
FORMS_AS_SEPARATE_POKEMON_UNIVERSAL = [
    'ALOLA', 'GALARIAN'
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


# ----------------- Ignored Pokemon and Raids -----------------


IGNORED_RAID_BOSSES = {  # Keys are raid tiers, no "legacy"
    "RAID_LEVEL_5": ['ZACIAN_HERO_FORM', 'ZAMAZENTA_HERO_FORM',  # Zacian and Zamazenta with no forms are already under future T5s
                    'MELOETTA_ARIA_FORM', 'MELOETTA_PIROUETTE_FORM']  # Already got from special research
}

IGNORED_FORMS = {  # Forms and Pokemon that should not exist
    'URSHIFU': [''],  # Current GM has Urshifu "regular" form as mono Fighting
    'HONEDGE': [''],  # The Honedge line has no stats yet in either GM or Pokebattler
    'DOUBLADE': [''],
    'AEGISLASH': [''],
    'ZYGARDE': [''],  # Zygarde has no stats yet in either GM or Pokebattler
}
# [Reminder] When using any Pokemon above, make sure these forms are ignored

COSMETIC_FORMS_UNIVERSAL = [  # Any Pokemon with these forms only have cosmetic changes
                              # (e.g. should not be considered a different raid boss)
    'FALL_2019', 'COPY_2019', 'COSTUME_2020', 'ADVENTURE_HAT_2020', 'WINTER_2020',
    # Note Pikachu Costume 2020 is Flying Pikachu with the move Fly, but it's the same as FLYING_5TH_ANNIV
    # VS_2019 is Pikachu Libre
    '2020', '2021', '2022'
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
    'SINISTEA': ['PHONY', 'ANTIQUE'],
    'POLTEAGEIST': ['PHONY', 'ANTIQUE'],

    # The following Pokemon have non-cosmetic forms, but one of them is identical to the "regular" form
    # (the one with no forms listed, which also appears in both Pokebattler and GM data),
    # hence this form is also considered cosmetic
    # [CAREFUL!!] Make sure the forms that Pokebattler uses on their Legacy T5 lists do NOT appear here!!!
    'BURMY': ['PLANT'],
    'WORMADAM': ['PLANT'],
    'SHAYMIN': ['LAND'],
    'CHERRIM': ['OVERCAST'],
    'DARMANITAN': ['STANDARD'],  # Galarian has no "regular" form, only Standard and Zen
    'TORNADUS': ['INCARNATE'],
    'THUNDURUS': ['INCARNATE'],
    'LANDORUS': ['INCARNATE'],
    'MELOETTA': ['ARIA'],  # Note that Pokebattler lists Aria Meloetta on their list,
                           # but it's fine since Meloetta raids as a whole are ignored
    'EISCUE': ['ICE'],
    'INDEEDEE': ['MALE'],
    'MORPEKO': ['FULL_BELLY'],  # Considering Hangry as non-cosmetic since Aura Wheel could be added one day
    'ZACIAN': [''],  # ['HERO'],
    'ZAMAZENTA': [''],  # ['HERO'],
    'PUMPKABOO': ['SMALL'],
    'GOURGEIST': ['SMALL'],
    'HOOPA': ['CONFINED'],
}
# [Reminder] When using any Pokemon above, make sure only their regular forms are considered
#  (and not considered again if one of the cosmetic forms already is)


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
}
SPECIAL_FORM_DISPLAY_NAMES = {
    'A': 'Armored',
    'VS_2019': 'Libre',
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
    'TRI_ATTACK': 'Tri-Attack',
}


# ----------------- Default Settings -----------------


MIN_LEVEL_DEFAULT = 30
MAX_LEVEL_DEFAULT = 50
LEVEL_STEP_DEFAULT = 5