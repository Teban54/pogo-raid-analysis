"""
This module includes two main types of utilities:
- A class that contains one or more sets of battle settings.
- Utilities for dealing with battle settings.
"""

from utils import *
from params import *


class BattleSettings:
    """
    Class for one or more sets of battle settings.

    Each instance of BattleSettings contains the following attributes:
    - Friendship level: No Friend, Good Friend, Great Friend, Ultra Friend, Best Friend.
      Default is Best Friend.
    - Weather: Extreme/No Weather/Neutral, Sunny/Clear, Rainy, Partly Cloudy, Cloudy, Windy, Snow, Fog.
      Default is Extreme.
    - Attack strategy (dodge or not): No Dodging, Dodge Specials PRO, Dodge All Weave.
      Default is No Dodging.
    - Dodge strategy (accuracy of dodging): Perfect Dodging, Realistic Dodging, Realistic Dodging Pro, 25% Dodging.
      Default is Realistic Dodging.
    (All settings are stored as code names. Display names are shown here for easier comprehension.)
    Notably, it does NOT contain attacker level.

    Each instance can contain one or more sets of possible battle settings.
    To represent multiple sets of battle settings, some attributes may contain multiple values to choose from,
    e.g. weather can be ['EXTREME', 'CLEAR', "RAINY'].
    When this happens, the constructor will create a list of BattleSetting objects with all combinations.
    """
    def __init__(self, friendship_str='best', weather_str='extreme',
                 attack_strategy_str='no dodging', dodge_strategy_str='realistic dodging'):
        """
        Initialize all battle settings.

        :param friendship_str: One or more friendship levels, either as natural language or code name.
        :param weather_str: One or more weathers, either as natural language or code name.
        :param attack_strategy_str: One or more attack strategies, either as natural language or code name.
        :param dodge_strategy_str: One or more dodge strategies, either as natural language or code name.
        """
        # Parse everything to code name
        self.friendship_code = self.init_one_setting(friendship_str, parse_friendship_str2code)
        self.weather_code = self.init_one_setting(weather_str, parse_weather_str2code)
        self.attack_strategy_code = self.init_one_setting(attack_strategy_str, parse_attack_strategy_str2code)
        self.dodge_strategy_code = self.init_one_setting(dodge_strategy_str, parse_dodge_strategy_str2code)

        self.multiple = any(type(setting) is list for setting in [
            self.friendship_code, self.weather_code, self.attack_strategy_code, self.dodge_strategy_code])
        self.indiv_settings = []  # Stores list of individual BattleSettings if this has multiple sets of options
        if self.multiple:
            self.indiv_settings = self.break_down_multiple()

    def init_one_setting(self, name_str, str2code_func):
        """
        Given (a) natural language name(s) of one setting (friendship, weather, or attack/dodge strategy),
        convert to code name.
        :param name_str: One or more names in natural language, as either string or list
        :param str2code_func: Function that converts a natural name to a code name, taking in a single parameter
        :return: A single string with code name, or a list if multiple options are provided
        """
        if type(name_str) is str:
            name_str = [name_str]
        list_code = [str2code_func(s) for s in name_str]
        return list_code[0] if len(list_code) == 1 else list_code

    def break_down_multiple(self):
        """
        Breaks down this BattleSettings object into a list of individual BattleSettings objects,
        each representing a single set of battle settings.
        :return: List of individual BattleSettings objects
        """
        flist, wlist, alist, dlist = (self.friendship_code, self.weather_code,
                                      self.attack_strategy_code, self.dodge_strategy_code)
        flist = [flist] if type(flist) is str else flist
        wlist = [wlist] if type(wlist) is str else wlist
        alist = [alist] if type(alist) is str else alist
        dlist = [dlist] if type(dlist) is str else dlist
        ret = [BattleSettings(friendship_str=f, weather_str=w, attack_strategy_str=a, dodge_strategy_str=d)
               for f in flist for w in wlist for a in alist for d in dlist]
        return ret

    def is_single(self):
        """
        Returns if this BattleSettings object contains a single set of settings.
        :return: True if this BattleSettings object contains a single set of settings
        """
        return not self.multiple

    def is_multiple(self):
        """
        Returns if this BattleSettings object contains multiple sets of settings.
        :return: True if this BattleSettings object contains multiple sets of settings
        """
        return self.multiple

    def get_csv_string(self):
        pass # TODO

    def debug_print(self):
        """
        Debug function that prints the settings to stdout.
        """
        if self.is_single():
            print(f"{self.friendship_code}, {self.weather_code}, {self.attack_strategy_code}, {self.dodge_strategy_code}")
        else:
            for indiv in self.indiv_settings:
                indiv.debug_print()


"""BS = BattleSettings(friendship_str=['no', 'ultra'],
                    weather_str=['neutral', 'sunny', 'rainy'],
                    attack_strategy_str=['no dodging', 'dodge specials'],
                    dodge_strategy_str=['realistic'])
BS.debug_print()"""