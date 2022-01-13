"""
Functions for retrieving JSON data from Pokebattler.

The data is returned as a Python object.
If needed, they can be written to a JSON file using write_json_to_file.
Some funtions also has a built-in option to write to a fixed cache location.

These functions do not parse the JSON files.
"""

import json
import requests
import os

from utils import *


def get_pokebattler_metadata(metadata_name, write_file=False):
    """
    Get the Pokebattler metadata JSON files (moves, Pokemon, raids).
    The files are obtained from https://fight.pokebattler.com/<metadata_name>.
    More info: https://www.reddit.com/r/pokebattler/comments/b876tq/pokebattler_api_usage_instructions/

    :param metadata_name: Name of the metadata file to be obtained.
            Should be one of "moves", "pokemon" or "raids".
    :param write_file: If True, the file will be written to cache location:
            data/json/<metadata_name>.json
    :return: Requested JSON data as Python object
    """
    data = do_http_request(f"https://fight.pokebattler.com/{metadata_name}")
    if write_file:
        write_json_to_file(data, f"data/json/{metadata_name}.json")
    return data


def get_pokebattler_raid_ranking(raid_boss, raid_level=5, pkm_level=40,
                                 friendship='Best Friend', weather='NO_WEATHER',
                                 legendary=True, shadow=True, mega=True,
                                 trainer_id=None,
                                 attack_strategy='No Dodging', dodge_strategy='Realistic Dodging'):
    """
    Get the pokemon_names_list.json of best attackers from Pokebattler and return it as JSON.
    Sorted by Estimator.

    :param str raid_boss: Code name of the raid boss (e.g. "LANDORUS_THERIAN_FORM").
    :param int raid_level: Raid boss level, 6 or MEGA for mega raids.
    :param int pkm_level: Attackerl evel.
    :param int friendship: Friendship level, either as natural language or code name.
            Default is best friend.
    :param str weather: weather, default is NO_WEATHER
            weather could be: CLEAR, RAINY, PARTLY_CLOUDY, CLOUDY, WINDY, SNOW, FOG
    :param legendary: If True, include Legendary Pokemon.
    :param shadow: If True, include Shadow Pokemon.
    :param mega: If True, include Mega Evolutions.
    :param int trainer_id: Pokebattler Trainer ID if a trainer's own Pokebox is used.
            If None, use all attackers by level.
    :param attack_strategy: Attack strategy, i.e. dodge or not.
            Should be one of: "No Dodging", "Dodge Specials PRO", "Dodge All Weave".
    :param dodge_strategy: Dodge strategy, i.e. accuracy of dodging.
            Should be one of: "Perfect Dodging", "Realistic Dodging", "Realistic Dodging Pro", "25% Dodging".
    :return: Pokebattler ranking results parsed as JSON, or an error string or None if applicable
    """
    payload = {
        "sort": "ESTIMATOR",  # TODO: Set this arbitrarily
        "weatherCondition": weather,
        "dodgeStrategy": parse_dodge_strategy_str2code(dodge_strategy),
        "aggregation": "AVERAGE",
        "includeLegendary": legendary,
        "includeShadow": shadow,
        "includeMegas": mega,
        "randomAssistants": "-1",
        "friendLevel": parse_friendship_str2code(friendship),
        "attackerTypes": "POKEMON_TYPE_ALL"  # ["POKEMON_TYPE_ICE","POKEMON_TYPE_FIRE"]
    }
    if raid_level == 6:
        raid_level = "MEGA"

    # url with API key:
    # https://www.pokebattler.com/raids/defenders/HEATRAN/levels/
    # RAID_LEVEL_5/attackers/users/757345/strategies/
    # CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC
    # ?sort=ESTIMATOR
    # &weatherCondition=CLEAR&dodgeStrategy=DODGE_REACTION_TIME&aggregation=AVERAGE
    # &includeMegas=true&randomAssistants=-1&numMegas=0#raid-estimator
    if trainer_id:
        url = f'https://fight.pokebattler.com/raids/defenders/{raid_boss}/' \
              f'levels/RAID_LEVEL_{raid_level}/attackers/users/{trainer_id}/' \
              f'strategies/{parse_attack_strategy_str2code(attack_strategy)}/DEFENSE_RANDOM_MC'
    else:
        url = f'https://fight.pokebattler.com/raids/defenders/{raid_boss}/' \
              f'levels/RAID_LEVEL_{raid_level}/attackers/levels/{pkm_level}/' \
              f'strategies/{parse_attack_strategy_str2code(attack_strategy)}/DEFENSE_RANDOM_MC'
    return do_http_request(url, payload)


# TODO: Consolidate everything below


def load_raid_info(filename='raids.json', raid_type="RAID_LEVEL_5_LEGACY"):
    """
    Extract all raid bosses of a certain tier listed in raids.json from Pokebattler.
    This pokemon_names_list.json can be used later to get simulations against all raid bosses.

    :param filename: Filename of raids information
    :param raid_type: Raid types
        Future raid: "RAID_LEVEL_5_FUTURE" / "RAID_LEVEL_MEGA_FUTURE"
        Legacy raid: "RAID_LEVEL_5_LEGACY" / "RAID_LEVEL_MEGA_LEGACY"
        Current raid: "RAID_LEVEL_5" / "RAID_LEVEL_MEGA"
    """
    data = load_json_from_file(filename)
    # data:
    result = []
    for tier in data['tiers']:
        if tier['tier'] == raid_type:
            raids = tier['raids']
    for raid in raids:
        result.append(raid['pokemon'])
    return result


def download_data(raid_level=5, pkm_level=40, trainer_id=None, raid_type='RAID_LEVEL_5'):
    """
    Download the rankings lists of all raids of a certain tier from Pokebattler.
    Writes them to JSON files.

    :param raid_level: Raid tier, in integer (to setup the simulations)
    :param pkm_level: Level of Pokemon used
    :param trainer_id: ID of user whose Pokebox will be used for simulations.
                    If None, all attackers by level will be used.
    :param raid_type: Raid types
        Future raid: "RAID_LEVEL_5_FUTURE" / "RAID_LEVEL_MEGA_FUTURE"
        Legacy raid: "RAID_LEVEL_5_LEGACY" / "RAID_LEVEL_MEGA_LEGACY"
        Current raid: "RAID_LEVEL_5" / "RAID_LEVEL_MEGA"
    """
    #
    pokemon_list = load_raid_info(raid_type=raid_type)
    print(f"{len(pokemon_list)} Pokemon found. Downloading data. ")
    for pkm in pokemon_list:
        try:
            if (trainer_id):
                data = get_pokebattler_raid_ranking(raid_boss=pkm,
                                                    raid_level=raid_type,
                                                    pkm_level=pkm_level,
                                                    trainer_id=trainer_id)
            else:
                data = get_pokebattler_raid_ranking(raid_boss=pkm,
                                                    raid_level=raid_type,
                                                    pkm_level=pkm_level)
        except Exception as e:
            print(e)
        if (data):
            print(f"Downloading {pkm} data. ")
            filename = f"{pkm}_no_weather.json"
            with open(filename, 'w') as fout:
                json.dump(data, fout)


#def play(**kwargs):
#    print(kwargs.get("qwe", 3))

if __name__ == "__main__":
    for metadata_name in ["raids", "pokemon", "moves"]:
        get_pokebattler_metadata(metadata_name, write_file=True)