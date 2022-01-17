"""
This module includes two main types of utilities:
- A class for a list of criteria that attackers have to satisfy.
- Utilities for dealing with attacker ensembles.

An AttackerCriteria object contains a collection of criteria that attackers need to satisfy.
Its main goal is to choose which attackers to analyze from the rankings lists.

The following filters can be added to a single AttackerCriteria object.
For an attacker to "meet" the AttackerCriteria, it has to pass ALL specified filters.
- Charged move type(s). This is an approximation for "attacker type", and should be used
  primarily for type-based filtering, instead of Pokemon types.
  Rationale:
    - Some attackers function without STAB: Shadow Ball Mewtwo, Shadow Ball Darkrai, etc.
    - Some attackers use fast and charged moves of different types in some situations:
      Swampert (MS/HC), Blaziken (Counter/BB), Mewtwo (PC/SB), Terrakion (SD/SS), etc.
    - Some attackers with type A/B prefer to use type A moves against a certain boss,
      which would skew the results if compared with attackers of type B.
      Garchomp against Reshiram and Zekrom is perhaps the most well-known example.
    - In both cases, charged move typing usually does the best in describing what "type"
      of attacker the Pokemon is functionally acting as.
        - Counter/Blast Burn Blaziken is a perfectly fine option, and everyone considers it as
          a fire attacker. No need to force Fire Spin on it in situations where Counter is better.
        - This does have the issue of using Dragon Tail/Earth Power Garchomp at times,
          or doing weird things to Terrakion (and Smack Down/Crunch Tyranitar against Lugia),
          but overall it's worth the tradeoff.
  If multiple types are included, all Pokemon with charged moves of these types will be considered.
- Minimum level, maximum level, and level step size.
- Whether the attacker is or is not a legendary, shadow or mega.
- Pokebattler Trainer ID. If specified, only attackers from that user's Pokebox will be used.
  Still subject to other filters, e.g. only consider grass attackers from the Pokebox.
- Specific Pokemon names (code names). If specified, only these Pokemon will be considered.
  Still subject to other filters.
- Pokemon type(s). Only use this if you know what you're doing.
  If multiple types are included, all Pokemon with these types will be considered.
- Fast move type(s). Only use this if you know what you're doing.

AttackerCriteriaMulti class is used as an "OR" of multiple AttackerCriteria objects.
I.e. An attacker that satisfies any AttackerCriteria object is eligible for AttackerCriteriaMulti.
Examples: Grass attackers in my Pokebox OR grass attackers by level, L40 shadows OR L50 non-shadows.
Since AttackerCriteriaMulti includes more APIs, it's recommended to build an AttackerCriteriaMulti
even if only one set of criteria is used.
"""

from utils import *
from params import *
from pokemon import *


