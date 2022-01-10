"""
This module includes two main types of utilities:
- A class for Pokemon species.
- Utilities related to Pokemon, e.g. typing.
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
    def __init__(self, pokebattler_JSON=None, GM_JSON=None):
        """
        Initialize the attributes and use the Pokebattler JSON information to fill them.
        :param pokebattler_JSON: JSON block from Pokebattler relating to this Pokemon
        :param GM_JSON: JSON block from Game Master relating to this Pokemon, if applicable
                (In practice, GM_JSON is typically left blank, since GM isn't loaded yet at this stage)
        """
        self.name = None
        self.type = None
        self.type2 = None
        self.base_attack = -1
        self.base_defense = -1
        self.base_stamina = -1
        self.pre_evo = None
        self.JSON = None
        self.base_codename = None  # "MR_MIME" when Pokemon is "MR_MIME_GALARIAN_FORM", or "VENUSAUR_MEGA"
        self.form_codename = None  # "GALARIAN" when Pokemon is "MR_MIME_GALARIAN_FORM"
        self.base_displayname = None
        self.form_displayname = None
        self.displayname = None
        self.is_legendary = False
        self.is_mythical = False
        self.is_shadow = False
        self.is_mega = False
        self.mega_codename = None  # "X", "Y"
        self.mega_displayname = None

        # The following are from GM
        self.GM_JSON = None
        self.evolutions = []

        if pokebattler_JSON:
            self.init_from_pokebattler(pokebattler_JSON)
            self.init_forms()
            self.init_display_names()
        if GM_JSON:
            self.init_from_GM(GM_JSON)

    def init_from_pokebattler(self, JSON):
        """
        Parse basic information from the Pokebattler JSON.
        :param JSON: JSON block from Pokebattler relating to this Pokemon
        """
        self.JSON = JSON
        self.name = JSON['pokemonId']
        self.type = parse_type_code2str(JSON['type'])
        if 'type2' in JSON:
            self.type2 = parse_type_code2str(JSON['type2'])
        self.base_attack = JSON['stats'].get('baseAttack', -1)
        self.base_defense = JSON['stats'].get('baseDefense', -1)
        self.base_stamina = JSON['stats'].get('baseStamina', -1)
        self.pre_evo = JSON.get('parentPokemonId', None)
        self.is_legendary = (JSON.get('rarity', '') == 'POKEMON_RARITY_LEGENDARY')
        self.is_mythical = (JSON.get('rarity', '') == 'POKEMON_RARITY_MYTHIC')

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
