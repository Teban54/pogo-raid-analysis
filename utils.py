"""
Generic utilities functions.

This module does not involve any Pokemon, RaidBoss or Move objects.
Utilities involving these objects can be found in the respective modules.
However, utilities dealing with their names can often be found here.
"""
import json
import requests
import os
import sys
import re
import numpy as np

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


def is_attack_strategy_str(attack_strategy):
    """
    Check if a given string for attack strategy is natural language (e.g. "no dodging").

    :param attack_strategy: Attack strategy string to be checked.
    :return: Whether the string is natural language.
    """
    return any(x in attack_strategy.lower() for x in ['no', 'special', 'all']) and '_' not in attack_strategy


def is_attack_strategy_code(attack_strategy):
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
    if not is_attack_strategy_str(attack_strategy_str) and not is_attack_strategy_code(attack_strategy_str):
        print(f"Warning (parse_attack_strategy_str2code): Attack strategy string {attack_strategy_str} is invalid",
              file=sys.stderr)
        return "CINEMATIC_ATTACK_WHEN_POSSIBLE"
    if is_attack_strategy_code(attack_strategy_str):
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
    if not is_attack_strategy_str(attack_strategy_code) and not is_attack_strategy_code(attack_strategy_code):
        print(f"Warning (parse_attack_strategy_code2str): Attack strategy string {attack_strategy_code} is invalid",
              file=sys.stderr)
        return "No Dodging"
    if is_attack_strategy_str(attack_strategy_code):
        return attack_strategy_code
    conv = {
        "CINEMATIC_ATTACK_WHEN_POSSIBLE": "No Dodging",
        "DODGE_SPECIALS": "Dodge Specials PRO",
        "DODGE_WEAVE_CAUTIOUS": "Dodge All Weave"
    }
    return conv.get(attack_strategy_code.upper(), "No Dodging")


def is_dodge_strategy_str(dodge_strategy):
    """
    Check if a given string for dodge strategy is natural language (e.g. "realistic dodging").

    :param dodge_strategy: Dodge strategy string to be checked.
    :return: Whether the string is natural language.
    """
    return any(x in dodge_strategy.lower() for x in ['perfect', 'realistic', '25']) and '_' not in dodge_strategy


def is_dodge_strategy_code(dodge_strategy):
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
    if not is_dodge_strategy_str(dodge_strategy_str) and not is_dodge_strategy_code(dodge_strategy_str):
        print(f"Warning (parse_dodge_strategy_str2code): Dodge strategy string {dodge_strategy_str} is invalid",
              file=sys.stderr)
        return "DODGE_REACTION_TIME"
    if is_dodge_strategy_code(dodge_strategy_str):
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
    if not is_dodge_strategy_str(dodge_strategy_code) and not is_dodge_strategy_code(dodge_strategy_code):
        print(f"Warning (parse_dodge_strategy_code2str): Dodge strategy string {dodge_strategy_code} is invalid",
              file=sys.stderr)
        return "Realistic Dodging"
    if is_dodge_strategy_str(dodge_strategy_code):
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


def is_friendship_str(friendship):
    """
    Check if a given string for friendship is natural language (e.g. "best friend").

    :param friendship: Friendship string to be checked.
    :return: Whether the string is natural language.
    """
    return any(x in friendship.lower() for x in ['no', 'good', 'great', 'ultra', 'best'])


def is_friendship_code(friendship):
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
    if not is_friendship_str(friendship_str) and not is_friendship_code(friendship_str):
        print(f"Warning (parse_friendship_str2code): Friendship string {friendship_str} is invalid", file=sys.stderr)
        return "FRIENDSHIP_LEVEL_0"
    if is_friendship_code(friendship_str):
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
    if not is_friendship_str(friendship_code) and not is_friendship_code(friendship_code):
        print(f"Warning (parse_friendship_code2str): Friendship string {friendship_code} is invalid", file=sys.stderr)
        return "FRIENDSHIP_LEVEL_0"
    if is_friendship_str(friendship_code):
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


