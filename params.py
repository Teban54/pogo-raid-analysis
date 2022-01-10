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
}
SPECIAL_FORM_DISPLAY_NAMES = {}

CAN_EVOLVE_FORCED_TRUE = [  # Species that have special evolution requirements don't show up in Pokebattler's GM (but do )

]