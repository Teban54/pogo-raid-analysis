"""
This module includes two main types of utilities:
- A class for Pokemon species.
- Utilities for dealing with single or multiple Pokemon.
    (Utilities related to typing without any specific Pokemon are in utils.py.)
"""

from utils import *
from params import *


class Pokemon:
    """
    Class for a Pokemon species.
    Not a specific Pokemon instance with level, IVs, etc.

    This is primarily used for raid boss lists and type filtering.
    Therefore, limited data is parsed for now.
    """
    def __init__(self, pokebattler_JSON=None, GM_JSON=None, metadata=None):
        """
        Initialize the attributes and use the Pokebattler JSON information to fill them.
        :param pokebattler_JSON: JSON block from Pokebattler relating to this Pokemon
        :param GM_JSON: JSON block from Game Master relating to this Pokemon, if applicable
                (In practice, GM_JSON is typically left blank, since GM isn't loaded yet at this stage)
        :param metadata: Current Metadata object (to lookup moves)
        """
        self.name = None
        self.base_codename = None  # "MR_MIME" when Pokemon is "MR_MIME_GALARIAN_FORM", or "VENUSAUR" for "VENUSAUR_MEGA"
        self.form_codename = None  # "GALARIAN" when Pokemon is "MR_MIME_GALARIAN_FORM"
        self.base_displayname = None
        self.form_displayname = None
        self.displayname = None

        self.type = None  # Natural language, e.g. "Dragon"
        self.type2 = None
        self.types = []  # List of all types, length 1 or 2
        self.base_attack = -1
        self.base_defense = -1
        self.base_stamina = -1

        self.pre_evo = None
        self.is_legendary = False
        self.is_mythical = False
        self.is_shadow = False
        self.is_mega = False
        self.mega_codename = None  # "X", "Y"
        self.mega_displayname = None

        self.fast_moves = []  # List of code names, include all legacy moves (ETM or not), from Pokebattler data
        self.charged_moves = []  # Not Move objects!!!
        self.movesets = []  # "tmMovesets" from Pokebattler, includes all possible movesets (e.g. Mud Shot/Rock Blast Golem)
        self.current_movesets = []  # From Pokebattler
        # Moveset lists follow Pokebattler format:
        # [{'quickMove': 'ROCK_THROW_FAST', 'cinematicMove': 'EARTHQUAKE'}, ...]

        self.JSON = None
        self.metadata = metadata

        # The following are from GM
        self.GM_JSON = None
        self.evolutions = []

        # Load data
        if pokebattler_JSON:
            self.init_from_pokebattler(pokebattler_JSON)
            self.init_forms()
            self.init_display_names()
        if GM_JSON:
            self.init_from_GM(GM_JSON)

    # ----------------- Initialization -----------------

    def init_from_pokebattler(self, JSON):
        """
        Parse basic information from the Pokebattler JSON.
        :param JSON: JSON block from Pokebattler relating to this Pokemon
        """
        self.JSON = JSON
        self.name = JSON['pokemonId']
        self.type = parse_type_code2str(JSON['type'])
        self.types.append(self.type)
        if 'type2' in JSON:
            self.type2 = parse_type_code2str(JSON['type2'])
            self.types.append(self.type2)
        self.base_attack = JSON['stats'].get('baseAttack', -1)
        self.base_defense = JSON['stats'].get('baseDefense', -1)
        self.base_stamina = JSON['stats'].get('baseStamina', -1)
        self.pre_evo = JSON.get('parentPokemonId', None)
        self.is_legendary = (JSON.get('rarity', '') == 'POKEMON_RARITY_LEGENDARY')
        self.is_mythical = (JSON.get('rarity', '') == 'POKEMON_RARITY_MYTHIC')
        self.fast_moves = JSON['quickMoves']
        self.charged_moves = JSON['cinematicMoves']
        self.movesets = JSON['tmMovesets']
        self.current_movesets = JSON['currentMovesets']

    def init_forms(self):
        """
        Process the form information of this Pokemon, including shadow.
        This populates the following fields: base_codename, form_codename, is_shadow, is_mega, mega_codename.
        """
        self.base_codename = self.JSON['pokedex']['pokemonId']
        if self.base_codename.endswith("_MEGA"):
            # For unreleased megas, Pokebattler currently has its pokedex pokeminId as "ALAKAZAM_MEGA"
            # But released megas have the base form "VENUSAUR" correct
            self.base_codename = self.base_codename[:-5]
        elif self.base_codename.endswith("_MEGA_X") or self.base_codename.endswith("_MEGA_Y"):
            self.base_codename = self.base_codename[:-7]

        if self.JSON.get('form', None):
            # This means an alternate form, not shadow
            form_codename = self.JSON.get('form', None).replace(self.base_codename, "", 1)
            form_codename = form_codename[1:]  # First char is '_'
            self.form_codename = form_codename
        if self.name.endswith("_SHADOW_FORM"):  # Technically both cases (above and this) can happen, but Pokebattler can't handle both concurrently yet
            self.is_shadow = True
        if self.name.endswith("_MEGA"):
            self.is_mega = True
            self.mega_codename = None
        elif self.name.endswith("_MEGA_X") or self.name.endswith("_MEGA_Y"):
            self.is_mega = True
            self.mega_codename = self.name[-1:]

    def init_display_names(self):
        """
        Process the display names for both the base name (e.g. Mr. Mime) and the form (e.g. Galarian).
        Includes Shadow and Mega at the start if applicable.
        This populates the following fields: base_displayname, form_displayname, displayname.
        """
        if self.displayname:  # Already filled out
            return
        # Base display name
        if self.base_codename in SPECIAL_BASE_DISPLAY_NAMES:
            self.base_displayname = SPECIAL_BASE_DISPLAY_NAMES[self.base_codename]
        else:
            self.base_displayname = codename_to_displayname(self.base_codename)

        # Form display name
        if self.form_codename:
            if self.form_codename in SPECIAL_FORM_DISPLAY_NAMES:
                self.form_displayname = SPECIAL_FORM_DISPLAY_NAMES[self.form_codename]
            else:
                self.form_displayname = codename_to_displayname(self.form_codename)

        # Mega display name (for X and Y)
        if self.is_mega:
            self.mega_displayname = codename_to_displayname(self.mega_codename)

        # Full display name
        self.displayname = self.base_displayname
        if self.is_shadow:
            self.displayname = "Shadow " + self.displayname
        if self.is_mega:
            self.displayname = "Mega " + self.displayname
            if self.mega_displayname:  # X and Y
                self.displayname += " " + self.mega_displayname
        if self.form_codename:
            self.displayname += f" ({self.form_displayname})"

    def init_from_GM(self, JSON, shadow=False):
        """
        Parse some additional information from the Game Master JSON.
        Currently, the main purpose of this is to add evolution lines to the Pokedex.

        :param JSON: JSON block from Game Master relating to this Pokemon.
                The block should have 'templateId': 'V0555_POKEMON_DARMANITAN_GALARIAN_STANDARD',
                and a 'pokemonSettings' field.
                It should not have a 'data' field (i.e. information should not be nested).
        :param shadow: Whether this current Pokemon object is a Shadow Pokemon.
                This should be redundant because self.is_shadow exists, but is fine as a double check.
        """
        self.GM_JSON = JSON
        shadow = self.is_shadow or shadow
        for evo_block in JSON['pokemonSettings'].get('evolutionBranch', []):
            if 'evolution' in evo_block:  # Mega evolutions also use the evolutionBranch field, but with temporaryEvolution instead
                evo_codename = evo_block['evolution']
                if 'form' in evo_block and not evo_block['form'].endswith("_NORMAL"):
                    evo_codename = evo_block['form'] + '_FORM'
                self.evolutions.append(evo_codename + ('_SHADOW_FORM' if shadow else ''))
                # This could cause two "_FORM"'s if there's a shadow with a special form, but that's not a thing yet

    # ----------------- Moves -----------------

    def is_move_stab(self, move):
        """
        Check if a given move is STAB on this Pokemon.
        :param move: Move, either as a Move object or as a string (will lookup in metadata if string)
        :return: Whether the move is STAB. Returns False in case of errors.
        """
        if type(move) is str:
            if not self.metadata:
                print(f"Warning (Pokemon.is_move_stab): Metadata not found", file=sys.stderr)
                return False
            move = self.metadata.find_move(move)
        return move.type in self.types

    def get_fast_moves(self, stab_only=False):
        """
        Get a list of fast moves as Move objects.
        :param stab_only: If True, only STAB moves are returned.
        :return: List of fast moves as Move objects
        """
        if not self.metadata:
            print(f"Warning (Pokemon.get_fast_moves): Metadata not found", file=sys.stderr)
            return []
        moves = self.metadata.find_moves(self.fast_moves)
        if stab_only:
            moves = [move for move in moves if self.is_move_stab(move)]
        return moves

    def get_charged_moves(self, stab_only=False):
        """
        Get a list of charged moves as Move objects.
        :param stab_only: If True, only STAB moves are returned.
        :return: List of charged moves as Move objects
        """
        if not self.metadata:
            print(f"Warning (Pokemon.get_charged_moves): Metadata not found", file=sys.stderr)
            return []
        moves = self.metadata.find_moves(self.charged_moves)
        if stab_only:
            moves = [move for move in moves if self.is_move_stab(move)]
        return moves