def is_type_str(pkm_type):
    """
    Check if a given string for Pokemon type is natural language (e.g. "dragon").

    :param pkm_type: Type string to be checked.
    :return: Whether the string is natural language.
    """
    return pkm_type.lower() in [x.lower() for x in POKEMON_TYPES]


def is_type_code(pkm_type):
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
    if not is_type_str(type_str) and not is_type_code(type_str):
        print(f"Warning (parse_type_str2code): Pokemon type string {type_str} is invalid", file=sys.stderr)
        return "POKEMON_TYPE_NORMAL"
    if is_type_code(type_str):
        return type_str
    return f"POKEMON_TYPE_{type_str.upper()}"


def parse_type_code2str(type_code):
    """
    Parse Pokemon type value from code name (e.g. "POKEMON_TYPE_DRAGON")
    to natural word (e.g. "Dragon").
    If a natural word ("dragon") is passed in, simply reformat it.

    :param type_code: Pokemon type in Pokebattler code name,
        in the form of "POKEMON_TYPE_<x>".
    :return: Pokemon type in natural language, e.g. "Dragon".
    """
    if not is_type_str(type_code) and not is_type_code(type_code):
        print(f"Warning (parse_type_code2str): Pokemon type string {type_code} is invalid", file=sys.stderr)
        return "Normal"
    if is_type_str(type_code):
        return type_code.capitalize()  # Reformat input
    return type_code.split("_")[-1].capitalize()


def parse_type_strs2inds(type_strs):
    """
    Given a list of Pokemon types as natural language (e.g. "dragon"),
    return a list of their indices in the POKEMON_TYPES list (e.g. 14).
    :param type_strs: List of Pokemon types in natural language, or a single type
    :return: List of indices, or None if any element of the list is not a Pokemon type
    """
    if type(type_strs) is not list:
        type_strs = [type_strs]
    # Convert possible code names to natural strings, and capitalize them
    if not all((type(s) is int and 0 <= s < len(POKEMON_TYPES)
                or type(s) is str and (is_type_str(s) or is_type_code(s)))
               for s in type_strs):
        print(f"Warning (parse_type_strs2inds): Some strings in {type_strs} are invalid", file=sys.stderr)
        return None
    type_strs = [parse_type_code2str(s).capitalize() for s in type_strs]
    return [POKEMON_TYPES.index(s) for s in type_strs]


def parse_type_inds2strs(type_inds):
    """
    Given a list of Pokemon types as indices (e.g. 14),
    return a list of their names as natural language (e.g. "Dragon").
    :param type_inds: List of Pokemon types as indices
    :return: List of type names, or None if any element of the list is not a valid index
    """
    # Convert possible code names to natural strings, and capitalize them
    if not all((type(id) is int and 0 <= id < len(POKEMON_TYPES)) for id in type_inds):
        print(f"Warning (parse_type_inds2strs): Some indices in {type_inds} are invalid", file=sys.stderr)
        return None
    return [POKEMON_TYPES[id] for id in type_inds]


def trim_raid_tier_str(tier):
    """
    Remove the word "Tier" from raid tier or category in natural language, and convert it to lower case.
    E.g. "Tier 5" becomes "5"; "Mega Tier" becomes "mega".
    This is typically for comparisons.
    :param tier: Raid tier or category string in natural language.
    :return: Trimmed string.
    """
    str = tier.lower().replace('tier', '').strip()
    # Remove double spaces (e.g. "Legacy Tier 5")
    return re.sub(' +', ' ', str)


def is_raid_tier_str(tier):
    """
    Check if a given string for raid tier is natural language (e.g. "tier 5" or "5").

    :param tier: Raid tier string to be checked.
    :return: Whether the string is natural language.
    """
    return any(trim_raid_tier_str(x) == trim_raid_tier_str(tier)
               for x in RAID_TIERS_CODE2STR.values())


