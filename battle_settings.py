"""
This module includes two main types of utilities:
- A class that contains one or more sets of battle settings.
- Utilities for dealing with battle settings.

Each instance of BattleSettings contains the following attributes:
- Weather: Extreme/No Weather/Neutral, Sunny/Clear, Rainy, Partly Cloudy, Cloudy, Windy, Snow, Fog.
  Default is Extreme.
- Friendship level: No Friend, Good Friend, Great Friend, Ultra Friend, Best Friend.
  Default is Best Friend.
- Attack strategy (dodge or not): No Dodging, Dodge Specials PRO, Dodge All Weave.
  Default is No Dodging.
- Dodge strategy (accuracy of dodging): Perfect Dodging, Realistic Dodging, Realistic Dodging Pro, 25% Dodging.
  Default is Realistic Dodging.
(All settings are stored as code names. Display names are shown here for easier comprehension.)
Notably, it does NOT contain attacker level, which falls under AttackerCriteria.

Each instance can contain one or more sets of possible battle settings.
To represent multiple sets of battle settings, some attributes may contain multiple values to choose from,
e.g. weather can be ['EXTREME', 'CLEAR', "RAINY'].
When this happens, the constructor will create a list of BattleSetting objects with all combinations.
"""

from utils import *
from params import *


class BattleSettings:
    """
    Class for one or more sets of battle settings.
    """
    def __init__(self, weather_str='extreme', friendship_str='best',
                 attack_strategy_str='no dodging', dodge_strategy_str='realistic dodging'):
        """
        Initialize all battle settings.

        :param weather_str: One or more weathers, either as natural language or code name.
        :param friendship_str: One or more friendship levels, either as natural language or code name.
        :param attack_strategy_str: One or more attack strategies, either as natural language or code name.
        :param dodge_strategy_str: One or more dodge strategies, either as natural language or code name.
        """
        # Parse everything to code name
        self.weather_code = self.init_one_setting(weather_str, parse_weather_str2code)
        self.friendship_code = self.init_one_setting(friendship_str, parse_friendship_str2code)
        self.attack_strategy_code = self.init_one_setting(attack_strategy_str, parse_attack_strategy_str2code)
        self.dodge_strategy_code = self.init_one_setting(dodge_strategy_str, parse_dodge_strategy_str2code)

        self.multiple = any(type(setting) is list for setting in [
            self.weather_code, self.friendship_code, self.attack_strategy_code, self.dodge_strategy_code])
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
        wlist, flist, alist, dlist = (self.weather_code, self.friendship_code,
                                      self.attack_strategy_code, self.dodge_strategy_code)
        wlist = [wlist] if type(wlist) is str else wlist
        flist = [flist] if type(flist) is str else flist
        alist = [alist] if type(alist) is str else alist
        dlist = [dlist] if type(dlist) is str else dlist
        ret = [BattleSettings(weather_str=w, friendship_str=f, attack_strategy_str=a, dodge_strategy_str=d)
               for w in wlist for f in flist for a in alist for d in dlist]
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

    def get_indiv_settings(self):
        """
        Get a list of all individual settings contained in this object.
        This will be a list containing this object itself if it only has one set of settings.
        :return: List of individual settings contained
        """
        return [self] if self.is_single() else self.indiv_settings

    def to_string(self, delimiter=',', multiple_settings_delimiter=';'):
        """
        Convert the object to a String with a given delimiter, in the following order:
        Weather, Friendship, Attack strategy, Dodge strategy. All in natural language.
        If this BattleSettings contains multiple individual settings, concatenate them
        with another delimiter.

        :param delimiter: Delimiter for components of an individual battle setting
        :param multiple_settings_delimiter: Delimiter between individual battle settings
        :return: Concatenated string
        """
        if self.is_single():
            return delimiter.join([
                parse_weather_code2str(self.weather_code),
                parse_friendship_code2str(self.friendship_code),
                parse_attack_strategy_code2str(self.attack_strategy_code),
                parse_dodge_strategy_code2str(self.dodge_strategy_code),
            ])
        return multiple_settings_delimiter.join(indiv.to_string(delimiter) for indiv in self.indiv_settings)

    def __str__(self):
        return self.to_string()

    def __hash__(self):
        if self.is_single():
            return hash((self.weather_code, self.friendship_code, self.attack_strategy_code, self.dodge_strategy_code))
        return hash(tuple([hash(indiv) for indiv in self.indiv_settings]))

    def __eq__(self, other):
        if type(other) is not BattleSettings:
            return False
        if self.is_single() and other.is_single():
            return ((self.weather_code, self.friendship_code, self.attack_strategy_code, self.dodge_strategy_code)
                    == (other.weather_code, other.friendship_code, other.attack_strategy_code, other.dodge_strategy_code))
        if self.is_multiple() and other.is_multiple():
            return self.indiv_settings == other.indiv_settings

    def debug_print(self):
        """
        Debug function that prints the settings to stdout.
        """
        if self.is_single():
            print(f"{self.weather_code}, {self.friendship_code}, {self.attack_strategy_code}, {self.dodge_strategy_code}")
        else:
            for indiv in self.indiv_settings:
                indiv.debug_print()


"""BS = BattleSettings(friendship_str=['no', 'ultra'],
                    weather_str=['neutral', 'sunny', 'rainy'],
                    attack_strategy_str=['no dodging', 'dodge specials'],
                    dodge_strategy_str=['realistic'])
BS.debug_print()"""