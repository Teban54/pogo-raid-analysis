"""
This module includes all classes for list(s) of raid counters against bosses,
at varying level of details.
Each time an instance of these classes is created, it pulls JSON data from Pokebattler
to generate the counters list immediately.

Currently, it includes classes for the following:
- A single list of counters against a particular boss, under a particular set of battle settings.
- Lists of counters for multiple attacker levels, with a particular boss and battle settings
  (aside from attacker level).
- Lists of counters against an ensemble of raid bosses, with multiple attacker levels for each ensemble.

This module also includes utilities for dealing with single or multiple counters lists.
"""

from utils import *
from params import *
from raid_boss import *
from get_json import *


class CountersList:
    """
    Class for a single counters list, against a particular raid boss and
    under a particular set of battle settings.
    """
    def __init__(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5",
                 metadata=None, attacker_level=40, trainer_id=None,
                 attacker_ensemble=None, battle_settings=None):
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
        :param attacker_ensemble: AttackerEnsemble object describing attackers to be used
        :param battle_settings: BattleSettings object
        """
        self.boss = None
        self.attacker_ensemble = attacker_ensemble
        self.battle_settings = battle_settings
        self.attacker_level = attacker_level
        self.trainer_id = trainer_id
        self.results = None
        self.JSON = None
        self.metadata = metadata

        self.init_raid_boss(raid_boss, raid_boss_pokemon, raid_boss_codename, raid_tier)
        self.get_JSON()

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

    def get_JSON(self):
        """
        Pull the Pokebattler JSON and store it in the object.
        """
        self.JSON = get_pokebattler_raid_counters(
            raid_boss=self.boss,
            attacker_level=self.attacker_level,
            trainer_id=self.trainer_id,
            # TODO: Remaining data to be parsed from battle settings and attacker ensemble later
        )


class CountersListsByLevel:
    """
    Class for multiple counters lists differing by Pokemon level,
    against a particular raid boss and under a particular set of battle settings.
    """
    def __init__(self, raid_boss=None, raid_boss_pokemon=None, raid_boss_codename=None, raid_tier="Tier 5",
                 metadata=None, min_level=20, max_level=51,
                 attacker_ensemble=None, battle_settings=None):
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
        :param attacker_ensemble: AttackerEnsemble object describing attackers to be used
        :param battle_settings: BattleSettings object
        """
        self.boss = None
        self.attacker_ensemble = attacker_ensemble
        self.battle_settings = battle_settings
        self.results = None
        self.JSON = None
        self.metadata = metadata

        self.lists_by_level = {}  # Dict mapping attacker level to CountersList object

        self.init_raid_boss(raid_boss, raid_boss_pokemon, raid_boss_codename, raid_tier)
        self.get_JSON()

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

    def create_individual_lists(self):
        """
        Create individual CounterList objects that store rankings for a particular level.
        This populates the field lists_by_level.
        """
        for level in range(self.min_level, self.max_level + 1, 0.5):
            self.lists_by_level[level] = CountersList(
                raid_boss=self.boss, metadata=self.metadata, attacker_level=level,
                attacker_ensemble=self.attacker_ensemble, battle_settings=self.battle_settings
            )