def is_raid_tier_code(tier):
    """
    Check if a given string for raid tier is Pokebattler code name (e.g. "RAID_LEVEL_5").

    :param tier: Raid tier string to be checked.
    :return: Whether the string is code name.
    """
    return tier in RAID_TIERS_CODE2STR.keys()


def parse_raid_tier_str2code(tier_str):
    """
    Parse raid tier from natural language (e.g. "tier 5") to code name (e.g. "RAID_LEVEL_5").

    If no matches are found, return RAID_LEVEL_<trimmed tier string, upper case, with _>.
    (Some tolerance of possible new tiers that may be added to Pokebattler, but not perfect.)

    :param tier_str: Raid tier in natural language, as a string. Can be with or without the word "tier".
        E.g. "Tier 5", "5", "Mega Tier", "Tier Mega", "Mega" are all fine.
        Do not accept integers. Do not accept words other than "tier".
    :return: Raid tier in Pokebattler code name, in form of "RAID_LEVEL_<x>".
    """
    if not is_raid_tier_str(tier_str) and not is_raid_tier_code(tier_str):
        print(f"Warning (parse_raid_tier_str2code): Raid tier string {tier_str} is invalid",
              file=sys.stderr)
        # Tolerance (see above)
        return "RAID_LEVEL_" + trim_raid_tier_str(tier_str).upper().replace(" ", "_").replace(".", "_")
    if is_raid_tier_code(tier_str):
        return tier_str
    tier_str = trim_raid_tier_str(tier_str)
    codes = [key for key, val in RAID_TIERS_CODE2STR.items() if trim_raid_tier_str(val) == tier_str]
    return codes[0] if codes else "RAID_LEVEL_5"


def parse_raid_tier_code2str(tier_code):
    """
    Parse raid tier from code name (e.g. "RAID_LEVEL_5") to natural language (e.g. "Tier 5").
    If a natural word ("5") is passed in, simply reformat it.

    If no matches are found, return the ORIGINAL CODE NAME.
    (Tolerance of possible new tiers that may be added to Pokebattler.)

    :param tier_code: Raid tier in Pokebattler code name, in form of "RAID_LEVEL_<x>".
    :return: Raid tier in natural language, as a well-formatted string with word "Tier".
        E.g. "Tier 5", "Mega Tier".
    """
    if not is_raid_tier_str(tier_code) and not is_raid_tier_code(tier_code):
        print(f"Warning (parse_raid_tier_code2str): Raid tier code name {tier_code} is invalid",
              file=sys.stderr)
        return tier_code  # Tolerance (see above)!!!
    if is_raid_tier_str(tier_code):
        # Reformat
        tier_str = trim_raid_tier_str(tier_code)
        strs = [val for key, val in RAID_TIERS_CODE2STR.items() if trim_raid_tier_str(val) == tier_str]
        return strs[0] if strs else "Tier 5"
    strs = [val for key, val in RAID_TIERS_CODE2STR.items() if key.lower() == tier_code.lower()]
    return strs[0] if strs else "Tier 5"


def is_raid_category_str(category):
    """
    Check if a given string for raid category is natural language (e.g. "tier 5" or "5").

    :param category: Raid category string to be checked.
    :return: Whether the string is natural language.
    """
    return any(trim_raid_tier_str(x) == trim_raid_tier_str(category)
               for x in RAID_CATEGORIES_CODE2STR.values())


def is_raid_category_code(category):
    """
    Check if a given string for raid category is Pokebattler code name (e.g. "RAID_LEVEL_5").

    :param category: Raid category string to be checked.
    :return: Whether the string is code name.
    """
    return category in RAID_CATEGORIES_CODE2STR.keys()