# ----------------- Pokemon filtering and grouping -----------------


def subtract_from_pokemon_list(list1, list2):
    """
    Given two lists of Pokemon, return "list1 - list2": all Pokemon in list 1
    but not in list 2.
    Does not modify either lists.

    :param list1: List of Pokemon to be considered
    :param list2: List or collection of all Pokemon to be removed
    :return: All Pokemon in list 1 but not list 2
    """
    list2_names = set(pkm.name for pkm in list2)
    return [pkm for pkm in list1 if pkm.name not in list2_names]


def union_pokemon_list(list1, list2):
    """
    Given two lists of Pokemon, return "list1 \cup list2": all Pokemon in either list 1
    or list 2, or both.
    Does not modify either lists.

    :param list1: List of Pokemon
    :param list2: List of Pokemon
    :return: All Pokemon in either list 1 or list 2
    """
    ret = list(list1)
    ret.extend(subtract_from_pokemon_list(list2, list1))
    return ret


def intersect_pokemon_list(list1, list2):
    """
    Given two lists of Pokemon, return "list1 \cap list2": all Pokemon in both list 1
    and list 2.
    Does not modify either lists.

    :param list1: List of Pokemon
    :param list2: List of Pokemon
    :return: All Pokemon in both list 1 and list 2
    """
    list2_names = set(pkm.name for pkm in list2)
    return [pkm for pkm in list1 if pkm.name in list2_names]


