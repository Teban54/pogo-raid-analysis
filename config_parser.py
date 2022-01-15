"""
Module for the Config object, which describes the configuration of a particular run.
"""

from params import *
from utils import *
from pokemon import *
from raid_boss import *
from move import *
from raid_ensemble import *
from config import *


class Config:
    """
    Class for a configuration of a particular run.
    """
    def __init__(self, metadata, config_attack_ensemble=None, config_raid_ensemble=None, config_battle_settings=None):
        """
        Initialize the configuration.

        There are 3 main components of a config:
        - Attacker ensemble: List or type of attackers, and their min/max levels. (TBC)
        - Raid boss ensemble: List of bosses and their weights.
        - Battle settings: Weather, friendship, etc.

        This constructor takes in config.py settings for each of the 3 components,
        then construct the corresponding objects (AttackEnsemble, RaidEnsemble, BattleSettings).

        :param metadata: Current Metadata object
        :param config_attack_ensemble: Config for attacker ensemble from config.py
        :param config_raid_ensemble: Config for raid ensemble from config.py
        :param config_battle_settings: Config for battle settings from config.py
        """
        self.meta = metadata
        self.attack_ensemble = None
        self.raid_ensemble = None
        self.battle_settings = None

        if config_attack_ensemble:
            # TODO
            pass
        if config_raid_ensemble:
            self.raid_ensemble = self.parse_raid_ensemble_config(config_raid_ensemble)
        if config_battle_settings:
            # TODO
            pass

    def parse_raid_ensemble_config(self, config):
        """
        Construct a RaidEnsemble object from the configuration lists/dicts in config.py.
        :param config: List (or occasionally dict) describing raid ensemble configs
                (Typically from config.py)
        :return: RaidEnsemble object
        """
        def parse_pokemon_pool(cfg):
            """
            Parse the Pokemon pool.
            :param cfg: Individual config dict for one single group of raid bosses
            :return: Tuple of len 3: (list of RaidBoss'es, list of Pokemon, raid tier), whichever applicable
            """
            if 'Pokemon pool' not in cfg:
                print(f"Error (Config.parse_raid_ensemble_config): "
                      f"'Pokemon pool' does not exist in raid ensemble config. Using All Pokemon as default.",
                      file=sys.stderr)
            pool = cfg.get('Pokemon pool', 'All Pokemon').lower()
            if pool not in ["all pokemon", "all pokemon except above",
                            "by raid tier", "by tier",
                            "by raid category", "by category"]:
                print(f"Error (Config.parse_raid_ensemble_config): "
                      f"Pokemon pool {cfg.get('Pokemon pool', 'All Pokemon')} does not match one of expected values. "
                      f"Using All Pokemon as default.",
                      file=sys.stderr)
                pool = "all pokemon"

            raids = None
            pokemon = None
            tier = None
            if pool == "by raid tier" or pool == "by tier":
                if 'Raid tier' not in cfg:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"'Raid tier' does not exist in raid ensemble config.\n"
                          f"Using T3 as default.",
                          file=sys.stderr)
                tier = cfg.get('Raid tier', "Tier 3")
                raids = self.meta.get_raid_bosses_by_tier(tier, remove_ignored=True)
            elif pool == "by raid category" or pool == "by category":
                if 'Raid category' not in cfg:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"'Raid category' does not exist in raid ensemble config.\n"
                          f"Using T3 as default.",
                          file=sys.stderr)
                category = cfg.get('Raid category', "Tier 3")
                raids = self.meta.get_raid_bosses_by_category(category, remove_ignored=True)
            elif pool == "all pokemon" or pool == "all pokemon except above":
                if 'Raid tier' not in cfg:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"'Raid tier' does not exist in raid ensemble config.\n"
                          f"(Even if your Pokemon pool is all Pokemon, you still need to specify a raid tier for all of them.)\n"
                          f"Using T3 as default.",
                          file=sys.stderr)
                tier = cfg.get('Raid tier', "Tier 3")
                pokemon = self.meta.get_all_pokemon(remove_ignored=True)
                if pool == "all pokemon except above":
                    pokemon = subtract_from_pokemon_list(pokemon, pokemon_used)
            return raids, pokemon, tier

        def apply_filter(ens, filter_key, filter_val):
            """
            Parse one filter from config and applyit to the current ensemble.
            :param ens: Current RaidEnsemble object
            :param filter_key: Filter key listed in config
            :param filter_val: Filter value listed in config
            :return: New, filtered RaidEnsemble object
            """
            filter_key = filter_key.lower()
            if filter_key == "weak to contender types":
                return filter_ensemble_by_criteria(ens, criterion_pokemon=criterion_weak_to_contender_types,
                                                   attack_types=filter_val)
            if filter_key == "evolution stage":
                return filter_ensemble_by_criteria(ens, criterion_pokemon=criterion_evo_stage,
                                                   keep_final_stage=(filter_val.lower() == 'final'),
                                                   keep_pre_evo=('pre' in filter_val.lower()))
            if filter_key == "is shadow" or filter_key == "is not shadow":
                return filter_ensemble_by_criteria(ens,
                    criterion_pokemon=criterion_shadow,
                    is_shadow=(filter_key == "is shadow" and filter_val),
                    is_not_shadow=(filter_key == "is not shadow" and filter_val)
                )
            if filter_key == "is mega" or filter_key == "is not mega":
                return filter_ensemble_by_criteria(ens,
                    criterion_pokemon=criterion_mega,
                    is_mega=(filter_key == "is mega" and filter_val),
                    is_not_mega=(filter_key == "is not mega" and filter_val)
                )
            if filter_key == "is legendary" or filter_key == "is not legendary":
                return filter_ensemble_by_criteria(ens,
                    criterion_pokemon=criterion_legendary,
                    is_legendary=(filter_key == "is legendary" and filter_val),
                    is_not_legendary=(filter_key == "is not legendary" and filter_val)
                )
            if filter_key == "is mythical" or filter_key == "is not mythical":
                return filter_ensemble_by_criteria(ens,
                    criterion_pokemon=criterion_mythical,
                    is_mythical=(filter_key == "is mythical" and filter_val),
                    is_not_mythical=(filter_key == "is not mythical" and filter_val)
                )
            if filter_key == "is legendary or mythical" or filter_key == "is not legendary or mythical":
                return filter_ensemble_by_criteria(ens,
                    criterion_pokemon=criterion_legendary_or_mythical,
                    is_legendary_or_mythical=(filter_key == "is legendary or mythical" and filter_val),
                    is_not_legendary_or_mythical=(filter_key == "is not legendary or mythical" and filter_val)
                )
            print(f"Error (Config.parse_raid_ensemble_config): "
                  f"Filter criteria {filter_key} does not match one of expected values.",
                  file=sys.stderr)
            return ens

        def combine_ensembles(ens_list):
            """
            Combine a list of RaidEnsemble objects into a single RaidEnsemble object,
            keeping their original weights.
            :param ens_list: List of RaidEnsemble objects
            :return: Combined RaidEnsemble object
            """
            ensemble = RaidEnsemble(raid_bosses=[])
            for e in ens_list:
                ensemble.extend(e)
            return ensemble

        if type(config) is dict:
            config = [config]
        # config is a list of dicts, and each dict represents a group of raid bosses

        ensembles = []  # (RaidEnsemble, total weight needed) for each dict, will combine them later
        pokemon_used = set()  # All Pokemon that currently exist in any group (for "All Pokemon except above")
        for cfg in config:
            raids, pokemon, tier = parse_pokemon_pool(cfg)
            weight = cfg.get("Weight of each Pokemon", 1)
            weight_group = cfg.get("Weight of whole group", -1)
            forms_weight_strategy = cfg.get("Forms weight strategy", 1)

            ens = RaidEnsemble(raid_bosses=raids, pokemons=pokemon, tier=tier,
                               weight_multiplier=weight, forms_weight_strategy=forms_weight_strategy)
            for filter_key, filter_val in cfg.get('Filters', {}).items():
                ens = apply_filter(ens, filter_key, filter_val)

            if weight_group >= 0:
                cur_weight = ens.get_weight_sum()
                if cur_weight == 0:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"One of the groups of raid bosses has total weight of 0.",
                          file=sys.stderr)
                else:
                    ens.apply_multiplier(weight_group / cur_weight)

            if ens.get_weight_sum() == 0:
                print(f"Warning (Config.parse_raid_ensemble_config): "
                      f"One of the groups of raid bosses has total weight of 0 (after possible reweighing by group).\n"
                      f"Here's the config for the group: {cfg}",
                      file=sys.stderr)
            ensembles.append(ens)
            pokemon_used.update(ens.get_pokemon_list())
        return combine_ensembles(ensembles)
