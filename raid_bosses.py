"""
This module includes two main types of utilities:
- A class for raid bosses included on Pokebattler website, with its corresponding tier.
- Utilities for dealing with single or multiple raid bosses.

NOTE: Distinction between "raid tier" and "raid category":
- "Raid tier" is the actual tier or difficulty, regardless of the time when the raid is available.
  As of now, the only valid raid tiers are: 1, 2, 3, 4, 4.5, 5, 6, Mega.
  This is sometimes shown as "guess tier" in Pokebattler.
- "Raid category" is the category under which the boss is displayed in Pokebattler.
  It typically considers whether it is available in the past, present or future.
  Examples: "Future Mega Tier", "Legacy Tier 5".
"""

from utils import *
from params import *


class RaidBoss:
    """
    Class for a specific raid boss, with the Pokemon,
    raid tier and possibly raid category.

    This is primarily used for parsing raid boss lists.
    """
    def __init__(self, pokebattler_JSON=None, pokemon_codename=None, tier_codename=None, category_codename=None,
                 metadata=None):
        """
        Initialize the attributes and use the Pokebattler JSON information to fill them.
        :param pokebattler_JSON: JSON block from Pokebattler relating to this raid
        :param pokemon_codename: Code name of the Pokemon, in case JSON is not provided
        :param tier_codename: Code name of the raid tier
        :param category_codename: Code name of the raid category
        :param metadata: Current Metadata object (to initialize Pokemon object)
        """
        self.pokemon_codename = pokemon_codename  # Possibly None if JSON is provided
        self.pokemon = None
        self.tier = tier_codename
        self.category = category_codename
        self.pokemon_base = None  # "MR_MIME" when Pokemon is "MR_MIME_GALARIAN_FORM", or "VENUSAUR" for "VENUSAUR_MEGA"
        self.pokemon_form = None  # "GALARIAN" when Pokemon is "MR_MIME_GALARIAN_FORM"; Ignores shadow and mega
        # The two fields above are just for convenience
        self.is_mega = False
        self.JSON = None

        if pokebattler_JSON:
            self.init_from_pokebattler(pokebattler_JSON)

        self.init_pokemon(metadata)

    def init_from_pokebattler(self, JSON):
        """
        Parse basic information from the Pokebattler JSON.
        :param JSON: JSON block from Pokebattler relating to this raid
        """
        self.JSON = JSON
        self.pokemon_codename = JSON['pokemon']
        if JSON['pokemonId'] != self.pokemon_codename:  # Help debug
            print(f"Warning (RaidBoss.init_from_pokebattler): "
                  f"pokemonId {JSON['pokemonId']} is different from pokemon {JSON['pokemon']}",
                  file=sys.stderr)

    def init_pokemon(self, metadata):
        """
        Finds the Pokemon object from codename, and process relevant information
        to populate other fields of the RaidBoss object.
        This populates the following fields: pokemon, pokemon_base, pokemon_form, is_mega.
        :param metadata: Metadata object
        """
        self.pokemon = metadata.find_pokemon(self.pokemon_codename)
        if self.pokemon:
            self.pokemon_base = self.pokemon.base_codename
            self.pokemon_form = self.pokemon.form_codename  # Ignores shadow and mega
            self.is_mega = self.tier == "RAID_LEVEL_MEGA" or self.pokemon.is_mega
        else:
            print(f"Warning (RaidBoss.init_pokemon): Pokemon with code name {self.pokemon_codename} not found",
                file=sys.stderr)
            # Try parsing forms here just in case?