def filter_pokemon_by_criteria(pkm_list, criterion, **kwargs):
    """
    Filter a list of Pokemon with a given criterion function.
    Returns all Pokemon that evaluate to True on the criterion function.
    See also: filter_raids_by_criteria, filter_ensemble_by_criteria

    The criterion function should take in at least one parameter, and the first must be a Pokemon object.
    Additional arguments can be passed into filter_pokemon_by_criteria as **kwargs.

    Example:
        def is_form(pokemon, form):
            return pokemon.form_codename == form
        result = filter_pokemon_by_criteria(pokemon_list, is_form, form='WINTER_2020')

    :param pkm_list: List of Pokemon objects to be filtered
    :param criterion: A criterion function as described above
    :return: List of Pokemon that evaluate to True on the criterion
    """
    return [pkm for pkm in pkm_list if criterion(pkm, **kwargs)]


def criterion_not_ignore_pokemon(pokemon):
    """
    Returns True if the Pokemon and form should NOT be ignored.
    An example of forms that should be ignored is cosmetic forms.
    :param pokemon: Pokemon object to be evaluated on
    :return: True if the Pokemon should not be ignored
    """
    form = pokemon.form_codename if pokemon.form_codename is not None else ''
    return (form not in COSMETIC_FORMS_UNIVERSAL
            and form not in COSMETIC_FORMS_PER_POKEMON.get(pokemon.base_codename, [])
            and form not in IGNORED_FORMS.get(pokemon.base_codename, []))


