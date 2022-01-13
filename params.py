"""
Parameters.
"""

JSON_DATA_PATH = "data/json/"

#POKEMON_TYPES = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Grass", "Ground", "Ghost",
#                 "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]  # Natural language
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

SPECIAL_BASE_DISPLAY_NAMES = {  # Default: Replace _ with space (Tapu Koko)
    'NIDORAN_FEMALE': 'Nidoran♀',
    'NIDORAN_MALE': 'Nidoran♂',
    'MR_MIME': 'Mr. Mime',
    'MIME_JR': 'Mime Jr.',
    'MR_RIME': 'Mr. Rime',
    'HO_OH': 'Ho-Oh',
    'Porygon_Z': 'Porygon-Z',
    'FARFETCHD': 'Farfetch\'d',
    'SIRFETCHD': 'Sirfetch\'d',
    'FLABEBE': 'Flabébé',
}
SPECIAL_FORM_DISPLAY_NAMES = {
    'A': 'Armored',
}

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
    'FURFROU': ['NATURAL', 'HEART', 'STAR', 'DIAMOND', 'DEBUTANTE', 'MATRON', 'DANDY', 'LA_REINE', 'KABUKI', 'PHARAOH'],
    'SINISTEA': ['PHONY', 'ANTIQUE'],
    'POLTEAGEIST': ['PHONY', 'ANTIQUE'],

    # The following Pokemon have non-cosmetic forms, but one of them is identical to the "regular" form
    # (the one with no forms listed, which also appears in both Pokebattler and GM data),
    # hence this form is also considered cosmetic
    'BURMY': ['PLANT'],
    'WORMADAM': ['PLANT'],
    'SHAYMIN': ['LAND'],
    'CHERRIM': ['OVERCAST'],
    'DARMANITAN': ['STANDARD'],  # Galarian has no "regular" form, only Standard and Zen
    'TORNADUS': ['INCARNATE'],
    'THUNDURUS': ['INCARNATE'],
    'LANDORUS': ['INCARNATE'],
    'MELOETTA': ['ARIA'],
    'EISCUE': ['ICE'],
    'INDEEDEE': ['MALE'],
    'MORPEKO': ['FULL_BELLY'],  # Considering Hangry as non-cosmetic since Aura Wheel could be added one day
    'ZACIAN': ['HERO'],
    'ZAMAZENTA': ['HERO'],
    'PUMPKABOO': ['SMALL'],
    'GOURGEIST': ['SMALL'],
    'HOOPA': ['CONFINED'],
}
# TODO: When using any Pokemon above, make sure only their regular forms are considered
#  (and not considered again if one of the cosmetic forms already is)

IGNORED_FORMS = {  # Forms that should not exist
    'URSHIFU': [''],  # Current GM has Urshifu "regular" form as mono Fighting
    'HONEDGE': [''],  # The Honedge line has no stats yet in either GM or Pokebattler
    'DOUBLADE': [''],
    'AEGISLASH': [''],
    'ZYGARDE': [''],  # Zygarde has no stats yet in either GM or Pokebattler
}
# TODO: When using any Pokemon above, make sure these forms are ignored

