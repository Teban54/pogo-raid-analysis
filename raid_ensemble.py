"""
This module includes two main types of utilities:
- A class for ensembles of raid bosses.
- Utilities for dealing with ensembles.

An "ensemble" is a collection of Pokemon as raid bosses with associated raid tiers,
and a weight for each raid boss.
Example: (Kyogre, T5, 1), (Giratina-A, T5, 0.5), (Giratina-O, T5, 0.5), (Skarmory, T3, 0.2), ...

In this project, an ensemble is primarily used for evaluting the performance of attackers.
In particular, an attacker's "average estimator" is obtained by finding the estimators
against each boss in the ensemble (with some normalization across all attackers),
then taking a weighted average of these estimators using weights specified by the ensemble.
In the example above, performance against Kyogre would matter twice as much as Giratina-A and
Giratina-O; Skarmory would be the least important boss.
"""
import csv

from utils import *
from params import *
from pokemon import *
from raid_boss import *


class RaidEnsemble:
    """
    Class for an ensemble of raid bosses.
    """
    def __init__(self, raid_bosses=None, pokemons=None, tier=None,
                 weight_multiplier=1,
                 forms_weight_strategy="combine", separate_shadows=True, separate_megas=True,
                 remove_dupes=True):
        """
        Initialize the raid ensemble.

        There are 4 main ways of initialization:
        1. Based on a dict of RaidBoss objects. The dict maps base codenames to RaidBoss objects
           whose Pokemon are different forms of that base (same as the output format of
           group_raid_bosses_by_basename).
           Need: raid_bosses as a dict
        2. Based on a list of RaidBoss objects. They have the Pokemon and raid tier specified.
           Need: raid_bosses as a list
        3. Based on a dict of Pokemon objects, and a standardized tier for all these Pokemon.
           The dict maps base codenames to Pokemon objects which are different forms of that base
           (same as the output format of group_pokemon_by_basename).
           Need: pokemons as a dict, tier
        4. Based on a list of Pokemon objects, and a standardized tier for all these Pokemon.
           Need: pokemons as a list, tier
        The 4 ways are functionally equivalent.

        Unless specified, all Pokemon will have a weight of 1 (except forms, detailed below).
        When the weight_multiplier parameter is specified, a uniform multiplier is applied to
        all Pokemon listed.
        To assign different weights, consider the RaidEnsemble.extend() function:
        first build two different RaidEnsemble objects with different weights, then extend one of them.

        There are two different ways of assigning weights to different forms of the same Pokemon
        (e.g. Giratina, Rotom, Arceus), controlled by the forms_weight_strategy parameter:
        - "combine" (default): All forms of the same base Pokemon will share a weight of 1 equally.
          Each Arceus form has a weight of 1/18, and all Arceus forms have a total weight of 1.
        - "separate": Each form gets a weight of 1 on its own.
          Each Arceus form has a weight of 1, and all Arceus forms have a total weight of 18.
        Understandably, there are "forms" that are functionally different Pokemon: Alolans, Galarians.
        They are specified in FORMS_AS_SEPARATE_POKEMON_UNIVERSAL in params.py: Any forms listed
        there will get a weight of 1 on their own (e.g. Ninetales 1 and Alolan Ninetales 1).

        Note: Allows building an empty RaidEnsemble with raid_bosses=[].

        :param raid_bosses: Dict or list of RaidBoss objects (method 1,2)
        :param pokemons: Dict or list of Pokemon objects (method 3,4)
        :param tier: Raid tier for all Pokemon specified (method 3,4)
        :param weight_multiplier: Weight of each Pokemon
        :param forms_weight_strategy: How weights of Pokemon with several forms should be handled;
            Should be either "combine" or "separate", see above
        :param separate_shadows: If True, each shadow will be considered as a separate base Pokemon,
            instead of as a form of the non-shadow variant.
        :param separate_megas: If True, each mega evolution will be considered as a separate base Pokemon,
            instead of as a form of the non-mega variant.
            This also means Mega X and Mega Y will be treated as different base Pokemon.
        :param remove_dupes: If True, duplicate raids with the same Pokemon and same tier will be removed.
        """
        self.bosses = []  # List of tuples: [(RaidBoss object with Pokemon and tier, Weight)]

        if ((raid_bosses is None or type(raid_bosses) not in [list, dict])
                and (pokemons is None or type(pokemons) not in [list, dict] or not tier)):
            print(f"Error (RaidEnsemble.__init__): Collection of raid bosses or Pokemon and tier not found",
                  file=sys.stderr)
            return
        raid_dict = self.build_raid_dict(
            raid_bosses=raid_bosses, pokemons=pokemons, tier=tier,
            separate_shadows=separate_shadows, separate_megas=separate_megas, remove_dupes=remove_dupes)
        self.bosses = self.convert_raid_dict_to_weighted_list(
            raid_dict, weight_multiplier=weight_multiplier, forms_weight_strategy=forms_weight_strategy)

    def build_raid_dict(self, raid_bosses=None, pokemons=None, tier=None,
                        separate_shadows=True, separate_megas=True, remove_dupes=True):
        """
        Combine all 4 initialization methods and give a single dict mapping
        Pokemon base codenames to RaidBoss objects, such as:
        {'GIRATINA': [<Giratina boss obj>, <Giratina-Origin boss obj>], ...}

        :param raid_bosses: Dict or list of RaidBoss objects (method 1,2)
        :param pokemons: Dict or list of Pokemon objects (method 3,4)
        :param tier: Raid tier for all Pokemon specified (method 3,4)
        :param separate_shadows: If True, each shadow will be considered as a separate base Pokemon,
            instead of as a form of the non-shadow variant.
        :param separate_megas: If True, each mega evolution will be considered as a separate base Pokemon,
            instead of as a form of the non-mega variant.
            This also means Mega X and Mega Y will be treated as different base Pokemon.
        :param remove_dupes: If True, duplicate raids with the same Pokemon and same tier will be removed.
        :return: Dict mapping Pokemon base codenames to RaidBoss objects
        """
        def remove_dupes_in_list(bosses_list):
            """
            Returns a copy of the list that removes duplicate bosses,
            with the same Pokemon name and same tier.
            """
            temp_dict = {}
            for boss in bosses_list:
                temp_dict[(boss.pokemon.name, boss.tier)] = boss
            return list(temp_dict.values())

        raid_boss_dict = None
        if raid_bosses is not None:
            if type(raid_bosses) is dict:
                raid_boss_dict = raid_bosses
            else:
                raid_boss_dict = group_raid_bosses_by_basename(
                    raid_bosses, separate_shadows=separate_shadows, separate_megas=separate_megas)
        else:
            if type(pokemons) is list:
                pokemons = group_pokemon_by_basename(
                    pokemons, separate_shadows=separate_shadows, separate_megas=separate_megas)
            raid_boss_dict = {
                base: [RaidBoss(pokemon_obj=pkm, tier_codename=tier) for pkm in mons]
                for base, mons in pokemons.items()
            }

        if remove_dupes:
            # Check within each bin
            for base in raid_boss_dict.keys():
                raid_boss_dict[base] = remove_dupes_in_list(raid_boss_dict[base])
        return raid_boss_dict

    def convert_raid_dict_to_weighted_list(self, raid_dict, weight_multiplier=1,
                 forms_weight_strategy="combine"):
        """
        Assign weights to raids: Given a completed dict mapping Pokemon base codenames
        to RaidBoss objects, convert it to a list of tuples with both the RaidBoss and
        its weight.
        :param raid_dict: Dict mapping Pokemon base codenames to RaidBoss objects
        :param weight_multiplier: Weight of each Pokemon
        :param forms_weight_strategy: How weights of Pokemon with several forms should be handled;
            Should be either "combine" or "separate", see above
        """
        def assign_weight_to_forms(bosses_list):
            """
            Given a list from a single dict value, which is a list of RaidBoss objects
            with the same base codename, return a list of tuples with these RaidBoss
            objects and their weight.
            """
            # First, filter out forms that should be separate Pokemon (Alola etc)
            bosses_list_separate_forms = []  # Alola, Galarian
            bosses_list_true_forms = []  # Origin, Therian etc
            for boss in bosses_list:
                base = boss.pokemon.base_codename
                form = boss.pokemon.form_codename if boss.pokemon.form_codename is not None else ''
                if (form in FORMS_AS_SEPARATE_POKEMON_UNIVERSAL
                        or form in FORMS_AS_SEPARATE_POKEMON_PER_POKEMON.get(base, [])):
                    bosses_list_separate_forms.append(boss)
                else:
                    bosses_list_true_forms.append(boss)

            ret = [(boss, weight_multiplier * 1.0) for boss in bosses_list_separate_forms]
            if len(bosses_list_true_forms) == 0:  # Avoid /0
                return ret
            if "combine" in forms_weight_strategy.lower():
                ret.extend((boss, weight_multiplier / len(bosses_list_true_forms))
                           for boss in bosses_list_true_forms)
            else:  # if forms_weight_strategy == "separate":
                ret.extend((boss, weight_multiplier * 1.0)
                           for boss in bosses_list_true_forms)
            return ret

        raid_list = []
        for base, bosses in raid_dict.items():
            raid_list.extend(assign_weight_to_forms(bosses))
        return raid_list

    def extend(self, ensemble2):
        """
        Add all tuples in another ensemble to this RaidEnsemble object. Modifies current object.
        :param ensemble2: RaidEnsemble whose content is to be added
        """
        self.bosses.extend(ensemble2.bosses)

    def apply_multiplier(self, multiplier):
        """
        Apply a multiplier to all raid weights in this ensemble.
        :param multiplier: Multiplier
        """
        self.bosses = [(boss, weight * multiplier) for boss, weight in self.bosses]

    def get_weight_sum(self):
        """
        Get the sum of all weights in this ensemble.
        """
        return sum(weight for boss, weight in self.bosses)

    def normalize_weights(self):
        """
        Normalize weights of all raids in this ensemble, so that they sum to 1.
        """
        if len(self.bosses) == 0:
            return
        self.apply_multiplier(1.0 / self.get_weight_sum())

    def get_raids_list(self):
        """
        Get a list of raid bosses included in this ensemble.
        :return: List of RaidBoss objects
        """
        return [raid for raid, weight in self.bosses]

    def get_pokemon_list(self):
        """
        Get a list of Pokemon included in this ensemble.
        :return: List of Pokemon objects
        """
        return [raid.pokemon for raid, weight in self.bosses]

    def debug_print_to_csv(self, filename="data/debug/ensemble.csv"):
        """
        Debug function that outputs the current ensemble to CSV.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Tier', 'Pokemon', 'Weight']
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for boss, weight in self.bosses:
                writer.writerow([
                    parse_raid_tier_code2str(boss.tier),
                    boss.pokemon.displayname,
                    weight
                ])


def filter_ensemble_by_criteria(ensemble, criterion_raid=None, criterion_pokemon=None, **kwargs):
    """
    Filter a RaidEnsemble with a given criterion function for raids,
    and optionally, a criterion function for Pokemon.
    Returns a NEW RaidEnsemble object with all raid bosses that evaluate to True
    on both criterion functions, with their original weights.
    See also: filter_pokemon_by_criteria, filter_raids_by_criteria

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
        result = filter_ensemble_by_criteria(
            ensemble, criterion=is_higher_than_level, criterion_pokemon=is_form,
            level_ceiling=3, form='WINTER_2020')

    :param ensemble: RaidEnsemble object to be filtered
    :param criterion_raid: A criterion function for raids as described above
    :param criterion_pokemon: A criterion function for Pokemon as described above
    :return: New RaidEnsemble object whose raids evaluate to True on both criterion
    """
    new_list = [(raid, weight) for raid, weight in ensemble.bosses
                if (criterion_raid is None or criterion_raid(raid, **kwargs))
                and (criterion_pokemon is None or criterion_pokemon(raid.pokemon, **kwargs))]
    new_ens = RaidEnsemble([])
    new_ens.bosses = new_list
    return new_ens
