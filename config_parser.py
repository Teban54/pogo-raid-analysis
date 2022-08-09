"""
Module for the Config object, which describes the configuration of a particular run.
"""

from params import *
from utils import *
from pokemon import *
from raid_boss import *
from move import *
from config import *
from attacker_criteria import *
from raid_ensemble import *
from battle_settings import *


class Config:
    """
    Class for a configuration of a particular run.
    """
    def __init__(self, metadata, config_attacker_criteria=None,
                 config_raid_ensemble=None, config_battle_settings=None,
                 config_sort_option=None, config_scaling_settings=None, config_processing_settings=None):
        """
        Initialize the configuration.

        There are 3 major components of a config:
        - Attacker criteria: Sets of criteria for attackers, such as types, min/max levels, etc.
        - Raid boss ensemble: List of bosses and their weights.
        - Battle settings: Weather, friendship, etc.
        Additionally, there are 3 minor components:
        - Sorting option
        - Estimator scaling settings: Enabled, baseline timing, baseline boss moveset.
        - Processing settings: How data should be processed (e.g. which attackers/bosses to keep),
            and what details to be included in the CSV

        This constructor takes in config.py settings for each of the 3 components,
        then construct the corresponding objects (AttackerCriteriaMulti, RaidEnsemble, BattleSettings).

        :param metadata: Current Metadata object
        :param config_attacker_criteria: Config for attacker criteria from config.py
        :param config_raid_ensemble: Config for raid ensemble from config.py
        :param config_battle_settings: Config for battle settings from config.py
        :param config_sort_option: Config for sorting option from config.py
        :param config_scaling_settings: Config for estimator scaling settings from config.py
        :param config_processing_settings: Config for data processing and CSV writing settings from config.py
        """
        self.meta = metadata
        self.attacker_criteria_multi = None
        self.raid_ensemble = None
        self.battle_settings = None
        self.sort_option = config_sort_option
        self.scaling_settings = None  # Dict, filled in later
        self.processing_settings = None  # Dict, filled in later

        if config_attacker_criteria:
            self.attacker_criteria_multi = self.parse_attacker_criteria_config(config_attacker_criteria)
        # Parse battle and scaling settings first, so that it can be used as default for raid ensemble
        self.battle_settings = self.parse_battle_settings_config(
            config_battle_settings if config_battle_settings
            else {}  # No battle settings specified, use default values
        )
        self.scaling_settings = self.format_scaling_settings_config(config_scaling_settings)
        self.processing_settings = self.format_processing_settings_config(config_processing_settings)

        if config_raid_ensemble:
            self.raid_ensemble = self.parse_raid_ensemble_config(config_raid_ensemble)

    def parse_attacker_criteria_config(self, config):
        """
        Construct an AttackerCriteriaMulti object from the configuration lists/dicts in config.py.

        :param config: List (or occasionally dict) describing attacker criteria configs
                (Typically from config.py)
        :return: AttackerCriteriaMulti object
        """
        if type(config) is dict:
            config = [config]
        # config is a list of dicts, and each dict represents a set of criteria

        sets = []  # Each element is a single AttackerCriteria object
        for cfg in config:
            sets.append(AttackerCriteria(
                metadata=self.meta,
                pokemon_types=cfg.get("Pokemon types", None),
                fast_types=cfg.get("Fast move types", None),
                charged_types=cfg.get("Charged move types", None),
                min_level=cfg.get("Min level", MIN_LEVEL_DEFAULT),
                max_level=cfg.get("Max level", MAX_LEVEL_DEFAULT),
                level_step=cfg.get("Level step size", LEVEL_STEP_DEFAULT),
                pokemon_codenames=cfg.get("Pokemon code names", None),
                trainer_id=cfg.get("Trainer ID", None),
                is_legendary=cfg.get("Must be legendary", False),
                is_not_legendary=cfg.get("Must be non legendary", cfg.get("Must be non-legendary", False)),
                is_mythical=cfg.get("Must be mythical", False),
                is_not_mythical=cfg.get("Must be non mythical", cfg.get("Must be non-mythical", False)),
                is_legendary_or_mythical=cfg.get("Must be legendary or mythical", False),
                is_not_legendary_or_mythical=cfg.get(
                    "Must be non legendary or mythical", cfg.get("Must be non-legendary or mythical", False)),
                is_shadow=cfg.get("Must be shadow", False),
                is_not_shadow=cfg.get("Must be non shadow", cfg.get("Must be non-shadow", False)),
                is_mega=cfg.get("Must be mega", False),
                is_not_mega=cfg.get("Must be non mega", cfg.get("Must be non-mega", False)),
                exclude_codenames=cfg.get("Exclude", None),
            ))
        return AttackerCriteriaMulti(sets, metadata=self.meta)

    def parse_raid_ensemble_config(self, config):
        """
        Construct a RaidEnsemble object from the configuration lists/dicts in config.py.
        Note: Uses self.battle_settings as default battle settings.

        :param config: List (or occasionally dict) describing raid ensemble configs
                (Typically from config.py)
        :return: RaidEnsemble object
        """
        def build_raids_list(cfg):
            """
            Parse the Pokemon pool and build the list or RaidBoss objects.
            :param cfg: Individual config dict for one single group of raid bosses
            :return: List of RaidBoss objects
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

            # Note: Config now supports specifying several raid tiers or categories at once.
            # If the Pokemon pool is determined by raid tier or category, pre-made RaidBoss objects
            # will be used (those were created when initializing the metadata).
            # If the Pokemon pool is all Pokemon (possibly except those used above), the list of
            # Pokemon will be pulled first, and then a RaidBoss object is created for each combination
            # of Pokemon and tier. (e.g. T1 Ferroseed, T3 Ferroseed, T1 Chansey, T3 Chansey, etc)
            raids = None
            pokemon = None
            tier = None
            if pool == "by raid tier" or pool == "by tier":
                tiers = []
                if 'Raid tier' not in cfg and 'Raid tiers' not in cfg:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"'Raid tier' or 'Raid tiers' do not exist in raid ensemble config.\n"
                          f"Using T3 as default.",
                          file=sys.stderr)
                    tiers.append("Tier 3")
                else:
                    if 'Raid tier' in cfg:
                        tiers.append(cfg['Raid tier'])
                    if 'Raid tiers' in cfg:
                        tiers += cfg['Raid tiers']
                #tier = cfg.get('Raid tier', "Tier 3")
                raids = self.meta.get_raid_bosses_by_tiers(tiers, remove_ignored=True)  # pre-built from metadata
                return raids
            elif pool == "by raid category" or pool == "by category":
                categories = []
                if 'Raid category' not in cfg and 'Raid categories' not in cfg:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"'Raid category' or 'Raid categories' does not exist in raid ensemble config.\n"
                          f"Using T3 as default.",
                          file=sys.stderr)
                    categories.append("Tier 3")
                else:
                    if 'Raid category' in cfg:
                        categories.append(cfg['Raid category'])
                    if 'Raid categories' in cfg:
                        categories += cfg['Raid categories']
                #category = cfg.get('Raid category', "Tier 3")
                raids = self.meta.get_raid_bosses_by_categories(categories, remove_ignored=True)  # pre-built from metadata
                return raids
            elif pool == "all pokemon" or pool == "all pokemon except above":
                tiers = []
                if 'Raid tier' not in cfg and 'Raid tiers' not in cfg:
                    print(f"Error (Config.parse_raid_ensemble_config): "
                          f"'Raid tier' or 'Raid tiers' does not exist in raid ensemble config.\n"
                          f"(Even if your Pokemon pool is all Pokemon, you still need to specify (a) raid tier(s) for all of them.)\n"
                          f"Using T3 as default.",
                          file=sys.stderr)
                    tiers.append("Tier 3")
                else:
                    if 'Raid tier' in cfg:
                        tiers.append(cfg['Raid tier'])
                    if 'Raid tiers' in cfg:
                        tiers += cfg['Raid tiers']
                #tier = cfg.get('Raid tier', "Tier 3")
                pokemon = self.meta.get_all_pokemon(remove_ignored=True)
                if pool == "all pokemon except above":
                    pokemon = subtract_from_pokemon_list(pokemon, pokemon_used)
                tiers = [parse_raid_tier_str2code(tier) for tier in tiers]
                return pokemon_list_to_raid_boss_list(pokemon, tiers)

            # if raids is not None:
            #     return raids
            # return pokemon_list_to_raid_boss_list(pokemon, tier)

        def apply_filter(raids_list, filter_key, filter_val):
            """
            Parse one filter from config and apply it to the current list of raid bosses.
            :param raids: Current list of RaidBoss objects
            :param filter_key: Filter key listed in config
            :param filter_val: Filter value listed in config
            :return: New, filtered list of RaidBoss objects
            """
            filter_key = filter_key.lower()
            if filter_key == "weak to contender types":
                return filter_raids_by_criteria(raids_list, criterion_pokemon=criterion_weak_to_contender_types,
                                                attack_types=filter_val)
            if filter_key == "weak to contender types simultaneously":
                return filter_raids_by_criteria(raids_list, criterion_pokemon=criterion_weak_to_contender_types_simult,
                                                attack_types=filter_val)
            if filter_key == "evolution stage":
                return filter_raids_by_criteria(raids_list, criterion_pokemon=criterion_evo_stage,
                                                keep_final_stage=(filter_val.lower() == 'final'),
                                                keep_pre_evo=('pre' in filter_val.lower()))
            if filter_key in ["must be shadow", "must be non shadow", "must be non-shadow"]:
                return filter_raids_by_criteria(raids_list,
                    criterion_pokemon=criterion_shadow,
                    is_shadow=(filter_key == "must be shadow" and filter_val),
                    is_not_shadow=(filter_key in ["must be non shadow", "must be non-shadow"] and filter_val)
                )
            if filter_key in ["must be mega", "must be non mega", "must be non-mega"]:
                return filter_raids_by_criteria(raids_list,
                    criterion_pokemon=criterion_mega,
                    is_mega=(filter_key == "must be mega" and filter_val),
                    is_not_mega=(filter_key in ["must be non mega", "must be non-mega"] and filter_val)
                )
            if filter_key in ["must be legendary", "must be non legendary", "must be non-legendary"]:
                return filter_raids_by_criteria(raids_list,
                    criterion_pokemon=criterion_legendary,
                    is_legendary=(filter_key == "must be legendary" and filter_val),
                    is_not_legendary=(filter_key in ["must be non legendary", "must be non-legendary"] and filter_val)
                )
            if filter_key in ["must be mythical", "must be non mythical", "must be non-mythical"]:
                return filter_raids_by_criteria(raids_list,
                    criterion_pokemon=criterion_mythical,
                    is_mythical=(filter_key == "must be mythical" and filter_val),
                    is_not_mythical=(filter_key in ["must be non mythical", "must be non-mythical"] and filter_val)
                )
            if filter_key in ["must be legendary or mythical", "must be non legendary or mythical",
                              "must be non-legendary or mythical"]:
                return filter_raids_by_criteria(raids_list,
                    criterion_pokemon=criterion_legendary_or_mythical,
                    is_legendary_or_mythical=(filter_key == "must be legendary or mythical" and filter_val),
                    is_not_legendary_or_mythical=(filter_key in [
                        "must be non legendary or mythical", "must be non-legendary or mythical"] and filter_val)
                )
            print(f"Error (Config.parse_raid_ensemble_config): "
                  f"Filter criteria {filter_key} does not match one of expected values.",
                  file=sys.stderr)
            return raids_list

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
            raids = build_raids_list(cfg)
            weight = cfg.get("Weight of each Pokemon", 1)
            weight_group = cfg.get("Weight of whole group", -1)
            forms_weight_strategy = cfg.get("Forms weight strategy", 1)

            # Apply filter first before building RaidEnsemble,
            # So that weights are only assigned to Pokemon that remain after filters
            for fkey, fval in cfg.get('Filters', {}).items():
                raids = apply_filter(raids, fkey, fval)

            # Parse group-specific battle settings if given
            # settings = (self.parse_battle_settings_config(cfg["Battle settings"])
            #             if "Battle settings" in cfg
            #             else self.battle_settings)
            settings = self.battle_settings
            if "Battle settings" in cfg:
                settings = settings.copy()
                settings.override_with_dict(cfg["Battle settings"])

            # Parse group-specific baseline battle settings (for estimator scaling)
            baseline_bs = (
                self.scaling_settings["Baseline battle settings"]
                if self.scaling_settings and "Baseline battle settings" in self.scaling_settings
                else settings  # Default: Battle settings for this RaidBoss
            )
            if "Baseline battle settings" in cfg:
                baseline_bs = baseline_bs.copy()
                baseline_bs.override_with_dict(cfg["Baseline battle settings"])

            ens = RaidEnsemble(raid_bosses=raids,
                               weight_multiplier=weight, forms_weight_strategy=forms_weight_strategy,
                               battle_settings=settings, baseline_battle_settings=baseline_bs)

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

    def parse_battle_settings_config(self, config):
        """
        Construct a BattleSettings object from the configuration dict in config.py.
        :param config: Dict describing battle settings config
                (Typically from config.py)
        :return: BattleSettings object
        """
        weather_str = config.get("Weather", "Extreme")
        friendship_str = config.get("Friendship", "Best")
        attack_strategy_str = config.get("Attack strategy", "No Dodging")
        dodge_strategy_str = config.get("Dodge strategy", "Realistic Dodging")
        return BattleSettings(weather_str=weather_str, friendship_str=friendship_str,
                              attack_strategy_str=attack_strategy_str,dodge_strategy_str=dodge_strategy_str)

    def format_scaling_settings_config(self, config):
        """
        Format the dict of scaling options from config.py.
        :param config: Dict describing scaling settings config
                (Typically from config.py)
        :return: Dict with properly formatted values (default values added in).
                Note that baseline battle settings (if specified) is parsed into a BattleSettings object.
        """
        cfg = config.copy()
        if "Enabled" not in cfg:
            cfg["Enabled"] = True
        if "Baseline chosen before filter" not in cfg:
            cfg["Baseline chosen before filter"] = False
        if "Baseline boss moveset" not in cfg:
            cfg["Baseline boss moveset"] = "random"
        elif cfg["Baseline boss moveset"].lower() not in ["random", "easiest", "hardest"]:
            print(f"Error (Config.format_scaling_settings_config): Boss moveset option {cfg['Baseline boss moveset']} "
                  f"for estimator scaling is invalid. Using 'random' as default.",
                  file=sys.stderr)
            cfg["Baseline boss moveset"] = "random"
        cfg["Baseline boss moveset"] = cfg["Baseline boss moveset"].lower()
        if "Baseline attacker level" not in cfg or cfg["Baseline attacker level"] == -1:
            cfg["Baseline attacker level"] = "by level"
        if type(cfg["Baseline attacker level"]) is str:
            cfg["Baseline attacker level"] = cfg["Baseline attacker level"].lower()

        if "Baseline battle settings" in cfg:
            cfg["Baseline battle settings"] = self.parse_battle_settings_config(cfg["Baseline battle settings"])
        return cfg

    def format_processing_settings_config(self, config):
        """
        Format the dict of processing options from config.py.
        :param config: Dict describing processing settings config
                (Typically from config.py)
        :return: Dict with properly formatted values (default values added in)
        """
        cfg = config.copy()
        # TODO: List settings not parsed yet

        # CSV Table settings
        if "Include unscaled estimators" not in cfg:
            cfg["Include unscaled estimators"] = False
        if "Combine attacker movesets" not in cfg:
            cfg["Combine attacker movesets"] = True
        if "Include random boss movesets" not in cfg:
            cfg["Include random boss movesets"] = True
        if "Include specific boss movesets" not in cfg:
            cfg["Include specific boss movesets"] = False
        if "Include attacker IVs" not in cfg:
            cfg["Include attacker IVs"] = False
        if "Attackers that should not be combined" not in cfg:
            cfg["Attackers that should not be combined"] = []
        return cfg
