"""
This module includes two main types of utilities:
- A class for moves.
- Utilities for dealing with single or multiple moves.
"""


from utils import *
from params import *


class Move:
    """
    Class for a specific move with its PvE data.
    """
    def __init__(self, pokebattler_JSON=None, move_codename=None, move_type=None):
        """
        Initialize the attributes and use the Pokebattler JSON information to fill them.
        :param pokebattler_JSON: JSON block from Pokebattler relating to this move
        :param move_codename: Code name of the move, in case JSON is not provided
        :param move_type: Code name of the type of the move, in case JSON is not provided
        """
        self.name = move_codename  # Possibly None if JSON is provided
        self.type = parse_type_code2str(move_type) if move_type else move_type  # Natural language
        self.displayname = None
        self.is_fast = False
        self.power = 0
        self.energy_delta = 0  # >0 for fast moves, <0 for charged moves
        self.duration = 0
        self.window_start = 0
        self.window_end = 0
        self.JSON = None

        if pokebattler_JSON:
            self.init_from_pokebattler(pokebattler_JSON)

        self.init_display_names()

    def init_from_pokebattler(self, JSON):
        """
        Parse basic information from the Pokebattler JSON.
        :param JSON: JSON block from Pokebattler relating to this move
        """
        self.JSON = JSON
        self.name = JSON['moveId']

        self.type = parse_type_code2str(JSON.get('type', "POKEMON_TYPE_NORMAL"))  # One copy of Hidden Power has no type
        self.power = JSON.get('power', 0)  # Splash, Transform, Yawn etc have 0 power
        self.energy_delta = JSON.get('energyDelta', 0)  # Struggle has 0 energy delta
        self.duration = JSON['durationMs']
        self.window_start = JSON['damageWindowStartMs']
        self.window_end = JSON['damageWindowEndMs']

    def init_display_names(self):
        """
        Process the move's display names, and determine if it's a fast move.
        This populates the following fields: displayname, is_fast.
        """
        if self.displayname:  # Already filled out
            return
        self.is_fast = "_FAST" in self.name
        self.displayname = parse_move_code2str(self.name)



