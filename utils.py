"""
Utilities functions
"""
import json
import requests
import os
import sys
import re

from params import *

# ----------------- HTTP -----------------


def do_http_request(url, payload={}):
    """
    Send an HTTP request and return the results as JSON.

    :param url: URL
    :param payload: Payload parameters
    :return: Results parsed as JSON, or None if an error occurred
    """
    try:
        r = requests.get(url, params=payload)
        if r.ok:
            return r.json()
        else:
            print("Error with HTTP request: " + str(r), file=sys.stderr)
            return None
    except Exception as e:
        print(e, file=sys.stderr)
        return None


# ----------------- JSON -----------------


def write_json_to_file(data, filename):
    """
    Write data to a JSON file.

    :param data: Data as Python object
    :param filename: Path and name of output file
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as fout:
        json.dump(data, fout)


def load_json_from_file(filename):
    """
    Load data from a JSON file.

    :param filename: Path and name of input file
    :return: Data as Python object
    """
    with open(filename, 'r') as fin:
        data = json.load(fin)
    return data


# ----------------- Parsing -----------------


def codename_to_displayname(codename):
    """
    Convert a code name with capital letters and _, such as FRENZY_PLANT,
    to a display name with spaces and first letters capitalized, e.g. Frenzy Plant.
    Does not apply to every situation.
    :param codename: code name with capital letters and _
    :return: display name with spaces and first letters capitalized
    """
    if codename is None:
        return None
    pb_str = map(str.capitalize, codename.split('_'))
    pb_str = ' '.join(pb_str)
    return pb_str


def GM_templateId_to_pokemon_codename(template_id):
    """
    Convert the templateId field of a Game Master item to a Pokemon's code name,
    or return None if it does not refer to a Pokemon.
    :param template_id: templateId field of a Game Master item
    :return Pokemon's code name, or None
    """
    match = re.match(r"V([0-9]{4})_POKEMON_(.+)", template_id)
    return match.group(2) if match else None


def check_attack_strategy_isstr(attack_strategy):
    """
    Check if a given string for attack strategy is natural language (e.g. "no dodging").

    :param attack_strategy: Attack strategy string to be checked.
    :return: Whether the string is natural language.
    """
    return any(x in attack_strategy.lower() for x in ['no', 'special', 'all']) and '_' not in attack_strategy


def check_attack_strategy_iscode(attack_strategy):
    """
    Check if a given string for attack strategy is Pokebattler code name (e.g. "CINEMATIC_ATTACK_WHEN_POSSIBLE").

    :param attack_strategy: Attack strategy string to be checked.
    :return: Whether the string is code name.
    """
    return attack_strategy.lower() in [
        x.lower() for x in ["CINEMATIC_ATTACK_WHEN_POSSIBLE", "DODGE_SPECIALS", "DODGE_WEAVE_CAUTIOUS"]]


def parse_attack_strategy_str2code(attack_strategy_str):
    """
    Parse attack strategy (i.e. dodge or not),
    from natural language (e.g. "No Dodging", "Dodge Specials PRO")
    to code name (e.g. "CINEMATIC_ATTACK_WHEN_POSSIBLE").

    :param attack_strategy_str: Attack strategy in natural language.
        Should be one of: "No Dodging", "Dodge Specials PRO", "Dodge All Weave".
    :return: Attack strategy in Pokebattler code name.
        Should be one of: "CINEMATIC_ATTACK_WHEN_POSSIBLE", "DODGE_SPECIALS", "DODGE_WEAVE_CAUTIOUS".
    """
    if not check_attack_strategy_isstr(attack_strategy_str) and not check_attack_strategy_iscode(attack_strategy_str):
        print(f"Warning (parse_attack_strategy_str2code): Attack strategy string {attack_strategy_str} is invalid",
              file=sys.stderr)
        return "CINEMATIC_ATTACK_WHEN_POSSIBLE"
    if check_attack_strategy_iscode(attack_strategy_str):
        return attack_strategy_str
    conv = {
        'no': "CINEMATIC_ATTACK_WHEN_POSSIBLE",
        'special': "DODGE_SPECIALS",
        'all': "DODGE_WEAVE_CAUTIOUS"
    }
    attack_strategy_str = attack_strategy_str.lower()
    strs = [val for key, val in conv.items() if key in attack_strategy_str]
    return strs[0] if strs else "CINEMATIC_ATTACK_WHEN_POSSIBLE"


def parse_attack_strategy_code2str(attack_strategy_code):
    """
    Parse attack strategy (i.e. dodge or not),
    from code name (e.g. "CINEMATIC_ATTACK_WHEN_POSSIBLE")
    to natural language (e.g. "No Dodging", "Dodge Specials PRO").

    :param attack_strategy_code: Attack strategy in Pokebattler code name.
        Should be one of: "CINEMATIC_ATTACK_WHEN_POSSIBLE", "DODGE_SPECIALS", "DODGE_WEAVE_CAUTIOUS".
    :return: Attack strategy in natural language.
        Should be one of: "No Dodging", "Dodge Specials PRO", "Dodge All Weave".
    """
    if not check_attack_strategy_isstr(attack_strategy_code) and not check_attack_strategy_iscode(attack_strategy_code):
        print(f"Warning (parse_attack_strategy_code2str): Attack strategy string {attack_strategy_code} is invalid",
              file=sys.stderr)
        return "No Dodging"
    if check_attack_strategy_isstr(attack_strategy_code):
        return attack_strategy_code
    conv = {
        "CINEMATIC_ATTACK_WHEN_POSSIBLE": "No Dodging",
        "DODGE_SPECIALS": "Dodge Specials PRO",
        "DODGE_WEAVE_CAUTIOUS": "Dodge All Weave"
    }
    return conv.get(attack_strategy_code.upper(), "No Dodging")


def check_dodge_strategy_isstr(dodge_strategy):
    """
    Check if a given string for dodge strategy is natural language (e.g. "realistic dodging").

    :param dodge_strategy: Dodge strategy string to be checked.
    :return: Whether the string is natural language.
    """
    return any(x in dodge_strategy.lower() for x in ['perfect', 'realistic', '25']) and '_' not in dodge_strategy


def check_dodge_strategy_iscode(dodge_strategy):
    """
    Check if a given string for dodge strategy is Pokebattler code name (e.g. "DODGE_REACTION_TIME").

    :param dodge_strategy: Dodge strategy string to be checked.
    :return: Whether the string is code name.
    """
    return dodge_strategy.lower() in [
        x.lower() for x in ["DODGE_100", "DODGE_REACTION_TIME", "DODGE_REACTION_TIME2", "DODGE_25"]]


def parse_dodge_strategy_str2code(dodge_strategy_str):
    """
    Parse dodge strategy (i.e. accuracy of dodging),
    from natural language (e.g. "Perfect Dodging", "Realistic Dodging")
    to code name (e.g. "DODGE_REACTION_TIME").

    :param dodge_strategy_str: Dodge strategy in natural language.
        Should be one of: "Perfect Dodging", "Realistic Dodging", "Realistic Dodging Pro", "25% Dodging".
    :return: Dodge strategy in Pokebattler code name.
        Should be one of: "DODGE_100", "DODGE_REACTION_TIME", "DODGE_REACTION_TIME2", "DODGE_25".
    """
    if not check_dodge_strategy_isstr(dodge_strategy_str) and not check_dodge_strategy_iscode(dodge_strategy_str):
        print(f"Warning (parse_dodge_strategy_str2code): Dodge strategy string {dodge_strategy_str} is invalid",
              file=sys.stderr)
        return "DODGE_REACTION_TIME"
    if check_dodge_strategy_iscode(dodge_strategy_str):
        return dodge_strategy_str
    conv = {
        'perfect': "DODGE_100",
        'pro': "DODGE_REACTION_TIME2",
        '25': "DODGE_25"
    }
    dodge_strategy_str = dodge_strategy_str.lower()
    strs = [val for key, val in conv.items() if key in dodge_strategy_str]
    return strs[0] if strs else "DODGE_REACTION_TIME"  # "realistic dodging" falls here


def parse_dodge_strategy_code2str(dodge_strategy_code):
    """
    Parse dodge strategy (i.e. accuracy of dodging),
    from code name (e.g. "DODGE_REACTION_TIME")
    to natural language (e.g. "Perfect Dodging", "Realistic Dodging").

    :param dodge_strategy_code: Dodge strategy in Pokebattler code name.
        Should be one of: "DODGE_100", "DODGE_REACTION_TIME", "DODGE_REACTION_TIME2", "DODGE_25".
    :return: Dodge strategy in natural language.
        Should be one of: "Perfect Dodging", "Realistic Dodging", "Realistic Dodging Pro", "25% Dodging".
    """
    if not check_dodge_strategy_isstr(dodge_strategy_code) and not check_dodge_strategy_iscode(dodge_strategy_code):
        print(f"Warning (parse_dodge_strategy_code2str): Dodge strategy string {dodge_strategy_code} is invalid",
              file=sys.stderr)
        return "Realistic Dodging"
    if check_dodge_strategy_isstr(dodge_strategy_code):
        return dodge_strategy_code
    conv = {
        "DODGE_100": "Perfect Dodging",
        "DODGE_REACTION_TIME": "Realistic Dodging",
        "DODGE_REACTION_TIME2": "Realistic Dodging Pro",
        "DODGE_25": "25% Dodging"
    }
    return conv.get(dodge_strategy_code.upper(), "Realistic Dodging")


"""
Parser for sorting that could be implemented:
{
    "Overall": "OVERALL",
    "Power": "POWER",
    "Win %": "WIN",
    "Time to Win": "TIME",
    "Potions": "POTIONS",
    "Damage (TDO)": "TDO",
    "Estimator": "ESTIMATOR"
}
Ignored for now since options other than Estimator and TTW are rarely used. 
"""


def check_friendship_isstr(friendship):
    """
    Check if a given string for friendship is natural language (e.g. "best friend").

    :param friendship: Friendship string to be checked.
    :return: Whether the string is natural language.
    """
    return any(x in friendship.lower() for x in ['no', 'good', 'great', 'ultra', 'best'])


def check_friendship_iscode(friendship):
    """
    Check if a given string for friendship is Pokebattler code name (e.g. "FRIENDSHIP_LEVEL_4").

    :param friendship: Friendship string to be checked.
    :return: Whether the string is code name.
    """
    return friendship.lower() in [f"friendship_level_{x}" for x in range(5)]


def parse_friendship_str2code(friendship_str):
    """
    Parse friendship value from natural word (e.g. "best friend")
    to code name (e.g. "FRIENDSHIP_LEVEL_4").

    :param friendship_str: Friendship in natural language,
        includes "no", "good", "great", "ultra" or "best" in it (case-insensitive)
    :return: Friendship in Pokebattler code name,
        in the form of "FRIENDSHIP_LEVEL_<x>" where x is 0,1,2,3 or 4
    """
    if not check_friendship_isstr(friendship_str) and not check_friendship_iscode(friendship_str):
        print(f"Warning (parse_friendship_str2code): Friendship string {friendship_str} is invalid", file=sys.stderr)
        return "FRIENDSHIP_LEVEL_0"
    if check_friendship_iscode(friendship_str):
        return friendship_str
    conv = {
        'no': 0,
        'good': 1,
        'great': 2,
        'ultra': 3,
        'best': 4
    }
    friendship_str = friendship_str.lower()
    intstrs = [val for key,val in conv.items() if key in friendship_str]
    intstr = str(intstrs[0]) if intstrs else '0'
    return f"FRIENDSHIP_LEVEL_{intstr}"


def parse_friendship_code2str(friendship_code):
    """
    Parse friendship value from code name (e.g. "FRIENDSHIP_LEVEL_4")
    to natural word (e.g. "Best Friend").

    :param friendship_code: Friendship in Pokebattler code name,
        in the form of "FRIENDSHIP_LEVEL_<x>" where x is 0,1,2,3 or 4
    :return: Friendship in natural language,
        in the form of "<x> Friend" where x is "No", "Good", "Great", "Ultra" or "Best"
    """
    if not check_friendship_isstr(friendship_code) and not check_friendship_iscode(friendship_code):
        print(f"Warning (parse_friendship_code2str): Friendship string {friendship_code} is invalid", file=sys.stderr)
        return "FRIENDSHIP_LEVEL_0"
    if check_friendship_isstr(friendship_code):
        return friendship_code
    conv = {
        0: 'No',
        1: 'Good',
        2: 'Great',
        3: 'Ultra',
        4: 'Best'
    }
    intstr = friendship_code[-1]
    return conv[int(intstr)] + " Friend"


def check_type_isstr(pkm_type):
    """
    Check if a given string for Pokemon type is natural language (e.g. "dragon").

    :param pkm_type: Type string to be checked.
    :return: Whether the string is natural language.
    """
    return pkm_type.lower() in [x.lower() for x in POKEMON_TYPES]


def check_type_iscode(pkm_type):
    """
    Check if a given string for Pokemon type is Pokebattler code name (e.g. "POKEMON_TYPE_DRAGON").

    :param pkm_type: Type string to be checked.
    :return: Whether the string is code name.
    """
    return pkm_type.lower() in [f"pokemon_type_{x.lower()}" for x in POKEMON_TYPES]


def parse_type_str2code(type_str):
    """
    Parse Pokemon type value from natural word (e.g. "dragon")
    to code name (e.g. "POKEMON_TYPE_DRAGON").

    :param type_str: Pokemon type in natural language.
    :return: Pokemon type in Pokebattler code name,
        in the form of "POKEMON_TYPE_<x>".
    """
    if not check_type_isstr(type_str) and not check_type_iscode(type_str):
        print(f"Warning (parse_type_str2code): Pokemon type string {type_str} is invalid", file=sys.stderr)
        return "POKEMON_TYPE_NORMAL"
    if check_type_iscode(type_str):
        return type_str
    return f"POKEMON_TYPE_{type_str.upper()}"


def parse_type_code2str(type_code):
    """
    Parse Pokemon type value from code name (e.g. "POKEMON_TYPE_DRAGON")
    to natural word (e.g. "Dragon").

    :param type_code: Pokemon type in Pokebattler code name,
        in the form of "POKEMON_TYPE_<x>".
    :return: Pokemon type in natural language, e.g. "Dragon".
    """
    if not check_type_isstr(type_code) and not check_type_iscode(type_code):
        print(f"Warning (parse_type_code2str): Pokemon type string {type_code} is invalid", file=sys.stderr)
        return "Normal"
    if check_type_isstr(type_code):
        return type_code
    return type_code.split("_")[-1].capitalize()
