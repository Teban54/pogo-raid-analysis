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

from utils import *
from params import *
from raid_boss import *
from get_json import *


class CountersListSingle:
    """
    Class for a single counters list, against a particular raid boss and
    under a particular set of battle settings.
    """
    def __init__(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5",
                 metadata=None, attacker_level=40, trainer_id=None,
                 attacker_criteria=None, battle_settings=None, sort_option="Estimator"):
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
        :param attacker_criteria: AttackerCriteria object describing attackers to be used
        :param battle_settings: BattleSettings object
        :param sort_option: Sorting option, as shown on Pokebattler (natural language or code name)
        """
        self.boss = None
        self.attacker_criteria = attacker_criteria
        self.battle_settings = None
        self.attacker_level = attacker_level
        self.trainer_id = trainer_id
        self.sort_option = parse_sort_option_str2code(sort_option)
        self.JSON = None
        self.metadata = metadata

        self.rankings = {}  # Mapping (fast move codename, charged move codename) pairs to lists
                            # For list format, see documentation for parse_JSON

        self.init_raid_boss(raid_boss, raid_boss_pokemon, raid_boss_codename, raid_tier)
        self.init_battle_settings(battle_settings)
        self.get_JSON()
        self.parse_JSON()

    def init_raid_boss(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5"):
        """
        Finds the RaidBoss object from codename, if necessary.
        This populates the following fields: boss.
        """
        if raid_boss:
            self.boss = raid_boss
            return
        if not raid_boss_pokemon and not raid_boss_codename:
            print(f"Error (CountersList.__init__): Raid boss, Pokemon or code name not found", file=sys.stderr)
            return
        if not raid_tier:
            print(f"Error (CountersList.__init__): Raid boss or tier not found", file=sys.stderr)
            return
        raid_tier = parse_raid_tier_str2code(raid_tier)
        self.boss = RaidBoss(pokemon_obj=raid_boss_pokemon, pokemon_codename=raid_boss_codename,
                             tier_codename=raid_tier, metadata=self.metadata)

    def init_battle_settings(self, battle_settings=None):
        """
        Loads the BattleSettings object and handles exceptions.
        This populates the following fields: bottle_settings.
        """
        if not battle_settings:
            print(f"Warning (CountersList.__init__): BattleSettings not found. Using default settings.",
                  file=sys.stderr)
            battle_settings = BattleSettings()
        if battle_settings.is_multiple():
            print(f"Warning (CountersList.__init__): BattleSettings includes multiple settings "
                  f"(this class requires a single setting). Using the first set.",
                  file=sys.stderr)
            battle_settings = battle_settings.indiv_settings[0]
        self.battle_settings = battle_settings

    def get_JSON(self):
        """
        Pull the Pokebattler JSON and store it in the object.
        """
        self.JSON = get_pokebattler_raid_counters(
            raid_boss=self.boss,
            attacker_level=self.attacker_level,
            trainer_id=self.trainer_id,
            battle_settings=self.battle_settings,
            sort_option=self.sort_option
        )

    def parse_JSON(self):
        """
        Process the Pokebattler JSON, including:
        - Splitting counters lists by boss movesets (random and specific)
        - Only keeping relevant data for each counter
        - Put the counters into correct order (JSON has them reversed)

        After this, self.rankings will be in the following format:
        {
            ('RANDOM', 'RANDOM'): [  # Listed from best to worst (in theory)
                {
                    "POKEMON_CODENAME": "MAGNETON_SHADOW_FORM",
                    "LEVEL": "40",  # String because .5
                    "IV": "15/15/15",
                    "ESTIMATOR": 2.9663813,  # Best moveset; keys match sort_options code names
                    "TIME": 778.319,  # Converted from milliseconds to seconds
                    "DEATHS": 55.08158337255771,
                    "BY_MOVE": {  # Listed from best to worst (in theory)
                        ('SPARK_FAST', 'FRUSTRATION'): {
                            "ESTIMATOR": 5.7496815,
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

        self.rankings = {}
        lists_all_movesets = self.JSON["attackers"][0]["byMove"] + [self.JSON["attackers"][0]["randomMove"]]
        for lst_mvst in lists_all_movesets:
            # lst_mvst: {"move1": "RANDOM", "move2": "RANDOM", "defenders": ...}
            defenders = [parse_defender(blk) for blk in lst_mvst["defenders"]]
            defenders.reverse()  # Pokebattler lists counters from #30 to #1
            self.rankings[(lst_mvst["move1"], lst_mvst["move2"])] = defenders

    def get_best_moveset_for_attacker(self, boss_moveset, attacker_codename=None, attacker=None,
                                      attacker_data=None):
        """
        Get the best moveset for an attacker, using this CountersList object's
        default sorting option.
        TODO: May not be needed after all?
        :param boss_moveset: Tuple with boss' fast and charged moves as code names
                (Key from self.rankings)
        :param attacker_codename: Attacker's code name
        :param attacker: Attacker's Pokemon object, if code name is not provided
        :param attacker_data: Data with attacker's info from self.rankings, if one is already located
        :return: Tuple with attacker's best fast and charged moves as code names.
                Returns "Attacker unranked", "Attacker unranked" if this attacker is not found.
        """
        if boss_moveset not in self.rankings:
            print(f"Error (CountersList.get_best_moveset_for_attacker): "
                  f"Boss moveset {boss_moveset} not found.",
                  file=sys.stderr)
            return None, None

        if not attacker_data:
            if not attacker_codename and not attacker:
                print(f"Error (CountersList.get_best_moveset_for_attacker): No attacker specified.",
                      file=sys.stderr)
                return None, None
            if not attacker_codename:
                attacker_codename = attacker.name
                attacker_datas = [atk for atk in self.rankings[boss_moveset]
                                  if atk["POKEMON_CODENAME"] == attacker_codename]
                if not attacker_datas:
                    return "Attacker unranked", "Attacker unranked"
                attacker_data = attacker_datas[0]

        return min(attacker_data["BY_MOVE"].keys(),
                   key=lambda mvst: attacker_data["BY_MOVE"][mvst][self.sort_option])

    def write_CSV_list(self, path, best_attacker_moveset=True,
                       random_boss_moveset=True, specific_boss_moveset=False):
        """
        Write the counters list to CSV in list format, with the following headers:
        Attacker , Attacker Fast Move, Attacker Charged Move, Boss, Boss Fast Move, Boss Charged Move,
        Estimator, Time to Win, Deaths
        All fields are code names.

        The file will be stored in the following location:
        COUNTERS_DATA_PATH/Lists/<Tier code name>/<Boss code name>/
        Level <level>,<sort option str>,<weather str>,<friendship str>,<attack strategy str>,<dodge strategy str>.csv
        # TODO: Add the following to file name:
        # Include shadows, include megas, include legendaries
        # 3 boolean parameters in this function

        :param path: Root path that stores all CSV file outputs
        :param best_attacker_moveset: If True, only the best moveset for each attacker will be written
        :param random_boss_moveset: If True, results for the random boss moveset will be included
        :param specific_boss_moveset: If True, results for specific boss movesets will be included
        """
        def get_row_attacker_moveset(writer, boss_mvst_key, atk_dict, atk_mvst_key, atk_mvst_val):
            """
            Get row to write for an attacker with a specific moveset against a certain boss moveset.
            :param boss_mvst_key: Tuple with boss moveset, as key from self.rankings
            :param atk_dict: Dict with attacker name and data (with all movesets)
            :param atk_mvst_key: Tuple with boss moveset, as key from BY_MOVE dicts
            :param atk_mvst_val: Dict , as key from BY_MOVE dicts
            """
            return {
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

        def get_rows_attacker(writer, boss_mvst_key, atk_dict):
            """
            Get rows to write for an attacker against a certain boss moveset.
            :param boss_mvst_key: Tuple with boss moveset, as key from self.rankings
            :param atk_dict: Dict with attacker name and data
            """
            atk_mvsts = atk_dict["BY_MOVE"].keys()
            if best_attacker_moveset:
                atk_mvsts = [self.get_best_moveset_for_attacker(boss_mvst_key, attacker_data=atk_dict)]
            return [get_row_attacker_moveset(writer, boss_mvst_key, atk_dict,
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
                rows.extend(get_rows_attacker(writer, boss_mvst_key, atk_dict))
            rows.sort(key=lambda row: row["Time to Win" if self.sort_option == "TIME" else "Estimator"])
            writer.writerows(rows)

        if not random_boss_moveset and not specific_boss_moveset:
            print(f"Warning (CountersList.write_CSV_list): Neither random boss moveset nor specific boss moveset "
                  f"are chosen. Nothing written.",
                  file=sys.stderr)
            return
        filename = os.path.join(
            path, "Lists", self.boss.tier, self.boss.pokemon_codename,
            "Level {},{},{},{},{},{}.csv".format(
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
                          "Estimator", "Time to Win", "Deaths"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            if random_boss_moveset:
                write_boss_moveset(writer, ('RANDOM', 'RANDOM'), self.rankings[('RANDOM', 'RANDOM')])
            if specific_boss_moveset:
                for mvst_key, mvst_val in self.rankings.items():
                    if mvst_key != ('RANDOM', 'RANDOM'):
                        write_boss_moveset(writer, mvst_key, mvst_val)


class CountersListsMultiBSLevel:
    """
    Class for multiple counters lists differing by battle settings and Pokemon level,
    against a particular raid boss.
    """
    def __init__(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5",
                 metadata=None, min_level=20, max_level=51, level_step=5,
                 attacker_criteria=None, battle_settings=None, sort_option="Estimator"):
        """
        Initialize the attributes, create individual CountersList objects, and get the JSON rankings.
        :param raid_boss: RaidBoss object
        :param raid_boss_pokemon: Pokemon object for the raid boss, if raid_boss is not provided.
        :param raid_boss_codename: Code name of the raid boss (e.g. "LANDORUS_THERIAN_FORM"),
                if raid_boss is not provided.
        :param raid_tier: Raid tier, either as natural language or code name,
                if raid_boss is not provided.
        :param metadata: Current Metadata object
        :param min_level: Minimum attacker level to be simulated, inclusive
        :param max_level: Maximum attacker level to be simulated, inclusive
        :param level_step: Step size for level, either 0.5 or integer
        :param attacker_criteria: AttackerCriteria object describing attackers to be used
        :param battle_settings: BattleSettings object, with one or multiple sets of battle settings.
        :param sort_option: Sorting option, as shown on Pokebattler (natural language or code name)
        """
        self.boss = None
        self.attacker_criteria = attacker_criteria
        self.battle_settings = None
        self.results = None
        self.min_level = min_level
        self.max_level = max_level
        self.level_step = level_step
        self.sort_option = parse_sort_option_str2code(sort_option)
        self.has_multiple_battle_settings = False
        self.JSON = None
        self.metadata = metadata

        self.lists_by_bs_by_level = {}
        # {<BattleSettings 1>: {20: <CountersListSingle>, 21: <CountersListSingle>, ...},
        #  <BattleSettings 2>: {20: <CountersListSingle>, 21: <CountersListSingle>, ...},
        #  ...}

        self.init_raid_boss(raid_boss, raid_boss_pokemon, raid_boss_codename, raid_tier)
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
            print(f"Error (CountersList.__init__): Raid boss, Pokemon or code name not found", file=sys.stderr)
            return
        if not raid_tier:
            print(f"Error (CountersList.__init__): Raid boss or tier not found", file=sys.stderr)
            return
        raid_tier = parse_raid_tier_str2code(raid_tier)
        self.boss = RaidBoss(pokemon_obj=raid_boss_pokemon, pokemon_codename=raid_boss_codename,
                             tier_codename=raid_tier, metadata=self.metadata)

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
            for level in get_levels_in_range(self.min_level, self.max_level, step_size=self.level_step):
                print(f"- Level {level}, Battle settings {bs}")
                self.lists_by_bs_by_level[bs][level] = CountersListSingle(
                    raid_boss=self.boss, metadata=self.metadata, attacker_level=level,
                    attacker_criteria=self.attacker_criteria, battle_settings=bs,
                    sort_option=self.sort_option
                )

    def write_CSV_list(self, path, best_attacker_moveset=True,
                       random_boss_moveset=True, specific_boss_moveset=False):
        """
        Write the counters lists to CSV in list format, with the following headers:
        Attacker , Attacker Fast Move, Attacker Charged Move, Boss, Boss Fast Move, Boss Charged Move,
        Estimator, Time to Win, Deaths
        All fields are code names.

        The file will be stored in the following location:
        COUNTERS_DATA_PATH/Lists/<Tier code name>/<Boss code name>/
        Level <level>,<sort option str>,<weather str>,<friendship str>,<attack strategy str>,<dodge strategy str>.csv

        :param path: Root path that stores all CSV file outputs
        :param best_attacker_moveset: If True, only the best moveset for each attacker will be written
        :param random_boss_moveset: If True, results for the random boss moveset will be included
        :param specific_boss_moveset: If True, results for specific boss movesets will be included
        """
        for lvl_to_lst in self.lists_by_bs_by_level.values():
            for lst in lvl_to_lst.values():
                lst.write_CSV_list(path, best_attacker_moveset=best_attacker_moveset,
                                   random_boss_moveset=random_boss_moveset, specific_boss_moveset=specific_boss_moveset)


class CountersListsRE:
    """
    Class for multiple counters lists against a RaidEnsemble, with possibly multiple
    levels.
    Battle settings are typically specified in the RaidEnsemble, and therefore
    not included in this object.
    """
    def __init__(self, ensemble,
                 metadata=None, min_level=20, max_level=51, level_step=5,
                 attacker_criteria=None, sort_option="Estimator"):
        """
        Initialize the attributes, create individual CountersListsByLevel objects, and get the JSON rankings.
        :param ensemble: RaidBoss object
        :param metadata: Current Metadata object
        :param min_level: Minimum attacker level to be simulated, inclusive
        :param max_level: Maximum attacker level to be simulated, inclusive
        :param level_step: Step size for level, either 0.5 or integer
        :param attacker_criteria: AttackerCriteria object describing attackers to be used
        :param sort_option: Sorting option, as shown on Pokebattler (natural language or code name)
        """
        self.ensemble = ensemble
        self.attacker_criteria = attacker_criteria
        self.results = None
        self.min_level = min_level
        self.max_level = max_level
        self.level_step = level_step
        self.sort_option = parse_sort_option_str2code(sort_option)
        self.JSON = None
        self.metadata = metadata

        self.lists_for_bosses = []  # List of CountersLists objects for each boss,
                                    # in the same order as they're listed in the ensemble

        self.create_individual_lists()

    def create_individual_lists(self):
        """
        Create individual CounterListsByLevel objects that store rankings for each boss.
        This populates the field lists_for_bosses.
        """
        for i, (boss, weight) in enumerate(self.ensemble.bosses):
            print("Creating lists for " + boss.pokemon_codename)
            bs = self.ensemble.battle_settings[i]
            self.lists_for_bosses.append(CountersListsMultiBSLevel(
                raid_boss=boss, metadata=self.metadata,
                min_level=self.min_level, max_level=self.max_level, level_step=self.level_step,
                attacker_criteria=self.attacker_criteria, battle_settings=bs,
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

    def write_CSV_list(self, path, best_attacker_moveset=True,
                       random_boss_moveset=True, specific_boss_moveset=False):
        """
        Write the counters lists to CSV in list format, with the following headers:
        Attacker , Attacker Fast Move, Attacker Charged Move, Boss, Boss Fast Move, Boss Charged Move,
        Estimator, Time to Win, Deaths
        All fields are code names.

        The file will be stored in the following location:
        COUNTERS_DATA_PATH/Lists/<Tier code name>/<Boss code name>/
        Level <level>,<sort option str>,<weather str>,<friendship str>,<attack strategy str>,<dodge strategy str>.csv

        :param path: Root path that stores all CSV file outputs
        :param best_attacker_moveset: If True, only the best moveset for each attacker will be written
        :param random_boss_moveset: If True, results for the random boss moveset will be included
        :param specific_boss_moveset: If True, results for specific boss movesets will be included
        """
        for lst in self.lists_for_bosses:
            lst.write_CSV_list(path, best_attacker_moveset=best_attacker_moveset,
                               random_boss_moveset=random_boss_moveset, specific_boss_moveset=specific_boss_moveset)