class AttackerCriteria:
    """
    Class for a single set of criteria for attackers.
    """
    def __init__(self, metadata=None, pokemon_types=None, fast_types=None, charged_types=None,
                 min_level=30, max_level=50, level_step=5,
                 pokemon_codenames=None, trainer_id=None,
                 is_legendary=False, is_not_legendary=False,
                 is_mythical=False, is_not_mythical=False,
                 is_legendary_or_mythical=False, is_not_legendary_or_mythical=False,
                 is_shadow=False, is_not_shadow=False,
                 is_mega=False, is_not_mega=False):
        """
        Initialize all filters.

        :param metadata: Current Metadata object
        :param pokemon_types: Types of Pokemon to be considered, as list of natural names ("Dragon")
            or a single string
        :param fast_types: Types of fast moves to be considered, as list of natural names ("Dragon")
            or a single string
        :param charged_types: Types of fast moves to be considered, as list of natural names ("Dragon")
            or a single string.
            This should be used as the primary way to filter attackers by type.
        :param min_level: Minimum attacker level, inclusive
        :param max_level: Maximum attacker level, inclusive
        :param level_step: Step size for level, either 0.5 or integer
        :param pokemon_codenames: List of codenames of all Pokemon so that attackers are restricted to
            these options, if necessary. Still subject to other filters.
            If None, all attackers will be considered.
        :param trainer_id: Pokebattler Trainer ID if a trainer's own Pokebox is used.
            If None, use all attackers by level.
        :param is_legendary: If True, only consider legendary attackers
        :param is_not_legendary: If True, only consider non-legendary attackers
        :param is_mythical: If True, only consider mythical attackers
        :param is_not_mythical: If True, only consider non-mythical attackers
        :param is_legendary_or_mythical: If True, only consider legendary or mythical attackers
        :param is_not_legendary_or_mythical: If True, only consider non-legendary or mythical attackers
        :param is_shadow: If True, only consider shadow attackers
        :param is_not_shadow: If True, only consider non-shadow attackers
        :param is_mega: If True, only consider mega attackers
        :param is_not_mega: If True, only consider non-mega attackers
        """
        def parse_types(types):
            """
            Parse the input types.
            :param types: None, a string or a list mixed with code and natural names.
            :return: Well-formatted list, or None if the filter shouldn't be active
            """
            if types is None:
                return None
            parsed = parse_type_codes2strs(types if type(types) is list else [types])
            if not parsed:  # Empty, as a result of all inputs removed
                return None
            return parsed

        self.pokemon_types = parse_types(pokemon_types)
        self.fast_types = parse_types(fast_types)
        self.charged_types = parse_types(charged_types)
        self.min_level = min_level
        self.max_level = max_level
        self.level_step = level_step
        self.pokemon_codenames = pokemon_codenames
        self.trainer_id = trainer_id
        self.is_legendary = is_legendary
        self.is_not_legendary = is_not_legendary
        self.is_mythical = is_mythical
        self.is_not_mythical = is_not_mythical
        self.is_legendary_or_mythical = is_legendary_or_mythical
        self.is_not_legendary_or_mythical = is_not_legendary_or_mythical
        self.is_shadow = is_shadow
        self.is_not_shadow = is_not_shadow
        self.is_mega = is_mega
        self.is_not_mega = is_not_mega
        self.metadata = metadata

    def check_attacker(self, pokemon=None, pokemon_codename=None, level=None,
                       fast=None, fast_codename=None,
                       charged=None, charged_codename=None):
        """
        Check if a particular attacker with fast and charged moves meets ALL criteria
        in this AttackerCriteria object.
        Note:
        - Trainer ID is not checked. Instead, it's applied to Pokebattler simulation settings.
        - If fast or charged moves are not given, those comparisons are IGNORED.

        :param pokemon_codename: Pokemon codename
        :param pokemon: Pokemon object, if codename is not given
        :param level: Level of attacker, as string or numerical value
        :param fast_codename: Fast move codename
        :param fast: Fast Move object, if codename is not given
        :param charged_codename: Charged move codename
        :param charged: Charged Move object, if codename is not given
        :return: Whether the attacker meets all criteria
        """
        if not pokemon:
            if not pokemon_codename:
                print(f"Error (AttackerCriteria.check_attacker): Neither Pokemon object nor codename provided.",
                      file=sys.stderr)
                return False
            pokemon = self.metadata.find_pokemon(pokemon_codename)
        ignore_fast = not self.fast_types
        if self.fast_types and not fast:
            if not fast_codename:
                print(f"Warning (AttackerCriteria.check_attacker): Neither fast move object nor codename provided. "
                      f"IGNORING the fast move typing check.",
                      file=sys.stderr)
                ignore_fast = True
            fast = self.metadata.find_move(fast_codename)
        ignore_charged = not self.charged_types
        if self.charged_types and not charged:
            if not charged_codename:
                print(f"Warning (AttackerCriteria.check_attacker): Neither charged move object nor codename provided. "
                      f"IGNORING the charged move typing check.",
                      file=sys.stderr)
                ignore_charged = True
            charged = self.metadata.find_move(fast_codename)

        return all([
            not self.pokemon_types or criterion_is_types(pokemon, self.pokemon_types),
            ignore_fast or fast.type in self.fast_types,
            ignore_charged or charged.type in self.charged_types,
            not level or is_level_in_range(level, self.min_level, self.max_level),  # Mostly for Pokebox
            not self.pokemon_codenames or pokemon.name in self.pokemon_codenames,
            criterion_legendary(pokemon, self.is_legendary, self.is_not_legendary),
            criterion_mythical(pokemon, self.is_mythical, self.is_not_mythical),
            criterion_legendary_or_mythical(pokemon, self.is_legendary_or_mythical, self.is_not_legendary_or_mythical),
            criterion_shadow(pokemon, self.is_shadow, self.is_not_shadow),
            criterion_mega(pokemon, self.is_mega, self.is_not_mega),
        ])