def parse_raid_category_str2code(category_str):
    """
    Parse raid category from natural language (e.g. "legacy tier 5") to code name (e.g. "RAID_LEVEL_5_LEGACY").

    If no matches are found, return RAID_LEVEL_<trimmed tier string, upper case, with _>.
    (Some tolerance of possible new tiers that may be added to Pokebattler, but not perfect.)

    :param category_str: Raid category in natural language, as a string. Can be with or without the word "tier".
        E.g. "Tier 5", "5", "Mega Tier", "Tier Mega", "Mega" are all fine.
        Do not accept integers. Do not accept words other than "tier".
    :return: Raid category in Pokebattler code name, in form of "RAID_LEVEL_<x>".
    """
    if not is_raid_category_str(category_str) and not is_raid_category_code(category_str):
        print(f"Warning (parse_raid_category_str2code): Raid category string {category_str} is invalid",
              file=sys.stderr)
        # Tolerance (see above)
        return "RAID_LEVEL_" + trim_raid_tier_str(category_str).upper().replace(" ", "_").replace(".", "_")
    if is_raid_category_code(category_str):
        return category_str
    category_str = trim_raid_tier_str(category_str)
    codes = [key for key, val in RAID_CATEGORIES_CODE2STR.items() if trim_raid_tier_str(val) == category_str]
    return codes[0] if codes else "RAID_LEVEL_5"


def parse_raid_category_code2str(category_code):
    """
    Parse raid category from code name (e.g. "RAID_LEVEL_5_LEGACY") to natural language (e.g. "Legacy Tier 5").
    If a natural word ("5") is passed in, simply reformat it.

    If no matches are found, return the ORIGINAL CODE NAME.
    (Tolerance of possible new tiers that may be added to Pokebattler.)

    :param category_code: Raid category in Pokebattler code name, in form of "RAID_LEVEL_<x>".
    :return: Raid category in natural language, as a well-formatted string with word "Tier".
        E.g. "Legacy Tier 5", "Future Mega Tier".
    """
    if not is_raid_category_str(category_code) and not is_raid_category_code(category_code):
        print(f"Warning (parse_raid_category_code2str): Raid tier code name {category_code} is invalid",
              file=sys.stderr)
        return category_code  # Tolerance (see above)!!!
    if is_raid_category_str(category_code):
        # Reformat
        category_str = trim_raid_tier_str(category_code)
        strs = [val for key, val in RAID_CATEGORIES_CODE2STR.items() if trim_raid_tier_str(val) == category_str]
        return strs[0] if strs else "Tier 5"
    strs = [val for key, val in RAID_CATEGORIES_CODE2STR.items() if key.lower() == category_code.lower()]
    return strs[0] if strs else "Tier 5"


# ----------------- Type Effectiveness -----------------


def get_effectiveness_single_defender(type_strs):
    """
    Get the type effectiveness table for a single defender with possibly multiple types.
    :param type_strs: List of defender's types in natural language, or defender's only type as a single string
    :return: List of type effectiveness values with length 18, corresponding to attacking types.
            A value of 1 means this attacking type is super effective to the given defender,
            2 means double effective, 0 means neutral, -1 means resisted, -2 means double resisted, etc.
            Returns None if any element in the input is invalid.
    """
    if type(type_strs) is str:  # Mono type
        type_strs = [type_strs]
    type_inds = parse_type_strs2inds(type_strs)
    if type_inds is None:
        return None
    eff_table_def_types = [TYPE_EFFECTIVENESS_TRANSPOSE[id] for id in type_inds]
    # ^ Each element is a list of length 18, for each defending type
    ret_array = np.sum(np.array(eff_table_def_types), 0)  # Sum over types
    return list(ret_array)


def get_weaknesses(type_strs):
    """
    Get all single and double weaknesses for a single defender with possibly multiple types.
    :param type_strs: List of defender's types in natural language, or defender's only type as a single string
    :return: Dict as following:
        {'DOUBLE_WEAKNESSES': ['Ground', ...],
         'SINGLE_WEAKNESSES': ['Water', ...]}
    """
    eff_list = get_effectiveness_single_defender(type_strs)
    if not eff_list:  # Error
        return None
    double_inds = [i for i, val in enumerate(eff_list) if val == 2]
    single_inds = [i for i, val in enumerate(eff_list) if val == 1]
    return {
        'DOUBLE_WEAKNESSES': parse_type_inds2strs(double_inds),
        'SINGLE_WEAKNESSES': parse_type_inds2strs(single_inds)
    }