def remove_pokemon_to_ignore(pkm_list):
    """
    Given a list of Pokemon, return a new list that removes all cosmetic forms
    and other Pokemon or forms that should be ignored.
    See also: remove_raids_to_ignore
    :param pkm_list: List of Pokemon objects
    :return: Filtered list of Pokemon objects
    """
    return filter_pokemon_by_criteria(pkm_list, criterion_not_ignore_pokemon)


def criterion_weak_to_contender_type(pokemon, attack_type=None):
    """
    Return True if the attacking type is a contender type against the Pokemon.
    E.g. If the given attacking type is Ice, returns True if the Pokemon is
    a mono grass/flying/dragon types, or Rayquaza, Landorus, etc.

    :param pokemon: Defending Pokemon object to be evaluated on
    :param attack_type: Attacking type, as either natural language or code name
    :return: True if the attacking type is a contender type against the given defending Pokemon
    """
    return is_contender_type(attack_type, pokemon.types)


def criterion_weak_to_contender_types(pokemon, attack_types=[]):
    """
    Return True if any of the attacking types is a contender type against the Pokemon.
    E.g. If the given attacking type is Ice, returns True if the Pokemon is
    a mono grass/flying/dragon types, or Rayquaza, Landorus, etc.
    If there are no types given, return False.

    :param pokemon: Defending Pokemon object to be evaluated on
    :param attack_types: List of attacking types, as either natural language or code name
    :return: True if any of the attacking types is a contender type against the given defending Pokemon
    """
    if not attack_types:
        return False
    return any(is_contender_type(attack_type, pokemon.types) for attack_type in attack_types)


def criterion_evo_stage(pokemon, keep_final_stage=True, keep_pre_evo=False):
    """
    Return True if the Pokemon's evolution stage matches requirements:
    a final stage Pokemon (Venusaur, Lapras, Pikachu Libre),
    or a pre-evolution Pokemon (e.g. Bulbasaur, Ivysaur, Bonsly).
    Mega evolutions are not considered as evolutions.

    :param pokemon: Pokemon object to be evaluated on
    :param keep_final_stage: If True, returns True if the Pokemon is a final stage Pokemon
    :param keep_pre_evo: If True, returns True if the Pokemon is a pre-evolution Pokemon
    :return: Whether the Pokemon satisfies required evolution stages
    """
    def is_final_stage(pkm):
        return not pkm.evolutions
    return (keep_final_stage and is_final_stage(pokemon)
            or keep_pre_evo and not is_final_stage(pokemon))


def criterion_shadow(pokemon, is_shadow=False, is_not_shadow=False):
    """
    Return True if the Pokemon matches the given shadow requirements: is or is not a shadow.

    :param pokemon: Pokemon object to be evaluated on
    :param is_shadow: If True, returns True if and only if the Pokemon is a shadow.
        Ignores all other parameters.
        If False, has no effect.
    :param is_not_shadow: If True, returns True only if the Pokemon is not a shadow.
        If False, has no effect.
    :return: Whether the Pokemon satisfies the shadow requirements
    """
    return (pokemon.is_shadow if is_shadow
            else not pokemon.is_shadow if is_not_shadow
            else True)


