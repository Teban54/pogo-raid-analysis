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
from pokemon import *


class RaidBoss:
    """
    Class for a specific raid boss, with the Pokemon,
    raid tier and possibly raid category.

    This is primarily used for parsing raid boss lists.
    """
    def __init__(self, pokebattler_JSON=None, pokemon_obj=None, pokemon_codename=None,
                 tier_codename=None, category_codename=None,
                 metadata=None):
        """
        Initialize the attributes and use the Pokebattler JSON information to fill them.
        :param pokebattler_JSON: JSON block from Pokebattler relating to this raid
        :param pokemon_obj: Pokemon object, in case JSON is not provided
        :param pokemon_codename: Code name of the Pokemon, in case JSON is not provided
        :param tier_codename: Code name of the raid tier
        :param category_codename: Code name of the raid category
        :param metadata: Current Metadata object (to initialize Pokemon object)
        """
        self.pokemon_codename = pokemon_codename  # Possibly None if JSON is provided
        self.pokemon = pokemon_obj
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
        if self.JSON:  # Either one of the three can be provided: JSON, pokemon, pokemon_codename
            self.pokemon = metadata.find_pokemon(self.pokemon_codename)
        elif self.pokemon:
            self.pokemon_codename = self.pokemon.name  # Metadata not required in this case
        else:
            self.pokemon = metadata.find_pokemon(self.pokemon_codename)

        if self.pokemon:
            self.pokemon_base = self.pokemon.base_codename
            self.pokemon_form = self.pokemon.form_codename  # Ignores shadow and mega
            self.is_mega = self.tier == "RAID_LEVEL_MEGA" or self.pokemon.is_mega
        else:
            print(f"Warning (RaidBoss.init_pokemon): Pokemon with code name {self.pokemon_codename} not found",
                file=sys.stderr)
            # Try parsing forms here just in case?


def pokemon_list_to_raid_boss_list(pokemon_list, tier):
    """
    Convert a list of Pokemon objects to a list of RaidBoss objects.
    :param pokemon_list: List of Pokemon bosses
    :param tier: Tier name or list of tier names, either natural language or code name
    :return; RaidBoss objects
    """
    tiers = [tier]
    if type(tier) is list:
        tiers = tier
    # tiers = [parse_raid_tier_str2code(tier) for tier in tiers]
    raid_bosses = []
    for tier in tiers:
        raid_bosses += [RaidBoss(pokemon_obj=pkm, tier_codename=parse_raid_tier_str2code(tier)) for pkm in pokemon_list]
    return raid_bosses
    # tier = parse_raid_tier_str2code(tier)
    # return [RaidBoss(pokemon_obj=pkm, tier_codename=tier) for pkm in pokemon_list]


def raid_boss_list_to_pokemon_list(raid_list):
    """
    Convert a list of RaidBoss objects to a list of Pokemon objects.
    :param raid_list: List of raid bosses
    :return; Pokemon objects
    """
    return [rb.pokemon for rb in raid_list]


# ----------------- Raid filtering and grouping -----------------


def filter_raids_by_criteria(raid_list, criterion_raid=None, criterion_pokemon=None, **kwargs):
    """
    Filter a list of raid bosses with a given criterion function for raids,
    and/or a criterion function for Pokemon.
    Returns all raid bosses that evaluate to True on both criterion functions.
    See also: filter_pokemon_by_criteria, filter_ensemble_by_criteria

    The criterion function for raids should take in at least one parameter,
    and the first must be a RaidBoss object.
    The criterion function for Pokemon should take in at least one parameter,
    and the first must be a Pokemon object.
    Additional arguments can be passed into filter_raids_by_criteria as **kwargs.

    Example:
        def is_higher_than_level(raid_boss, level_ceiling):
            return int(raid_boss.tier.replace("RAID_LEVEL_")) >= level_ceiling
        def is_form(pokemon, form):
            return pokemon.form_codename == form
        result = filter_raids_by_criteria(
            raid_list, criterion=is_higher_than_level, criterion_pokemon=is_form,
            level_ceiling=3, form='WINTER_2020')

    :param raid_list: List of RaidBoss objects to be filtered
    :param criterion_raid: A criterion function for raids as described above
    :param criterion_pokemon: A criterion function for Pokemon as described above
    :return: List of RaidBoss that evaluate to True on both criterion
    """
    return [raid for raid in raid_list
            if (criterion_raid is None or criterion_raid(raid, **kwargs))
            and (criterion_pokemon is None or criterion_pokemon(raid.pokemon, **kwargs))]


def criterion_not_ignore_raid(raid):
    """
    Returns True if the RaidBoss should NOT be ignored.
    An example of raids that should be ignored is Meloetta raids.
    We also ignore a raid if the featured Pokemon should be ignored.

    :param raid: RaidBoss object to be evaluated on
    :return: True if the RaidBoss should not be ignored
    """
    return (raid.pokemon_codename not in IGNORED_RAID_BOSSES.get(raid.tier, [])
            and criterion_not_ignore_pokemon(raid.pokemon))


def remove_raids_to_ignore(raid_list):
    """
    Given a list of RaidBoss, returns a new list that removes all raids that should be ignored.
    See also: remove_pokemon_to_ignore
    :param raid_list: List of RaidBoss objects
    :return: Filtered list of RaidBoss objects
    """
    return filter_raids_by_criteria(raid_list, criterion_raid=criterion_not_ignore_raid)


def group_raid_bosses_by_basename(boss_list, separate_shadows=True, separate_megas=True):
    """
    Given a list of RaidBoss objects, group them into a dict with the base names of their Pokemon as keys,
    and different forms as a list under that key.
    See also: group_pokemon_by_basename

    :param boss_list: List of RaidBoss objects
    :param separate_shadows: If True, each shadow will be considered as a separate base Pokemon,
        instead of as a form of the non-shadow variant.
    :param separate_megas: If True, each mega evolution will be considered as a separate base Pokemon,
        instead of as a form of the non-mega variant.
        This also means Mega X and Mega Y will be treated as different base Pokemon.
    :return: Dict of the following structure: {'GIRATINA': [<Giratina boss obj>, <Giratina-Origin boss obj>], ...}
    """
    ret = {}
    for boss in boss_list:
        pkm = boss.pokemon
        base = pkm.base_codename
        if pkm.is_shadow and separate_shadows:
            base += "_SHADOW_FORM"
            # Need to check shadows with forms (e.g. Shadow Darmanitan Zen) in future, but okay for now
        if pkm.is_mega and separate_megas:
            base = pkm.name
        if base not in ret:
            ret[base] = []
        ret[base].append(boss)
    return ret
