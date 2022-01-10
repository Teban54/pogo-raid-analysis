"""
Parameters.
"""

JSON_DATA_PATH = "data/json/"

POKEMON_TYPES = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Grass", "Ground", "Ghost",
                 "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]  # Natural language

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
}