def criterion_mega(pokemon, is_mega=False, is_not_mega=False):
    """
    Return True if the Pokemon matches the given mega requirements: is or is not a mega.

    :param pokemon: Pokemon object to be evaluated on
    :param is_mega: If True, returns True if and only if the Pokemon is a mega.
        Ignores all other parameters.
        If False, has no effect.
    :param is_not_mega: If True, returns True only if the Pokemon is not a mega.
        If False, has no effect.
    :return: Whether the Pokemon satisfies the mega requirements
    """
    return (pokemon.is_mega if is_mega
            else not pokemon.is_mega if is_not_mega
            else True)


def criterion_legendary(pokemon, is_legendary=False, is_not_legendary=False):
    """
    Return True if the Pokemon matches the given legendary requirements: is or is not a legendary.
    NOTE: Mythicals are not considered as legendaries for this purpose.

    :param pokemon: Pokemon object to be evaluated on
    :param is_legendary: If True, returns True if and only if the Pokemon is a legendary.
        Ignores all other parameters.
        If False, has no effect.
    :param is_not_legendary: If True, returns True only if the Pokemon is not a legendary.
        If False, has no effect.
    :return: Whether the Pokemon satisfies the legendary requirements
    """
    return (pokemon.is_legendary if is_legendary
            else not pokemon.is_legendary if is_not_legendary
            else True)


def criterion_mythical(pokemon, is_mythical=False, is_not_mythical=False):
    """
    Return True if the Pokemon matches the given mythical requirements: is or is not a mythical.

    :param pokemon: Pokemon object to be evaluated on
    :param is_mythical: If True, returns True if and only if the Pokemon is a mythical.
        Ignores all other parameters.
        If False, has no effect.
    :param is_not_mythical: If True, returns True only if the Pokemon is not a mythical.
        If False, has no effect.
    :return: Whether the Pokemon satisfies the mythical requirements
    """
    return (pokemon.is_mythical if is_mythical
            else not pokemon.is_mythical if is_not_mythical
            else True)


def criterion_legendary_or_mythical(pokemon, is_legendary_or_mythical=False,
                                    is_not_legendary_or_mythical=False):
    """
    Return True if the Pokemon matches the given legendary or requirements:
    is legendary or mythical, or is not legendary nor mythical.

    :param pokemon: Pokemon object to be evaluated on
    :param is_legendary_or_mythical: If True, returns True if and only if the Pokemon is legendary or mythical.
        Ignores all other parameters.
        If False, has no effect.
    :param is_not_legendary_or_mythical: If True, returns True only if the Pokemon is not legendary nor mythical.
        If False, has no effect.
    :return: Whether the Pokemon satisfies the legendary or mythical requirements
    """
    return (pokemon.is_legendary or pokemon.is_mythical if is_legendary_or_mythical
            else not (pokemon.is_legendary or pokemon.is_mythical) if is_not_legendary_or_mythical
            else True)


def group_pokemon_by_basename(pkm_list, separate_shadows=True, separate_megas=True):
    """
    Given a list of Pokemon, group them into a dict with the base names as keys,
    and different forms as a list under that key.
    See also: group_raid_bosses_by_basename

    :param pkm_list: List of Pokemon objects
    :param separate_shadows: If True, each shadow will be considered as a separate base Pokemon,
        instead of as a form of the non-shadow variant.
    :param separate_megas: If True, each mega evolution will be considered as a separate base Pokemon,
        instead of as a form of the non-mega variant.
        This also means Mega X and Mega Y will be treated as different base Pokemon.
    :return: Dict of the following structure: {'GIRATINA': [<Giratina object>, <Giratina-Origin object>], ...}
    """
    ret = {}
    for pkm in pkm_list:
        base = pkm.base_codename
        if pkm.is_shadow and separate_shadows:
            base += "_SHADOW_FORM"
            # Need to check shadows with forms (e.g. Shadow Darmanitan Zen) in future, but okay for now
        if pkm.is_mega and separate_megas:
            base = pkm.name
        if base not in ret:
            ret[base] = []
        ret[base].append(pkm)
    return ret


