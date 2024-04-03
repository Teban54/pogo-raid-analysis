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
                 min_level=MIN_LEVEL_DEFAULT, max_level=MAX_LEVEL_DEFAULT, level_step=LEVEL_STEP_DEFAULT,
                 pokemon_codenames=None, pokemon_codenames_and_moves=None, trainer_id=None,
                 is_legendary=False, is_not_legendary=False,
                 is_mythical=False, is_not_mythical=False,
                 is_legendary_or_mythical=False, is_not_legendary_or_mythical=False,
                 is_shadow=False, is_not_shadow=False,
                 is_mega=False, is_not_mega=False,
                 exclude_codenames=None):
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
        :param pokemon_codenames_and_moves: List of tuples of Pokemon codenames and movesets
            so that attackers are restricted to these options, if necessary. Still subject to other filters.
            Possibly including IVs.
            Format:
            [
                ("URSALUNA", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
                ("URSALUNA", "TACKLE_FAST", "HIGH_HORSEPOWER"),
                ("GOLURK_SHADOW_FORM", "MUD_SLAP_FAST", "EARTH_POWER"),
                ("GARCHOMP_MEGA", "MUD_SHOT_FAST", "EARTH_POWER", "10/10/10"),
                ...
            ]
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
        :param exclude_codenames: List of codenames of all Pokemon to be excluded, regardless of other filters.
        """
        def parse_types(types):
            """
            Parse the input types.
            :param types: None, a string or a list mixed with code and natural names.
            :return: Well-formatted list, or None if the filter shouldn't be active
            """
            if types is None or not types:
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
        self.pokemon_codenames_and_moves = pokemon_codenames_and_moves
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
        self.exclude_codenames = exclude_codenames

        if self.pokemon_codenames and type(self.pokemon_codenames) is str:
            self.pokemon_codenames = [self.pokemon_codenames]
        if self.pokemon_codenames_and_moves and type(self.pokemon_codenames_and_moves) is tuple:
            self.pokemon_codenames_and_moves = [self.pokemon_codenames_and_moves]
        if self.exclude_codenames and type(self.exclude_codenames) is str:
            self.exclude_codenames = [self.exclude_codenames]

    def check_attacker(self, pokemon=None, pokemon_codename=None, level=None, iv=None,
                       fast=None, fast_codename=None,
                       charged=None, charged_codename=None, ignore_specific_codenames_and_moves=False):
        """
        Check if a particular attacker with fast and charged moves meets ALL criteria
        in this AttackerCriteria object.
        Note:
        - Trainer ID is not checked. Instead, it's applied to Pokebattler simulation settings.
        - If fast or charged moves are not given, those comparisons are IGNORED.

        :param pokemon_codename: Pokemon codename
        :param pokemon: Pokemon object, if codename is not given
        :param level: Level of attacker, as string or numerical value
        :param iv: IV of attacker, as string "15\\15\\15"
        :param fast_codename: Fast move codename
        :param fast: Fast Move object, if codename is not given
        :param charged_codename: Charged move codename
        :param charged: Charged Move object, if codename is not given
        :param ignore_specific_codenames_and_moves: If True, always returns False if this AttackerCriteria includes
            a check for Pokemon codenames and moves. The effect of this is that an attacker can only pass
            AttackerCriteriaMulti via single AttackerCriteria objects that do not focus on a whitelist, but
            on generic criteria (e.g. typing).
            This is used to determine eligibility for estimator scaling (IN_SCALING): For example, Black Kyurem
            against itself will not pass the generic AttackerCriteria, but it passes the whitelist AttackerCriteria.
            We don't want Black Kyurem to participate in estimator scaling, so we need a way to prevent it from
            passing the whitelist for these purposes.
            Default to False.
        :return: Whether the attacker meets all criteria
        """
        if not pokemon:
            if not pokemon_codename:
                print(f"Error (AttackerCriteria.check_attacker): Neither Pokemon object nor codename provided.",
                      file=sys.stderr)
                return False
            pokemon = self.metadata.find_pokemon(pokemon_codename)
        fast_not_given = False
        if (self.fast_types or self.pokemon_codenames_and_moves) and not fast:
            if not fast_codename:
                print(f"Warning (AttackerCriteria.check_attacker): Neither fast move object nor codename provided. "
                      f"IGNORING the fast move typing and/or specific Pokemon check.",
                      file=sys.stderr)
                fast_not_given = True
            fast = self.metadata.find_move(fast_codename)
        charged_not_given = False
        if (self.charged_types or self.pokemon_codenames_and_moves) and not charged:
            if not charged_codename:
                print(f"Warning (AttackerCriteria.check_attacker): Neither charged move object nor codename provided. "
                      f"IGNORING the charged move typing and/or specific Pokemon check.",
                      file=sys.stderr)
                charged_not_given = True
            charged = self.metadata.find_move(charged_codename)

        # Check if the given attacker satisfies self.pokemon_codenames_and_moves
        pass_pokemon_moves_check = True
        if self.pokemon_codenames_and_moves is not None:  # Empty list will fail all checks
            if ignore_specific_codenames_and_moves:
                return False
            pass_pokemon_moves_check = False
            if fast and charged:
                for pkm in self.pokemon_codenames_and_moves:
                    if (pkm[0] == pokemon.name and pkm[1] == fast.name and pkm[2] == charged.name
                            and (len(pkm) <= 3 or pkm[3] == iv)):
                        pass_pokemon_moves_check = True
                        break

        return all([
            not self.pokemon_types or criterion_is_types(pokemon, self.pokemon_types),
            not self.fast_types or fast_not_given or fast.type in self.fast_types,
            not self.charged_types or charged_not_given or charged.type in self.charged_types,
            not level or is_level_in_range(level, self.min_level, self.max_level),  # Mostly for Pokebox
            not self.pokemon_codenames or pokemon.name in self.pokemon_codenames,
            pass_pokemon_moves_check,
            criterion_legendary(pokemon, self.is_legendary, self.is_not_legendary),
            criterion_mythical(pokemon, self.is_mythical, self.is_not_mythical),
            criterion_legendary_or_mythical(pokemon, self.is_legendary_or_mythical, self.is_not_legendary_or_mythical),
            criterion_shadow(pokemon, self.is_shadow, self.is_not_shadow),
            criterion_mega(pokemon, self.is_mega, self.is_not_mega),
            not self.exclude_codenames or pokemon.name not in self.exclude_codenames
        ])

    def copy(self):
        """
        Create a deep copy of this AttackerCriteria object.
        :return: Copy of this AttackerCriteria object.
        """
        cp = AttackerCriteria()
        cp.pokemon_types = self.pokemon_types.copy() if self.pokemon_types is not None else None
        cp.fast_types = self.fast_types.copy() if self.fast_types is not None else None
        cp.charged_types = self.charged_types.copy() if self.charged_types is not None else None
        cp.min_level = self.min_level
        cp.max_level = self.max_level
        cp.level_step = self.level_step
        cp.pokemon_codenames = self.pokemon_codenames.copy() if self.pokemon_codenames is not None else None
        cp.pokemon_codenames_and_moves = self.pokemon_codenames_and_moves.copy() if self.pokemon_codenames_and_moves is not None else None
        cp.trainer_id = self.trainer_id
        cp.is_legendary = self.is_legendary
        cp.is_not_legendary = self.is_not_legendary
        cp.is_mythical = self.is_mythical
        cp.is_not_mythical = self.is_not_mythical
        cp.is_legendary_or_mythical = self.is_legendary_or_mythical
        cp.is_not_legendary_or_mythical = self.is_not_legendary_or_mythical
        cp.is_shadow = self.is_shadow
        cp.is_not_shadow = self.is_not_shadow
        cp.is_mega = self.is_mega
        cp.is_not_mega = self.is_not_mega
        cp.metadata = self.metadata
        cp.exclude_codenames = self.exclude_codenames.copy() if self.exclude_codenames is not None else None
        return cp

    def get_required_attackers(self):
        """
        Get the list of required attacker codenames, their levels, IVs and movesets specified in this object,
        specifically the pokemon_codenames_and_moves attribute.
        These attackers are forced to be included in the output CSV. If they're not in the counters lists, they
        should be filled during fill_blanks.
        IV is taken as 15\\15\\15 by default, unless specified in self.pokemon_codenames_and_moves.
        This should only be used if this object is by level, not trainer ID. Thus, levels are generated based on
        the configurations here.

        :return: List of required attacker codenames, their levels, IVs, movesets and whether they participate in
            estimator scaling (None if it's left to the default settings). Format:
            [
                ("URSALUNA", 30, "15\\15\\15", "MUD_SHOT_FAST", "HIGH_HORSEPOWER", None),
                ("URSALUNA", 40, "15\\15\\15", "MUD_SHOT_FAST", "HIGH_HORSEPOWER", None),
                ("URSALUNA", 30, "15\\15\\15", "TACKLE_FAST", "HIGH_HORSEPOWER", None),
                ("URSALUNA", 40, "15\\15\\15", "TACKLE_FAST", "HIGH_HORSEPOWER", None),
                ("GOLURK_SHADOW_FORM", 30, "15\\15\\15", "MUD_SLAP_FAST", "EARTH_POWER", None),
                ("GOLURK_SHADOW_FORM", 40, "15\\15\\15", "MUD_SLAP_FAST", "EARTH_POWER", None),
                ("GARCHOMP_MEGA", 30, "10\\10\\10", "MUD_SHOT_FAST", "EARTH_POWER", None),
                ("GARCHOMP_MEGA", 40, "10\\10\\10", "MUD_SHOT_FAST", "EARTH_POWER", None),
                ("SCIZOR_MEGA", 30, "15\\15\\15", "FURY_CUTTER_FAST", "X_SCISSOR", True),  # Force to participate in scaling
                ("SCIZOR_MEGA", 40, "15\\15\\15", "FURY_CUTTER_FAST", "X_SCISSOR", True),  # Force to participate in scaling
                ...
            ]
        """
        # TODO: Consider adding pokemon_codenames?
        if not self.pokemon_codenames_and_moves:
            return []
        ret = []
        lvl_range = [40]
        if self.trainer_id:
            print(f"Warning (AttackerCriteria.get_required_attackers): "
                  f"Method called on AttackerCriteria based on Trainer IDs. \n"
                  f"Please only use it on criteria by level.\n"
                  f"Using Level 40 as default.",
                  file=sys.stderr)
        else:
            lvl_range = get_levels_in_range(self.min_level, self.max_level, self.level_step)
        for pkm in self.pokemon_codenames_and_moves:
            for lvl in lvl_range:
                ret.append((
                    pkm[0],  # Pokemon codename
                    lvl,
                    pkm[3] if len(pkm) >= 4 else "15\\15\\15",  # IV
                    pkm[1], pkm[2],  # Fast and charged moves
                    pkm[4] if len(pkm) >= 5 else None,  # Scaling participation
                ))
        return ret


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
        :param iv: IV of attacker, as string "15\\15\\15"
        :param fast_codename: Fast move codename
        :param fast: Fast Move object, if codename is not given
        :param charged_codename: Charged move codename
        :param charged: Charged Move object, if codename is not given
        :param ignore_specific_codenames_and_moves: If True, always returns False if this AttackerCriteria includes
            a check for Pokemon codenames and moves. The effect of this is that an attacker can only pass
            AttackerCriteriaMulti via single AttackerCriteria objects that do not focus on a whitelist, but
            on generic criteria (e.g. typing).
            This is used to determine eligibility for estimator scaling (IN_SCALING): For example, Black Kyurem
            against itself will not pass the generic AttackerCriteria, but it passes the whitelist AttackerCriteria.
            We don't want Black Kyurem to participate in estimator scaling, so we need a way to prevent it from
            passing the whitelist for these purposes.
            Default to False.
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
            for lvl in get_levels_in_range(criteria.min_level, criteria.max_level, criteria.level_step)
            if not criteria.trainer_id
        ]))
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
        if any((not criteria.pokemon_types and criteria.pokemon_codenames_and_moves is None) for criteria in self.sets):
            return None
        return list(set([parse_type_str2code(tp)  # Code name
                         for criteria in self.sets if criteria.pokemon_types
                         for tp in criteria.pokemon_types]))
        # Careful to ignore whitelist AttackerCriteria objects

    def pokebattler_trainer_ids(self):
        """
        Return all Pokebattler Trainer IDs that will possibly be needed for simulations.
        Excludes all None values.
        :return: List of Pokebattler trainer IDs in all sets of criteria.
        """
        return list(set([criteria.trainer_id
                         for criteria in self.sets
                         if criteria.trainer_id]))

    def get_subset_no_trainer_ids(self):
        """
        Get a new AttackerCriteriaMulti object that contains all AttackerCriteria without
        trainer IDs, i.e. all criteria with attacker levels.
        :return: AttackerCriteriaMulti object that contains all AttackerCriteria without
        trainer IDs
        """
        return AttackerCriteriaMulti([criteria for criteria in self.sets if not criteria.trainer_id],
                                     metadata=self.metadata)

    def get_subset_trainer_ids(self):
        """
        Get a new AttackerCriteriaMulti object that contains all AttackerCriteria with
        trainer IDs.
        :return: AttackerCriteriaMulti object that contains all AttackerCriteria with
        trainer IDs
        """
        return AttackerCriteriaMulti([criteria for criteria in self.sets if criteria.trainer_id],
                                     metadata=self.metadata)

    def copy(self):
        """
        Create a deep copy of this AttackerCriteriaMulti object.
        Each individual AttackerCriteria will also be copied.
        :return: Copy of this AttackerCriteriaMulti object.
        """
        return AttackerCriteriaMulti([criteria.copy() for criteria in self.sets],
                                     metadata=self.metadata)

    def get_required_attackers(self):
        """
        Get the list of required attacker codenames, their levels, IVs and movesets specified in this object,
        specifically the pokemon_codenames_and_moves attributes of individual AttackerCriteria objects.
        These attackers are forced to be included in the output CSV. If they're not in the counters lists, they
        should be filled during fill_blanks.
        IV is taken as 15/15/15 by default, unless specified in self.pokemon_codenames_and_moves.
        This should only be used if this object is by level, not trainer ID. Thus, levels are generated based on
        the configurations here.

        :return: List of required attacker codenames, their levels, IVs and movesets, Format:
            [
                ("URSALUNA", 30, "15\\15\\15", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
                ("URSALUNA", 40, "15\\15\\15", "MUD_SHOT_FAST", "HIGH_HORSEPOWER"),
                ("URSALUNA", 30, "15\\15\\15", "TACKLE_FAST", "HIGH_HORSEPOWER"),
                ("URSALUNA", 40, "15\\15\\15", "TACKLE_FAST", "HIGH_HORSEPOWER"),
                ("GOLURK_SHADOW_FORM", 30, "15\\15\\15", "MUD_SLAP_FAST", "EARTH_POWER"),
                ("GOLURK_SHADOW_FORM", 40, "15\\15\\15", "MUD_SLAP_FAST", "EARTH_POWER"),
                ("GARCHOMP_MEGA", 30, "10\\10\\10", "MUD_SHOT_FAST", "EARTH_POWER"),
                ("GARCHOMP_MEGA", 40, "10\\10\\10", "MUD_SHOT_FAST", "EARTH_POWER"),
                ...
            ]
        """
        ret = set()
        for criteria in self.sets:
            ret.update(set(criteria.get_required_attackers()))
        return list(ret)
