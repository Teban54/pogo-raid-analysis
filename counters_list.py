"""
This module includes all classes for list(s) of raid counters against bosses,
at varying level of details.
Each time an instance of these classes is created, it pulls JSON data from Pokebattler
to generate the counters list immediately.

Currently, it includes classes for the following:
- A single list of counters against a particular boss, under a particular set of battle settings.
- Lists of counters for multiple attacker levels, with a particular boss and battle settings
  (aside from attacker level).
- Lists of counters against an ensemble of raid bosses, with multiple attacker levels for each boss,
  and with a particular set of battle settings.

This module also includes utilities for dealing with single or multiple counters lists.
"""
import csv
import copy

from utils import *
from params import *
from raid_boss import *
from attacker_criteria import *
from get_json import *


class CountersListSingle:
    """
    Class for a single counters list, against a particular raid boss and
    under a particular set of battle settings.
    """
    def __init__(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5",
                 metadata=None, attacker_level=40, trainer_id=None,
                 attacker_criteria_multi=None, battle_settings=None, sort_option="Estimator"):
        """
        Initialize the attributes and get the JSON rankings.
        :param raid_boss: RaidBoss object
        :param raid_boss_pokemon: Pokemon object for the raid boss, if raid_boss is not provided.
        :param raid_boss_codename: Code name of the raid boss (e.g. "LANDORUS_THERIAN_FORM"),
                if raid_boss is not provided.
        :param raid_tier: Raid tier, either as natural language or code name,
                if raid_boss is not provided.
        :param metadata: Current Metadata object
        :param attacker_level: Attacker level
        :param int trainer_id: Pokebattler Trainer ID if a trainer's own Pokebox is used.
                If None, use all attackers by level.
        :param attacker_criteria_multi: AttackerCriteriaMulti object describing attackers to be used
        :param battle_settings: BattleSettings object
        :param sort_option: Sorting option, as shown on Pokebattler (natural language or code name)
        """
        self.boss = None
        self.attacker_criteria_multi = None
        self.battle_settings = None
        self.attacker_level = attacker_level
        self.trainer_id = trainer_id
        self.sort_option = parse_sort_option_str2code(sort_option)
        self.JSON = None
        self.metadata = metadata

        # Ranking dicts: Mapping (fast move codename, charged move codename) pairs to lists
        # For list format, see documentation for parse_JSON
        self.rankings_raw = {}  # Before filtering by attackers
        self.rankings = {}  # After filtering by attackers
        self.scaling_baseline = 1  # For recovering originals

        self.init_raid_boss(raid_boss, raid_boss_pokemon, raid_boss_codename, raid_tier)
        self.init_attacker_criteria(attacker_criteria_multi)
        self.init_battle_settings(battle_settings)
        #self.load_JSON()
        #self.parse_JSON()

    def init_raid_boss(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5"):
        """
        Finds the RaidBoss object from codename, if necessary.
        This populates the following fields: boss.
        """
        if raid_boss:
            self.boss = raid_boss
            return
        if not raid_boss_pokemon and not raid_boss_codename:
            print(f"Error (CountersListSingle.__init__): Raid boss, Pokemon or code name not found", file=sys.stderr)
            return
        if not raid_tier:
            print(f"Error (CountersListSingle.__init__): Raid boss or tier not found", file=sys.stderr)
            return
        raid_tier = parse_raid_tier_str2code(raid_tier)
        self.boss = RaidBoss(pokemon_obj=raid_boss_pokemon, pokemon_codename=raid_boss_codename,
                             tier_codename=raid_tier, metadata=self.metadata)

    def init_attacker_criteria(self, attacker_criteria_multi=None):
        """
        Loads the AttackerCriteriaMulti object and handles exceptions.
        This populates the following fields: attacker_criteria_multi.
        """
        if not attacker_criteria_multi:
            print(f"Warning (CountersListSingle.__init__): AttackerCriteriaMulti not found. Using default criteria.",
                  file=sys.stderr)
            attacker_criteria_multi = AttackerCriteriaMulti(sets=[AttackerCriteria(metadata=self.metadata)],
                                                            metadata=self.metadata)
        if type(attacker_criteria_multi) is AttackerCriteria:
            print(f"Warning (CountersListSingle.__init__): Only a singular AttackerCriteria passed in, "
                  f"expected AttackerCriteriaMulti. Packaging it into multi criteria.",
                  file=sys.stderr)
            attacker_criteria_multi = AttackerCriteriaMulti(sets=[attacker_criteria_multi],
                                                            metadata=self.metadata)
        self.attacker_criteria_multi = attacker_criteria_multi

    def init_battle_settings(self, battle_settings=None):
        """
        Loads the BattleSettings object and handles exceptions.
        This populates the following fields: bottle_settings.
        """
        if not battle_settings:
            print(f"Warning (CountersListSingle.__init__): BattleSettings not found. Using default settings.",
                  file=sys.stderr)
            battle_settings = BattleSettings()
        if battle_settings.is_multiple():
            print(f"Warning (CountersListSingle.__init__): BattleSettings includes multiple settings "
                  f"(this class requires a single setting). Using the first set.",
                  file=sys.stderr)
            battle_settings = battle_settings.indiv_settings[0]
        self.battle_settings = battle_settings

    def load_JSON(self):
        """
        Pull the Pokebattler JSON and store it in the object.
        """
        if self.trainer_id:
            print(f"Loading: {parse_raid_tier_code2str(self.boss.tier)} {self.boss.pokemon_codename}, "
                  f"Trainer ID {self.trainer_id}, {self.battle_settings}")
        else:
            print(f"Loading: {parse_raid_tier_code2str(self.boss.tier)} {self.boss.pokemon_codename}, "
                  f"Level {self.attacker_level}, {self.battle_settings}")
        self.JSON = get_pokebattler_raid_counters(
            raid_boss=self.boss,
            attacker_level=self.attacker_level,
            trainer_id=self.trainer_id,
            attacker_criteria_multi=self.attacker_criteria_multi,
            battle_settings=self.battle_settings,
            sort_option=self.sort_option
        )

    def parse_JSON(self):
        """
        Process the Pokebattler JSON, including:
        - Splitting counters lists by boss movesets (random and specific)
        - Only keeping relevant data for each counter
        - Put the counters into correct order (JSON has them reversed)

        After this, both self.rankings_raw and self.rankings will be in the following format.
        self.rankings will be a copy of self.rankings_raw (different dict objects).
        {
            ('RANDOM', 'RANDOM'): [  # Listed from best to worst (in theory)
                {
                    "POKEMON_CODENAME": "MAGNETON_SHADOW_FORM",
                    "LEVEL": "40",  # String because .5
                    "IV": "15/15/15",
                    "ESTIMATOR": 2.9663813,  # Best moveset; keys match sort_options code names
                    # If estimator has been scaled, an "ESTIMATOR_UNSCALED" key will appear here
                    "TIME": 778.319,  # Converted from milliseconds to seconds
                    "DEATHS": 55.08158337255771,
                    "BY_MOVE": {  # Listed from best to worst (in theory)
                        ('SPARK_FAST', 'FRUSTRATION'): {
                            "ESTIMATOR": 5.7496815,
                            # If estimator has been scaled, an "ESTIMATOR_UNSCALED" key will appear here
                            "TIME": 1509.393,
                            "DEATHS": 106.56669881823231,
                        },
                        ...
                    }
                },
                {
                    "POKEMON_CODENAME": "CACTURNE_SHADOW_FORM",
                    ...
                },
                ...
            ],
            ('WATERFALL', 'BLIZZARD'): [...],
            ...
        }
        """
        def parse_timings(timings):
            """
            Parse a dict in Pokebattler JSON that describes timings, such as estimator, TTW etc,
            associated with either an attacker's best performance or with a specific moveset.
            :param timings: JSON block with timings: {"estimator": 2.9663813, ...}
                    This block can be retrieved from either defender["total"] or defender["byMove"][0]["result"].
            :return: Processed dict with "ESTIMATOR", "TIME", "DEATHS"
            """
            return {"ESTIMATOR": timings.get("estimator", 0),
                    "TIME": timings.get("effectiveCombatTime", 0),
                    "DEATHS": timings.get("effectiveDeaths", 0)}  # Possible to have 0 deaths, won't have key in dict

        def parse_defender(def_dict):
            """
            Parse a "defender" in Pokebattler JSON (which are raid attackers).
            :param def_dict: JSON block for a single defender: {"pokemonId": "MAGNETON_SHADOW_FORM", ...}
            :return: Processed dict in format shown above
            """
            dct = {"POKEMON_CODENAME": def_dict["pokemonId"],
                   "LEVEL": def_dict["stats"]["level"],
                   "IV": "{}/{}/{}".format(
                       def_dict["stats"]["attack"], def_dict["stats"]["defense"], def_dict["stats"]["stamina"]),
                   "BY_MOVE": {}}
            dct.update(parse_timings(def_dict["total"]))
            for mvst_blk in reversed(def_dict["byMove"]):  # Pokebattler lists movesets from worst to best
                dct["BY_MOVE"][(mvst_blk["move1"], mvst_blk["move2"])] = parse_timings(mvst_blk["result"])
            return dct

        self.rankings_raw = {}
        lists_all_movesets = self.JSON["attackers"][0]["byMove"] + [self.JSON["attackers"][0]["randomMove"]]
        for lst_mvst in lists_all_movesets:
            # lst_mvst: {"move1": "RANDOM", "move2": "RANDOM", "defenders": ...}
            defenders = [parse_defender(blk) for blk in lst_mvst["defenders"]]
            defenders.reverse()  # Pokebattler lists counters from #30 to #1
            self.rankings_raw[(lst_mvst["move1"], lst_mvst["move2"])] = defenders
        self.rankings = copy.deepcopy(self.rankings_raw)

    def filter_rankings(self):
        """
        Filter the current rankings list in self.rankings according to AttackerCriteriaMulti.
        This CHANGES the value of self.rankings such that only attackers that meet
        AttackerCriteriaMulti are retained.

        In theory, when this function is called, self.rankings should have at least been parsed
        from JSON, and may or may not have been scaled depending on scaling settings.
        """
        def filter_attacker(atker_dict):
            """
            Filter a single attacker. Only retains movesets that pass the criteria check,
            and possibly removes the entire attacker altogehter (returns None).
            :param atker_dict: Dict describing an attacker from self.rankings_raw
            :return: Filtered dict in the same format, or None if the attacker should be removed
            """
            atker_filter = atker_dict.copy()
            codename, level = atker_filter["POKEMON_CODENAME"], atker_filter["LEVEL"]
            atker_filter["BY_MOVE"] = {
                (fast_codename, charged_codename): timings_dict
                for (fast_codename, charged_codename), timings_dict in atker_dict["BY_MOVE"].items()
                if self.attacker_criteria_multi.check_attacker(
                    pokemon_codename=codename, level=level,
                    fast_codename=fast_codename, charged_codename=charged_codename
                )
            }
            if not atker_filter["BY_MOVE"]:
                return None  # No moves meet criteria, remove attacker
            # Update overall timings
            best_moveset = self.get_best_moveset_for_attacker(attacker_data=atker_filter)
            atker_filter.update(atker_filter["BY_MOVE"][best_moveset])
            return atker_filter

        new_rankings = {}
        for mvst_key, mvst_val in self.rankings.items():
            new_rankings[mvst_key] = [filter_attacker(atker_dict) for atker_dict in mvst_val]
            new_rankings[mvst_key] = [atker_filter for atker_filter in new_rankings[mvst_key]
                                      if atker_filter]  # Remove Nones
        self.rankings = new_rankings

    def get_estimator_baseline(self, baseline_boss_moveset="random"):
        """
        Get the value of the estimator baseline from all attackers currently stored in self.rankings.
        This value will be scaled to 1.0, and all other estimators scaled proportionally.

        This is a query function that does not change the value of self.rankings.
        This function does not consider whether self.rankings has been filtered based on
        AttackerCriteriaMulti.

        For details on how scaling works, refer to CONFIG_ESTIMATOR_SCALING_SETTINGS in config.py.

        :param baseline_boss_moveset: The boss moveset that should be used to set the baseline,
            should be one of "random", "easiest" and "hardest".
            The minimum estimator across all attackers against this specific boss moveset will
            be used as the baseline, and will be scaled to 1.0.
        :return: Value of estimator baseline.
        """
        baseline_boss_moveset = baseline_boss_moveset.lower()
        if baseline_boss_moveset not in ["random", "easiest", "hardest"]:
            print(f"Error (CountersListSingle.get_estimator_baseline): "
                  f"Boss moveset option {baseline_boss_moveset} is invalid. Using 'random' as default.",
                  file=sys.stderr)
            baseline_boss_moveset = "random"

        # Determine baseline
        baselines_per_boss_moveset = {
            mvst_key: min(atker_dict["ESTIMATOR"] for atker_dict in atkers_list)
            for mvst_key, atkers_list in self.rankings.items()
        }
        baseline = baselines_per_boss_moveset[("RANDOM", "RANDOM")]
        if baseline_boss_moveset == "easiest":
            baseline = min(min_est for mvst, min_est in baselines_per_boss_moveset.items()
                           if mvst != ("RANDOM", "RANDOM"))
        elif baseline_boss_moveset == "hardest":
            baseline = max(min_est for mvst, min_est in baselines_per_boss_moveset.items()
                           if mvst != ("RANDOM", "RANDOM"))
        return baseline

    def scale_estimators(self, baseline_value=None, scaling_factor=None, baseline_boss_moveset="random"):
        """
        Scale the estimators of all attackers currently stored in self.rankings, such that
        the baseline (typically best attacker) gets an estimator of 1.0, and all others scaled
        proportionally.

        This function allows a specific baseline or scaling factor. Typical usage is to call
        get_estimator_baseline() first, then pass in its value as baseline_value.
        If the baseline and scaling factor are both unspecified, the function will call
        get_estimator_baseline() as the default option. This will use the baseline_boss_moveset
        parameter.

        This CHANGES the value of self.rankings, specifically all estimator values.
        Keeps the original values with key "ESTIMATOR_UNSCALED".
        This function does not consider whether self.rankings has been filtered based on
        AttackerCriteriaMulti.

        For details on how scaling works, refer to CONFIG_ESTIMATOR_SCALING_SETTINGS in config.py.

        :param baseline_value: A specific baseline value to be used for scaling of all estimators.
            Supersedes scaling_factor. In practice, do not give both parameters.
        :param scaling_factor: A specific scaling factor to be applied to all estimators.
            Only used if baseline_value is None.
            If both baseline_value and scaling_factor are None, the scaling factor will be computed
            based on the data and baseline options.
        :param baseline_boss_moveset: The boss moveset that should be used to set the baseline,
            should be one of "random", "easiest" and "hardest".
            The minimum estimator across all attackers against this specific boss moveset will
            be used as the baseline, and will be scaled to 1.0.
            Only used if both baseline_value and scaling_factor are None.
        """
        if baseline_value is None and scaling_factor is None:
            baseline_value = self.get_estimator_baseline(baseline_boss_moveset=baseline_boss_moveset)

        if baseline_value is not None:
            scaling_factor = 1.0 / baseline_value
            self.scaling_baseline = baseline_value
        else:
            self.scaling_baseline = 1.0 / scaling_factor

        for mvst_key, atkers_list in self.rankings.items():
            for atker_dict in atkers_list:
                atker_dict["ESTIMATOR_UNSCALED"] = atker_dict["ESTIMATOR"]
                atker_dict["ESTIMATOR"] *= scaling_factor
                for (fast_codename, charged_codename), timings_dict in atker_dict["BY_MOVE"].items():
                    timings_dict["ESTIMATOR_UNSCALED"] = timings_dict["ESTIMATOR"]
                    timings_dict["ESTIMATOR"] *= scaling_factor

    def get_best_moveset_for_attacker(self, attacker_data=None,
                                      boss_moveset=None, attacker_codename=None, attacker=None,
                                      filtered_data=True):
        """
        Get the best moveset for an attacker, using this CountersList object's
        default sorting option.

        The best practice is to specify attacker_data. If it's given, the following 3 fields can be
        omitted: boss_moveset, attacker_codename, attacker.
        If attacker_data is not given, boss_moveset and either of the two attacker fields are required
        to locate the attacker data from overall rankings.

        :param attacker_data: Data with attacker's info from self.rankings, if one is already located
        :param boss_moveset: Tuple with boss' fast and charged moves as code names (Key from self.rankings),
            if attacker_data is not given
        :param attacker_codename: Attacker's code name, if attacker_data is not given
        :param attacker: Attacker's Pokemon object, if attacker_data and attacker_codename are not given
        :param filtered_data: If True, use filtered data that only contain attackers that meet criteria.
            If False, use raw data that contains all attackers.
        :return: Tuple with attacker's best fast and charged moves as code names.
                Returns "Attacker unranked", "Attacker unranked" if this attacker is not found.
        """
        if not attacker_data:
            # Attempt to find attacker data from overall rankings
            ranking_use = self.rankings if filtered_data else self.rankings_raw
            if boss_moveset not in ranking_use:
                print(f"Error (CountersListSingle.get_best_moveset_for_attacker): "
                      f"Boss moveset {boss_moveset} not found.",
                      file=sys.stderr)
                return None, None
            if not attacker_codename and not attacker:
                print(f"Error (CountersListSingle.get_best_moveset_for_attacker): No attacker specified.",
                      file=sys.stderr)
                return None, None

            if not attacker_codename:
                attacker_codename = attacker.name
            attacker_datas = [atk for atk in ranking_use[boss_moveset]
                              if atk["POKEMON_CODENAME"] == attacker_codename]
            if not attacker_datas:
                return "Attacker unranked", "Attacker unranked"
            attacker_data = attacker_datas[0]

        return min(attacker_data["BY_MOVE"].keys(),
                   key=lambda mvst: attacker_data["BY_MOVE"][mvst][self.sort_option])

    def write_CSV_list(self, path, raw=True,
                       best_attacker_moveset=True, random_boss_moveset=True, specific_boss_moveset=False):
        """
        Write the counters list to CSV in list format, with the following headers:
        Attacker, Attacker Fast Move, Attacker Charged Move, Attacker Level, Attacker IV,
        Boss, Boss Fast Move, Boss Charged Move, Estimator, Time to Win, Deaths,
        Estimator Unscaled (if applicable)
        All fields are code names.

        The file will be stored in the following location:
        COUNTERS_DATA_PATH/Lists/<Tier code name>/<Boss code name>/
        <"Filtered,">Level <level>,<sort option str>,<weather str>,<friendship str>,<attack strategy str>,<dodge strategy str>.csv
        # TODO: Add the following to file name:
        # Include shadows, include megas, include legendaries
        # 3 boolean parameters in this function
        # Remove level from header

        :param path: Root path that stores all CSV file outputs
        :param raw: If True, use final self.rankings after scaling and filtering.
            If False, use raw data (self.rankings_raw) without scaling and filtering.
        :param best_attacker_moveset: If True, only the best moveset for each attacker will be written
        :param random_boss_moveset: If True, results for the random boss moveset will be included
        :param specific_boss_moveset: If True, results for specific boss movesets will be included
        """
        def get_row_attacker_moveset(boss_mvst_key, atk_dict, atk_mvst_key, atk_mvst_val):
            """
            Get row to write for an attacker with a specific moveset against a certain boss moveset.
            :param boss_mvst_key: Tuple with boss moveset, as key from self.rankings
            :param atk_dict: Dict with attacker name and data (with all movesets)
            :param atk_mvst_key: Tuple with boss moveset, as key from BY_MOVE dicts
            :param atk_mvst_val: Dict , as key from BY_MOVE dicts
            """
            ret = {
                "Attacker": atk_dict["POKEMON_CODENAME"],
                "Attacker Fast Move": atk_mvst_key[0],
                "Attacker Charged Move": atk_mvst_key[1],
                "Attacker Level": atk_dict["LEVEL"],
                "Attacker IV": atk_dict["IV"],
                "Boss": self.boss.pokemon_codename,
                "Boss Fast Move": boss_mvst_key[0],
                "Boss Charged Move": boss_mvst_key[1],
                "Estimator": atk_mvst_val["ESTIMATOR"],
                "Time to Win": atk_mvst_val["TIME"],
                "Deaths": atk_mvst_val["DEATHS"],
            }
            if "ESTIMATOR_UNSCALED" in atk_mvst_val:
                ret["Estimator Unscaled"] = atk_mvst_val["ESTIMATOR_UNSCALED"]
            return ret

        def get_rows_attacker(boss_mvst_key, atk_dict):
            """
            Get rows to write for an attacker against a certain boss moveset.
            :param boss_mvst_key: Tuple with boss moveset, as key from self.rankings
            :param atk_dict: Dict with attacker name and data
            """
            atk_mvsts = atk_dict["BY_MOVE"].keys()
            if best_attacker_moveset:
                atk_mvsts = [self.get_best_moveset_for_attacker(attacker_data=atk_dict)]
            return [get_row_attacker_moveset(boss_mvst_key, atk_dict,
                                             atk_mvst, atk_dict["BY_MOVE"][atk_mvst])
                    for atk_mvst in atk_mvsts]

        def write_boss_moveset(writer, boss_mvst_key, boss_mvst_val):
            """
            Write all data for a certain boss moveset (either random or specific),
            sorted across all (attacker, moveset) combinations.
            :param boss_mvst_key: Tuple with boss moveset, as key from self.rankings
            :param boss_mvst_val: List of attackers, as value from self.rankings
            """
            rows = []
            for atk_dict in boss_mvst_val:
                rows.extend(get_rows_attacker(boss_mvst_key, atk_dict))
            rows.sort(key=lambda row: row["Time to Win" if self.sort_option == "TIME" else "Estimator"])
            writer.writerows(rows)

        if not random_boss_moveset and not specific_boss_moveset:
            print(f"Warning (CountersListSingle.write_CSV_list): Neither random boss moveset nor specific boss moveset "
                  f"are chosen. Nothing written.",
                  file=sys.stderr)
            return
        rankings_use = self.rankings if raw else self.rankings_raw

        if self.trainer_id:
            filename = os.path.join(
                path, "Lists", self.boss.tier, self.boss.pokemon_codename,
                "{}Trainer ID {},{},{},{},{},{}.csv".format(
                    "Filtered," if raw else "",
                    self.trainer_id,
                    parse_sort_option_code2str(self.sort_option),
                    parse_weather_code2str(self.battle_settings.weather_code),
                    parse_friendship_code2str(self.battle_settings.friendship_code),
                    parse_attack_strategy_code2str(self.battle_settings.attack_strategy_code),
                    parse_dodge_strategy_code2str(self.battle_settings.dodge_strategy_code),
                )
            )
        else:
            filename = os.path.join(
                path, "Lists", self.boss.tier, self.boss.pokemon_codename,
                "{}Level {},{},{},{},{},{}.csv".format(
                    "Filtered," if raw else "",
                    self.attacker_level,
                    parse_sort_option_code2str(self.sort_option),
                    parse_weather_code2str(self.battle_settings.weather_code),
                    parse_friendship_code2str(self.battle_settings.friendship_code),
                    parse_attack_strategy_code2str(self.battle_settings.attack_strategy_code),
                    parse_dodge_strategy_code2str(self.battle_settings.dodge_strategy_code),
                )
            )
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w') as csv_file:
            fieldnames = ["Attacker", "Attacker Fast Move", "Attacker Charged Move",
                          "Attacker Level", "Attacker IV",
                          "Boss", "Boss Fast Move", "Boss Charged Move",
                          "Estimator", "Time to Win", "Deaths", "Estimator Unscaled"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            if random_boss_moveset:
                write_boss_moveset(writer, ('RANDOM', 'RANDOM'), rankings_use[('RANDOM', 'RANDOM')])
            if specific_boss_moveset:
                for mvst_key, mvst_val in rankings_use.items():
                    if mvst_key != ('RANDOM', 'RANDOM'):
                        write_boss_moveset(writer, mvst_key, mvst_val)


class CountersListsMultiBSLevel:
    """
    Class for multiple counters lists differing by battle settings and Pokemon level,
    against a particular raid boss.
    """
    def __init__(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5",
                 metadata=None, attacker_criteria_multi=None, battle_settings=None, sort_option="Estimator"):
        """
        Initialize the attributes, create individual CountersList objects, and get the JSON rankings.
        :param raid_boss: RaidBoss object
        :param raid_boss_pokemon: Pokemon object for the raid boss, if raid_boss is not provided.
        :param raid_boss_codename: Code name of the raid boss (e.g. "LANDORUS_THERIAN_FORM"),
                if raid_boss is not provided.
        :param raid_tier: Raid tier, either as natural language or code name,
                if raid_boss is not provided.
        :param metadata: Current Metadata object
        :param attacker_criteria_multi: AttackerCriteriaMulti object describing attackers to be used
        :param battle_settings: BattleSettings object, with one or multiple sets of battle settings.
        :param sort_option: Sorting option, as shown on Pokebattler (natural language or code name)
        """
        self.boss = None
        self.attacker_criteria_multi = None
        self.attacker_criteria_multi_levels = None  # All criteria by levels
        self.attacker_criteria_multi_ids = None  # All criteria by ids
        self.battle_settings = None
        self.results = None
        self.sort_option = parse_sort_option_str2code(sort_option)
        self.has_multiple_battle_settings = False
        self.JSON = None
        self.metadata = metadata

        self.lists_by_bs_by_level = {}
        # {<BattleSettings 1>: {20: <CountersListSingle>, 21: <CountersListSingle>, ...},
        #  <BattleSettings 2>: {20: <CountersListSingle>, 21: <CountersListSingle>, ...},
        #  ...}
        self.lists_by_bs_by_trainer_id = {}
        # {<BattleSettings 1>: {52719: <CountersListSingle>, ...},
        #  ...}

        self.init_raid_boss(raid_boss, raid_boss_pokemon, raid_boss_codename, raid_tier)
        self.init_attacker_criteria(attacker_criteria_multi)
        self.init_battle_settings(battle_settings)
        self.create_individual_lists()

    def init_raid_boss(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5"):
        """
        Finds the RaidBoss object from codename, if necessary.
        This populates the following fields: boss.
        """
        if raid_boss:
            self.boss = raid_boss
            return
        if not raid_boss_pokemon and not raid_boss_codename:
            print(f"Error (CountersListsMultiBSLevel.__init__): Raid boss, Pokemon or code name not found", file=sys.stderr)
            return
        if not raid_tier:
            print(f"Error (CountersListsMultiBSLevel.__init__): Raid boss or tier not found", file=sys.stderr)
            return
        raid_tier = parse_raid_tier_str2code(raid_tier)
        self.boss = RaidBoss(pokemon_obj=raid_boss_pokemon, pokemon_codename=raid_boss_codename,
                             tier_codename=raid_tier, metadata=self.metadata)

    def init_attacker_criteria(self, attacker_criteria_multi=None):
        """
        Loads the AttackerCriteriaMulti object and handles exceptions.
        This populates the following fields: attacker_criteria_multi.
        """
        if not attacker_criteria_multi:
            print(f"Warning (CountersListsMultiBSLevel.__init__): AttackerCriteriaMulti not found. "
                  f"Using default criteria.",
                  file=sys.stderr)
            attacker_criteria_multi = AttackerCriteriaMulti(sets=[AttackerCriteria(metadata=self.metadata)],
                                                            metadata=self.metadata)
        if type(attacker_criteria_multi) is AttackerCriteria:
            print(f"Warning (CountersListsMultiBSLevel.__init__): Only a singular AttackerCriteria passed in, "
                  f"expected AttackerCriteriaMulti. Packaging it into multi criteria.",
                  file=sys.stderr)
            attacker_criteria_multi = AttackerCriteriaMulti(sets=[attacker_criteria_multi],
                                                            metadata=self.metadata)
        self.attacker_criteria_multi = attacker_criteria_multi
        self.attacker_criteria_multi_levels = attacker_criteria_multi.get_subset_no_trainer_ids()
        self.attacker_criteria_multi_ids = attacker_criteria_multi.get_subset_trainer_ids()

    def init_battle_settings(self, battle_settings=None):
        """
        Loads the BattleSettings object and handles exceptions.
        This populates the following fields: bottle_settings, has_multiple_battle_settings.
        """
        if not battle_settings:
            print(f"Warning (CountersListsByLevel.__init__): BattleSettings not found. Using default settings.",
                  file=sys.stderr)
            battle_settings = BattleSettings()
        # if battle_settings.is_multiple():
        #     print(f"Warning (CountersListsByLevel.__init__): BattleSettings includes multiple settings "
        #           f"(this class requires a single setting). Using the first set.",
        #           file=sys.stderr)
        #     battle_settings = battle_settings.indiv_settings[0]
        self.battle_settings = battle_settings
        self.has_multiple_battle_settings = battle_settings.is_multiple()

    def create_individual_lists(self):
        """
        Create individual CounterList objects that store rankings for a particular
        battle setting and level.
        This populates the field lists_by_bs_by_level.
        """
        for bs in self.battle_settings.get_indiv_settings():
            self.lists_by_bs_by_level[bs] = {}
            self.lists_by_bs_by_trainer_id[bs] = {}
            for level in self.attacker_criteria_multi.all_levels():
                self.lists_by_bs_by_level[bs][level] = CountersListSingle(
                    raid_boss=self.boss, metadata=self.metadata, attacker_level=level,
                    attacker_criteria_multi=self.attacker_criteria_multi_levels,  # self.attacker_criteria_multi,
                    battle_settings=bs,
                    sort_option=self.sort_option
                )
            for id in self.attacker_criteria_multi.pokebattler_trainer_ids():
                self.lists_by_bs_by_trainer_id[bs][id] = CountersListSingle(
                    raid_boss=self.boss, metadata=self.metadata, trainer_id=id,
                    attacker_criteria_multi=self.attacker_criteria_multi_ids,  # self.attacker_criteria_multi,
                    battle_settings=bs,
                    sort_option=self.sort_option
                )

    def load_and_parse_JSON(self):
        """
        Pull the Pokebattler JSON for all CountersListSingle objects and parse them.
        """
        for lvl_to_lst in self.lists_by_bs_by_level.values():
            for lst in lvl_to_lst.values():
                lst.load_JSON()
                lst.parse_JSON()
        for id_to_lst in self.lists_by_bs_by_trainer_id.values():
            for lst in id_to_lst.values():
                lst.load_JSON()
                lst.parse_JSON()

    def filter_rankings(self):
        """
        Filter the raw rankings list that has been parsed from JSON, according to
        AttackerCriteriaMulti.
        """
        for lvl_to_lst in self.lists_by_bs_by_level.values():
            for lst in lvl_to_lst.values():
                lst.filter_rankings()
        for id_to_lst in self.lists_by_bs_by_trainer_id.values():
            for lst in id_to_lst.values():
                lst.filter_rankings()

    def get_estimator_baselines(self, baseline_boss_moveset="random", baseline_attacker_level="by level"):
        """
        Get the value of the estimator baselines for each member CountersListSingle object.
        This value will be scaled to 1.0, and all other estimators scaled proportionally.

        baseline_attacker_level specifies a baseline level if applicable. The same baseline
        will be used for all member lists with a particular BattleSettings.
        If not specified, a baseline will be computed for each individual list with specific
        BattleSettings and level.

        This is a query function that does not change the value of self.rankings.
        This function does not consider whether self.rankings has been filtered based on
        AttackerCriteriaMulti.

        For details on how scaling works, refer to CONFIG_ESTIMATOR_SCALING_SETTINGS in config.py.

        :param baseline_boss_moveset: The boss moveset that should be used to set the baseline,
            should be one of "random", "easiest" and "hardest".
            The minimum estimator across all attackers against this specific boss moveset will
            be used as the baseline, and will be scaled to 1.0.
        :param baseline_attacker_level: Baseline attacker level to determine estimators, or
            a criterion for the baseline level.
            If the value is "by level", -1 or None, this is turned off, and compute baseline
            separately for each individual list.
            Should be a number (either numeric or string), "min", "max", "average" or "by level".
        :return: A tuple with two 2D dicts, the first mapping BattleSettings and then attacker level
            to the baseline value, the second mapping BattleSettings and then Trainer ID to baseline value.
            (Same format as (self.lists_by_bs_by_level, self.lists_by_bs_by_trainer_id))
        """
        # TODO: Add an option to get baseline by trainer ID?
        ret, ret_id = {}, {}
        for bs, lvl_to_list in self.lists_by_bs_by_level.items():
            ret[bs] = {}
            ret_id[bs] = {}
            # Find baseline level
            base_lvl = -1  # -1 for "by level"
            if baseline_attacker_level:
                if type(baseline_attacker_level) in [int, float] and baseline_attacker_level > 0:
                    base_lvl = baseline_attacker_level
                elif type(baseline_attacker_level) is str:
                    baseline_attacker_level = baseline_attacker_level.lower()
                    if baseline_attacker_level == "min":
                        base_lvl = min(lvl_to_list.keys())
                    elif baseline_attacker_level == "max":
                        base_lvl = max(lvl_to_list.keys())
                    elif baseline_attacker_level == "average":
                        base_lvl = sum(lvl_to_list.keys()) / len(lvl_to_list.keys())
            if base_lvl > 0:
                if base_lvl not in lvl_to_list:
                    print(f"Error (CountersListsMultiBSLevel.get_estimator_baselines): "
                          f"Baseline level {base_lvl} (parsed or computed) is invalid for battle settings {bs}.\n"
                          f"Falling back on default option: scale each level independently.",
                          file=sys.stderr)
                else:
                    baseline = lvl_to_list[base_lvl].get_estimator_baseline(
                        baseline_boss_moveset=baseline_boss_moveset)
                    ret[bs] = {lvl: baseline for lvl in lvl_to_list.keys()}
                    ret_id[bs] = {id: baseline for id in self.lists_by_bs_by_trainer_id[bs].keys()}
                    continue  # Next BS
            # Baseline level not specified or failed, scale each level independently
            ret[bs] = {
                lvl: lst.get_estimator_baseline(baseline_boss_moveset=baseline_boss_moveset)
                for lvl, lst in lvl_to_list.items()}
            ret_id[bs] = {
                id: lst.get_estimator_baseline(baseline_boss_moveset=baseline_boss_moveset)
                for id, lst in self.lists_by_bs_by_trainer_id[bs].items()}
        return ret, ret_id

    def scale_estimators(self, baselines_dict=None, baselines_id_dict=None,
                         baseline_boss_moveset="random", baseline_attacker_level="by level"):
        """
        Scale the estimators of all attackers currently stored in self.rankings of each
        member CountersListSingle object, such that the baseline (typically best attacker) gets
        an estimator of 1.0, and all others scaled proportionally.

        This function allows a specific dict of baseline values for each member list.
        Typical usage is to call get_estimator_baselines() first, then pass in its value as baselines_dict.
        If baselines_dict is unspecified, the function will call get_estimator_baselines() as the
        default option. This will use the baseline_boss_moveset and baseline_attacker_level parameters.

        This CHANGES the value of self.rankings, specifically all estimator values.
        Keeps the original values with key "ESTIMATOR_UNSCALED".
        This function does not consider whether self.rankings has been filtered based on
        AttackerCriteriaMulti.

        For details on how scaling works, refer to CONFIG_ESTIMATOR_SCALING_SETTINGS in config.py.

        :param baselines_dict: 2D dict mapping BattleSettings and then attacker levels to the
            baseline value for that member CountersListSingle object.
        :param baselines_id_dict: 2D dict mapping BattleSettings and then trainer IDs to the
            baseline value for that member CountersListSingle object.
        :param baseline_boss_moveset: The boss moveset that should be used to set the baseline,
            should be one of "random", "easiest" and "hardest".
            The minimum estimator across all attackers against this specific boss moveset will
            be used as the baseline, and will be scaled to 1.0.
            Only used if baselines_dict is None.
        :param baseline_attacker_level: Baseline attacker level to determine estimators, or
            a criterion for the baseline level.
            If the value is "by level", -1 or None, this is turned off, and compute baseline
            separately for each individual list.
            Should be a number (either numeric or string), "min", "max", "average" or "by level".
            Only used if baselines_dict is None.
        """
        if not baselines_dict or not baselines_id_dict:
            baselines_dict, baselines_id_dict = self.get_estimator_baselines(
                baseline_boss_moveset=baseline_boss_moveset, baseline_attacker_level=baseline_attacker_level)
        for bs, lvl_to_lst in self.lists_by_bs_by_level.items():
            for lvl, lst in lvl_to_lst.items():
                lst.scale_estimators(baseline_value=baselines_dict[bs][lvl])
        for bs, id_to_lst in self.lists_by_bs_by_trainer_id.items():
            for id, lst in id_to_lst.items():
                lst.scale_estimators(baseline_value=baselines_id_dict[bs][id])

    def write_CSV_list(self, path, raw=True,
                       best_attacker_moveset=True, random_boss_moveset=True, specific_boss_moveset=False):
        """
        Write the counters lists to CSV in list format, with the following headers:
        Attacker , Attacker Fast Move, Attacker Charged Move, Boss, Boss Fast Move, Boss Charged Move,
        Estimator, Time to Win, Deaths
        All fields are code names.

        The file will be stored in the following location:
        COUNTERS_DATA_PATH/Lists/<Tier code name>/<Boss code name>/
        Level <level>,<sort option str>,<weather str>,<friendship str>,<attack strategy str>,<dodge strategy str>.csv

        :param path: Root path that stores all CSV file outputs
        :param raw: If True, use final self.rankings after scaling and filtering.
            If False, use raw data (self.rankings_raw) without scaling and filtering.
        :param best_attacker_moveset: If True, only the best moveset for each attacker will be written
        :param random_boss_moveset: If True, results for the random boss moveset will be included
        :param specific_boss_moveset: If True, results for specific boss movesets will be included
        """
        for lvl_to_lst in self.lists_by_bs_by_level.values():
            for lst in lvl_to_lst.values():
                lst.write_CSV_list(path, raw=raw, best_attacker_moveset=best_attacker_moveset,
                                   random_boss_moveset=random_boss_moveset, specific_boss_moveset=specific_boss_moveset)
        for id_to_lst in self.lists_by_bs_by_trainer_id.values():
            for lst in id_to_lst.values():
                lst.write_CSV_list(path, raw=raw, best_attacker_moveset=best_attacker_moveset,
                                   random_boss_moveset=random_boss_moveset, specific_boss_moveset=specific_boss_moveset)


class CountersListsRE:
    """
    Class for multiple counters lists against a RaidEnsemble, with possibly multiple
    levels.
    Battle settings are typically specified in the RaidEnsemble, and therefore
    not included in this object.
    """
    def __init__(self, ensemble, metadata=None,
                 attacker_criteria_multi=None,
                 sort_option="Estimator", scaling_settings=None):
        """
        Initialize the attributes, create individual CountersListsByLevel objects, and get the JSON rankings.
        :param ensemble: RaidBoss object
        :param metadata: Current Metadata object
        :param attacker_criteria_multi: AttackerCriteriaMulti object describing attackers to be used
        :param sort_option: Sorting option, as shown on Pokebattler (natural language or code name)
        :param scaling_settings: Dict describing settings for estimator scaling (from config.py)
        """
        self.ensemble = ensemble
        self.attacker_criteria_multi = None
        self.results = None
        self.sort_option = parse_sort_option_str2code(sort_option)
        self.scaling_settings = scaling_settings
        self.JSON = None
        self.metadata = metadata

        self.init_attacker_criteria(attacker_criteria_multi)
        self.lists_for_bosses = []  # List of CountersLists objects for each boss,
                                    # in the same order as they're listed in the ensemble

        self.create_individual_lists()

    def init_attacker_criteria(self, attacker_criteria_multi=None):
        """
        Loads the AttackerCriteriaMulti object and handles exceptions.
        This populates the following fields: attacker_criteria_multi.
        """
        if not attacker_criteria_multi:
            print(f"Warning (CountersListsRE.__init__): AttackerCriteriaMulti not found. "
                  f"Using default criteria.",
                  file=sys.stderr)
            attacker_criteria_multi = AttackerCriteriaMulti(sets=[AttackerCriteria(metadata=self.metadata)],
                                                            metadata=self.metadata)
        if type(attacker_criteria_multi) is AttackerCriteria:
            print(f"Warning (CountersListsRE.__init__): Only a singular AttackerCriteria passed in, "
                  f"expected AttackerCriteriaMulti. Packaging it into multi criteria.",
                  file=sys.stderr)
            attacker_criteria_multi = AttackerCriteriaMulti(sets=[attacker_criteria_multi],
                                                            metadata=self.metadata)
        self.attacker_criteria_multi = attacker_criteria_multi

    def create_individual_lists(self):
        """
        Create individual CounterListsByLevel objects that store rankings for each boss.
        This populates the field lists_for_bosses.
        """
        for i, (boss, weight) in enumerate(self.ensemble.bosses):
            bs = self.ensemble.battle_settings[i]
            self.lists_for_bosses.append(CountersListsMultiBSLevel(
                raid_boss=boss, metadata=self.metadata,
                attacker_criteria_multi=self.attacker_criteria_multi, battle_settings=bs,
                sort_option=self.sort_option
            ))

    def get_boss_weights_bs_counters_list(self):
        """
        Build a list containing each RaidBoss, its weight, its BattleSettings,
        and its CounterListsMultiBSLevel.
        (Essentially breaking down RaidEnsemble back to list and adding counter lists.)
        :return: List containing (RaidBoss, weight, BattleSettings, CounterListsMultiBSLevel) tuples
        """
        return [(boss, weight, self.ensemble.battle_settings[i], self.lists_for_bosses[i])
                for i, (boss, weight) in enumerate(self.ensemble.bosses)]

    def load_and_parse_JSON(self):
        """
        Pull the Pokebattler JSON for all CountersListMultiBSLevel objects and parse them.
        """
        for lst in self.lists_for_bosses:
            lst.load_and_parse_JSON()

    def filter_rankings(self):
        """
        Filter the raw rankings list that has been parsed from JSON, according to
        AttackerCriteriaMulti.
        """
        for lst in self.lists_for_bosses:
            lst.filter_rankings()

    def get_estimator_baselines(self, baseline_boss_moveset="random", baseline_attacker_level="by level"):
        """
        Get the value of the estimator baselines for each member CountersListsMultiBSLevel object.
        This value will be scaled to 1.0, and all other estimators scaled proportionally.

        Since member lists have different bosses, they will always be scaled separately.
        The baseline_boss_moveset and baseline_attacker_level parameters are supplied to
        each member list. For more info, see documentation for CountersListsMultiBSLevel.get_estimator_baselines.

        For details on how scaling works, refer to CONFIG_ESTIMATOR_SCALING_SETTINGS in config.py.

        :param baseline_boss_moveset: The boss moveset that should be used to set the baseline,
            should be one of "random", "easiest" and "hardest".
            The minimum estimator across all attackers against this specific boss moveset will
            be used as the baseline, and will be scaled to 1.0.
        :param baseline_attacker_level: Baseline attacker level to determine estimators, or
            a criterion for the baseline level.
            If the value is "by level", -1 or None, this is turned off, and compute baseline
            separately for each individual list.
            Should be a number (either numeric or string), "min", "max", "average" or "by level".
        :return: A list of tuples of two dicts of baseline values for each member list,
            in the same order as the ensemble.
            (Same format as self.lists_for_bosses)
        """
        return [lst.get_estimator_baselines(
                    baseline_boss_moveset=baseline_boss_moveset,baseline_attacker_level=baseline_attacker_level)
                for lst in self.lists_for_bosses]

    def scale_estimators(self, baselines_list=None,
                         baseline_boss_moveset="random", baseline_attacker_level="by level"):
        """
        Scale the estimators of all attackers currently stored in self.rankings of each
        member CountersListsMultiBSLevel object, such that the baseline (typically best attacker) gets
        an estimator of 1.0, and all others scaled proportionally.

        This function allows a specific list of baseline values for each member list.
        Typical usage is to call get_estimator_baselines() first, then pass in its value as baselines_list.
        If baselines_list is unspecified, the function will call get_estimator_baselines() as the
        default option. This will use the baseline_boss_moveset and baseline_attacker_level parameters.

        This CHANGES the value of self.rankings, specifically all estimator values.
        Keeps the original values with key "ESTIMATOR_UNSCALED".
        This function does not consider whether self.rankings has been filtered based on
        AttackerCriteriaMulti.

        For details on how scaling works, refer to CONFIG_ESTIMATOR_SCALING_SETTINGS in config.py.

        :param baselines_list: List of tuples of 2 dicts of baseline values for each member list,
            in the same order as the ensemble.
        :param baseline_boss_moveset: The boss moveset that should be used to set the baseline,
            should be one of "random", "easiest" and "hardest".
            The minimum estimator across all attackers against this specific boss moveset will
            be used as the baseline, and will be scaled to 1.0.
            Only used if baselines_list is None.
        :param baseline_attacker_level: Baseline attacker level to determine estimators, or
            a criterion for the baseline level.
            If the value is "by level", -1 or None, this is turned off, and compute baseline
            separately for each individual list.
            Should be a number (either numeric or string), "min", "max", "average" or "by level".
            Only used if baselines_list is None.
        """
        if not baselines_list:
            baselines_list = self.get_estimator_baselines(baseline_boss_moveset=baseline_boss_moveset,
                                                          baseline_attacker_level=baseline_attacker_level)
        for i, lst in enumerate(self.lists_for_bosses):
            baselines, baselines_id = baselines_list[i]
            lst.scale_estimators(baselines_dict=baselines, baselines_id_dict=baselines_id)

    def load_and_process_all_lists(self):
        """
        Pull all Pokebattler counters lists and process them (filtering, scaling)
        for each member CountersListSingle object.
        Uses scaling settings stored in this object.
        In practice, you only need to call this to get all data.
        """
        self.load_and_parse_JSON()
        if self.scaling_settings["Enabled"] and self.scaling_settings["Baseline chosen before filter"]:
            self.scale_estimators(baseline_boss_moveset=self.scaling_settings["Baseline boss moveset"],
                                  baseline_attacker_level=self.scaling_settings["Baseline attacker level"])
        self.filter_rankings()
        if self.scaling_settings["Enabled"] and not self.scaling_settings["Baseline chosen before filter"]:
            self.scale_estimators(baseline_boss_moveset=self.scaling_settings["Baseline boss moveset"],
                                  baseline_attacker_level=self.scaling_settings["Baseline attacker level"])

    def write_CSV_list(self, path, raw=True,
                       best_attacker_moveset=True, random_boss_moveset=True, specific_boss_moveset=False):
        """
        Write the counters lists to CSV in list format, with the following headers:
        Attacker , Attacker Fast Move, Attacker Charged Move, Boss, Boss Fast Move, Boss Charged Move,
        Estimator, Time to Win, Deaths
        All fields are code names.

        The file will be stored in the following location:
        COUNTERS_DATA_PATH/Lists/<Tier code name>/<Boss code name>/
        Level <level>,<sort option str>,<weather str>,<friendship str>,<attack strategy str>,<dodge strategy str>.csv

        :param path: Root path that stores all CSV file outputs
        :param raw: If True, use final self.rankings after scaling and filtering.
            If False, use raw data (self.rankings_raw) without scaling and filtering.
        :param best_attacker_moveset: If True, only the best moveset for each attacker will be written
        :param random_boss_moveset: If True, results for the random boss moveset will be included
        :param specific_boss_moveset: If True, results for specific boss movesets will be included
        """
        for lst in self.lists_for_bosses:
            lst.write_CSV_list(path, raw=raw, best_attacker_moveset=best_attacker_moveset,
                               random_boss_moveset=random_boss_moveset, specific_boss_moveset=specific_boss_moveset)

    def temp_write_table(self, path,
                         combine_attacker_movesets=True,
                         random_boss_moveset=True, specific_boss_moveset=False,
                         write_unscaled=True, write_iv=False,
                         exclude=[]):
        # Temporary method for Bulbasaur CD analysis.
        # TODO: Clean up.

        attackers_boss_dict = {}
        # {("VENUSAUR_MEGA", "VINE_WHIP_FAST", "FRENZY_PLANT", "40", "15/15/15"):
        #     {
        #         ("GROUDON", "DRAGON_TAIL_FAST", "SOLAR_BEAM", "RAID_LEVEL_5", <Battle Settings object>, weight): {
        #             "ESTIMATOR": 1.0,
        #             "ESTIMATOR_UNSCALED": 2.5,
        #             "TIME": 1509.393,
        #             "DEATHS": 106.56669881823231,
        #         }, ...
        #     }, ...
        # }
        boss_keys = set()

        def update_single_list(lst, bs, boss, weight):
            """
            Update attackers_boss_dict and boss_keys using values from a CountersListSingle.
            This applies to both lists by level and by trainer IDs.
            :param lst: CountersListSingle to be used
            :param bs: BattleSettings object
            :param boss: RaidBoss object
            :param weight: Weight of the boss
            """
            for boss_mvst, atkers_list in lst.rankings.items():
                for atker_dict in atkers_list:
                    for atker_mvst, timings in atker_dict["BY_MOVE"].items():
                        atker_key = (atker_dict["POKEMON_CODENAME"], atker_mvst[0], atker_mvst[1],
                                     atker_dict["LEVEL"], atker_dict["IV"])
                        boss_key = (boss.pokemon_codename, boss_mvst[0], boss_mvst[1], boss.tier, bs, weight)
                        if atker_key not in attackers_boss_dict:
                            attackers_boss_dict[atker_key] = {}
                        attackers_boss_dict[atker_key][boss_key] = copy.deepcopy(timings)
                        boss_keys.add(boss_key)

        for i, lst_bslvl in enumerate(self.lists_for_bosses):
            boss, weight = self.ensemble.bosses[i]
            for bs, lvl_to_lst in lst_bslvl.lists_by_bs_by_level.items():
                for lvl, lst in lvl_to_lst.items():
                    update_single_list(lst, bs, boss, weight)
            for bs, id_to_lst in lst_bslvl.lists_by_bs_by_trainer_id.items():
                for id, lst in id_to_lst.items():
                    update_single_list(lst, bs, boss, weight)

        # Exclude certain attackers as specified (e.g. Black Kyurem against itself)
        attackers_boss_dict = {atker_key: val for atker_key, val in attackers_boss_dict.items()
                               if atker_key[0] not in exclude}

        # Filter boss keys according to settings
        boss_keys = list(boss_keys)
        boss_keys = [boss for boss in boss_keys
                     if (random_boss_moveset and boss[1] == "RANDOM"
                         or specific_boss_moveset and boss[1] != "RANDOM")]
        boss_keys.sort(key=lambda boss: (boss[0], "" if boss[1] == "RANDOM" else boss[1],  # Prioritize random
                                         "" if boss[2] == "RANDOM" else boss[2], boss[3], boss[4], boss[5]))
        # Reorder boss keys to restore their order in raid ensemble
        # TODO: Terribly inefficient.
        new_boss_keys = []
        for boss, weight in self.ensemble.bosses:
            boss_keys_add = [k for k in boss_keys if k[0] == boss.pokemon_codename and k[3] == boss.tier]
            new_boss_keys.extend(boss_keys_add)
        boss_keys = new_boss_keys

        # Estimate blank values
        # for atker_key, atker_values in attackers_boss_dict.items():
        #     for boss_key in boss_keys:
        #         if boss_key not in atker_values:
        #             print(f"Value not found: Attacker key = {atker_key}, Boss key = {boss_key}")
        # Too many blanks, need sysmetic ways of doing this

        # Combine attacker moves (e.g. FS/BB and Counter/BB Blaziken)
        if combine_attacker_movesets:
            new_atk_boss_dict = {}  # Same format
            atker_names_lvls_ivs = set((atker_key[0], atker_key[3], atker_key[4])
                                       for atker_key in attackers_boss_dict.keys())
            for atker, atker_lvl, atker_iv in atker_names_lvls_ivs:
                atker_curr_vals = {}  # Map boss keys to timings
                atker_curr_mvsts = {}  # Map boss keys to attacker movesets (fast, charged)
                for atker_mvst_key, atker_mvst_vals in attackers_boss_dict.items():
                    if not (atker_mvst_key[0] == atker and atker_mvst_key[3] == atker_lvl
                            and atker_mvst_key[4] == atker_iv):
                        continue
                    fast, charged = atker_mvst_key[1], atker_mvst_key[2]
                    for boss_key in boss_keys:
                        if boss_key not in atker_mvst_vals:
                            continue
                        timings = atker_mvst_vals[boss_key]
                        add = (boss_key not in atker_curr_vals
                               or timings[self.sort_option] < atker_curr_vals[boss_key][self.sort_option])
                        if add:
                            atker_curr_vals[boss_key] = timings
                            atker_curr_mvsts[boss_key] = (fast, charged)
                if not atker_curr_mvsts:
                    # This attacker doesn't show up in any of the boss movesets we're interested in
                    # Therefore, it no longer has to be in the output
                    continue
                best_fast = list(set(mvst[0] for mvst in atker_curr_mvsts.values()))
                best_charged = list(set(mvst[1] for mvst in atker_curr_mvsts.values()))
                new_atker_key = (atker, "Unknown" if not best_fast else " or ".join(best_fast),
                                 "Unknown" if not best_charged else " or ".join(best_charged), atker_lvl, atker_iv)
                new_atk_boss_dict[new_atker_key] = atker_curr_vals
            attackers_boss_dict = new_atk_boss_dict

        # Convert boss keys to headers
        boss_headers = [
            "{0}{1}, {2}".format(
                self.metadata.pokemon_codename_to_displayname(boss_key[0]),
                " ({0}/{1})".format(self.metadata.move_codename_to_displayname(boss_key[1]),
                                    self.metadata.move_codename_to_displayname(boss_key[2]))
                if boss_key[1] != 'RANDOM' else '',
                parse_raid_tier_code2str(boss_key[3])
            )
            for boss_key in boss_keys
        ]

        # Print what we have
        filename = os.path.join(path, "table.csv")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w') as csv_file:
            fieldnames = ["Attacker", "Fast Move", "Charged Move", "Level"]
            if write_iv:
                fieldnames.append("IV")
            fieldnames += boss_headers
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            # Write battle settings
            weights_row = {"Attacker": "(Battle settings)"}
            for i, boss_key in enumerate(boss_keys):
                weights_row[boss_headers[i]] = boss_key[4]
            writer.writerow(weights_row)

            # Write weights
            weights_row = {"Attacker": "(Boss weights)"}
            for i, boss_key in enumerate(boss_keys):
                weights_row[boss_headers[i]] = boss_key[5]
            writer.writerow(weights_row)

            for atker_key, atker_values in attackers_boss_dict.items():
                atker_row = {"Attacker": self.metadata.pokemon_codename_to_displayname(atker_key[0]),
                             "Fast Move": (
                                 "Unknown" if atker_key[1] == "Unknown"
                                 else " or ".join([self.metadata.move_codename_to_displayname(code)
                                                   for code in atker_key[1].split(" or ")])),
                             "Charged Move": (
                                 "Unknown" if atker_key[2] == "Unknown"
                                 else " or ".join([self.metadata.move_codename_to_displayname(code)
                                                   for code in atker_key[2].split(" or ")])),
                             "Level": atker_key[3]}
                if write_iv:
                    atker_row["IV"] = atker_key[4]
                for i, boss_key in enumerate(boss_keys):
                    if boss_key in atker_values:
                        atker_row[boss_headers[i]] = atker_values[boss_key][self.sort_option]
                writer.writerow(atker_row)

                if write_unscaled:
                    unscaled_row = atker_row.copy()
                    unscaled_row["Attacker"] = atker_row["Attacker"] + " (Unscaled)"
                    for i, boss_key in enumerate(boss_keys):
                        if boss_key in atker_values:
                            unscaled_row[boss_headers[i]] = atker_values[boss_key][self.sort_option + "_UNSCALED"]
                    writer.writerow(unscaled_row)