class AttackerCriteriaMulti:
    """
    Class for multiple sets of criteria for attackers, such that an attacker only
    needs to satisfy any one set of criteria.

    Many functions in this class are to get values for Pokabattler API.
    """
    def __init__(self, sets, metadata=None):
        """
        Initialize with all sets as AttackerCriteria objects.
        """
        self.sets = sets
        self.metadata = metadata

    def check_attacker(self, **kwargs):
        """
        Check if a particular attacker with fast and charged moves satisfies
        ANY of the individual AttackerCriteria objects.

        :param pokemon_codename: Pokemon codename
        :param pokemon: Pokemon object, if codename is not given
        :param level: Level of attacker, as string or numerical value
        :param fast_codename: Fast move codename
        :param fast: Fast Move object, if codename is not given
        :param charged_codename: Charged move codename
        :param charged: Charged Move object, if codename is not given
        :return: Whether the attacker meets any individual AttackerCriteria
        """
        return any(criteria.check_attacker(**kwargs) for criteria in self.sets)

    def all_levels(self):
        """
        Return all individual attacker levels that needs to be considered across
        all AttackerCriteria sets.
        :return: List of all levels to be considered
        """
        all_levels = list(set([
            lvl
            for criteria in self.sets
            for lvl in get_levels_in_range(criteria.min_level, criteria.max_level, criteria.level_step)]))
        return sorted(all_levels)

    def min_level(self):
        """
        Return the minimum level that needs to be considered across all AttackerCriteria sets.
        :return: Minimum level to be considered
        """
        return min(criteria.min_level for criteria in self.sets)

    def max_level(self):
        """
        Return the maximum level that needs to be considered across all AttackerCriteria sets.
        :return: Maximum level to be considered
        """
        return max(criteria.max_level for criteria in self.sets)

    def pokebattler_legendary(self):
        """
        Checks whether the "show legendaries" option in Pokebatter needs to be turned on.
        :return: Value of the "show legendaries" option to be used for Pokebattler API
        """
        return any(not (criteria.is_not_legendary_or_mythical
                        or criteria.is_not_legendary and criteria.is_not_mythical)
                   for criteria in self.sets)

    def pokebattler_shadow(self):
        """
        Checks whether the "show shadows" option in Pokebatter needs to be turned on.
        :return: Value of the "show shadows" option to be used for Pokebattler API
        """
        return any(not criteria.is_not_shadow for criteria in self.sets)

    def pokebattler_mega(self):
        """
        Checks whether the "show megas" option in Pokebatter needs to be turned on.
        :return: Value of the "show megas" option to be used for Pokebattler API
        """
        return any(not criteria.is_not_mega for criteria in self.sets)

    def pokebattler_pokemon_types(self):
        """
        If all individual sets of AttackerCriteria has a limit on Pokemon types,
        return the union of all these sets. This can be used in Pokebattler API
        to limit the types of attackers included.
        If any AttackerCriteria does not enforce a limit on Pokemon types, return None.
        :return: List of attacker Pokemon types in code name, or None if should not be enforced
        """
        if any(not criteria.pokemon_types for criteria in self.sets):
            return None
        return list(set([parse_type_str2code(tp)  # Code name
                         for criteria in self.sets for tp in criteria.pokemon_types]))