def get_attack_effectiveness(attack_type, defend_types):
    """
    Check the effectiveness of an attacking type against a single defender with possibly multiple types.
    :param attack_type: Name of attacking type in natural language, e.g. "dragon"
    :param defend_types: List of defender's types in natural language, or defender's only type as a single string
    :return: Effectiveness of this attack as a single value.
            A value of 1 means this attacking type is super effective to the given defender,
            2 means double effective, 0 means neutral, -1 means resisted, -2 means double resisted, etc.
            Returns None if any element in the input is invalid.
    """
    attack_inds = parse_type_strs2inds([attack_type])
    defend_inds = parse_type_strs2inds(defend_types)
    if not attack_inds or not defend_inds:
        return None
    attack_ind = attack_inds[0]
    return sum(TYPE_EFFECTIVENESS[attack_ind][id] for id in defend_inds)


def get_contender_types(defend_types):
    """
    Find all "contender types" against a single defender with possibly multiple types.
    "Contender type" is defined as:
    - If the defender has double weakness(es): Its double weaknesses are the only contender types.
    - If the defender has single weakness(es) but no double weaknesses: Its single weaknesses are the only contender types.
    - If the defender has no weaknesses: Types that are not resisted are the only contender types.
        (Impossible as of Gen 8)

    :param defend_types: List of defender's types in natural language, or defender's only type as a single string
    :return: List of all contender types in natural language.
            Returns None in case of errors.
    """
    weaknesses = get_weaknesses(defend_types)
    if weaknesses is None:
        return None
    if weaknesses.get('DOUBLE_WEAKNESSES', []):
        return weaknesses['DOUBLE_WEAKNESSES']
    if weaknesses.get('SINGLE_WEAKNESSES', []):
        return weaknesses['SINGLE_WEAKNESSES']
    # Defender has no weaknesses  (This part of code has not been tested yet)
    eff_table = get_effectiveness_single_defender(defend_types)
    neutral_ids = [i for i, val in enumerate(eff_table) if val == 0]
    return parse_type_inds2strs(neutral_ids)


def is_contender_type(attack_type, defend_types):
    """
    Check if an attacking type is a "contender type" against a single defender with possibly multiple types.
    "Contender type" is defined as:
    - If the defender has double weakness(es): Its double weaknesses are the only contender types.
    - If the defender has single weakness(es) but no double weaknesses: Its single weaknesses are the only contender types.
    - If the defender has no weaknesses: Types that are not resisted are the only contender types.
        (Impossible as of Gen 8)
    For definition of "contender type", see docs for get_contender_types.

    :param attack_type: Name of attacking type in natural language, e.g. "dragon"
    :param defend_types: List of defender's types in natural language, or defender's only type as a single string
    :return: Whether the attacking type is a contender type.
    """
    attack_type = parse_type_code2str(attack_type)
    return attack_type in get_contender_types(defend_types)


# ----------------- Moves -----------------


def parse_move_code2str(move_code):
    """
    Parse move name from code name (e.g. "SMACK_DOWN_FAST") to natural language (e.g. "Smack Down").
    Does not check whether the name is valid.

    :param move_code: Move in Pokebattler code name, possibly including "_FAST".
    :return: Move name in natural language.
    """
    if move_code in SPECIAL_MOVE_DISPLAY_NAMES:
        return SPECIAL_MOVE_DISPLAY_NAMES[move_code]
    if "_FAST" in move_code:
        move_code = move_code.replace("_FAST", "")
    return codename_to_displayname(move_code)

