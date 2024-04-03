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
from battle_settings import *


async def get_pokebattler_metadata(metadata_name, write_file=False):
    """
    Get the Pokebattler metadata JSON files (moves, Pokemon, raids).
    The files are obtained from https://fight-beta.pokebattler.com/<metadata_name>.
    More info: https://www.reddit.com/r/pokebattler/comments/b876tq/pokebattler_api_usage_instructions/

    :param metadata_name: Name of the metadata file to be obtained.
            Should be one of "moves", "pokemon" or "raids".
    :param write_file: If True, the file will be written to cache location:
            data/json/<metadata_name>.json
    :return: Requested JSON data as Python object
    """
    data = await do_http_request(f"{POKEBATTLER_SERVER}{metadata_name}")
    if write_file:
        write_json_to_file(data, f"data/json/{metadata_name}.json")
    return data


async def get_pokebattler_raid_counters(raid_boss=None, raid_boss_codename=None, raid_tier="Tier 5",
                                  attacker_level=40, trainer_id=None,
                                  attacker_criteria_multi=None,
                                  battle_settings=None,
                                  sort_option="Estimator"):
    """
    Get the list of best attackers from Pokebattler and return it as JSON.

    :param raid_boss: RaidBoss object.
    :param str raid_boss_codename: Code name of the raid boss (e.g. "LANDORUS_THERIAN_FORM"),
            if a RaidBoss object is not provided.
    :param int raid_tier: Raid tier, either as natural language or code name.
    :param int attacker_level: Attacker level.
    :param int trainer_id: Pokebattler Trainer ID if a trainer's own Pokebox is used.
            If None, use all attackers by level.
    :param attacker_criteria_multi: AttackerCriteriaMulti object describing attackers to be used.
            This will be used for shadow/mega/legendary toggles, Pokemon types and Trainer ID.
    :param battle_settings: BattleSettings object, including friendship, weather, and attack/dodge strategies.
            Must be for a single set of settings.
    :param sort_option: Sorting option for Pokebattler counters list.
    :return: Pokebattler ranking results parsed as JSON, or an error string or None if applicable
    """
    # TODO: Add sanity check for attacker criteria
    if not battle_settings:
        print(f"Warning (get_pokebattler_raid_counters): BattleSettings not found. Using default settings.",
              file=sys.stderr)
        battle_settings = BattleSettings()
    if battle_settings.is_multiple():
        print(f"Warning (get_pokebattler_raid_counters): BattleSettings includes multiple settings. Using the first set.",
              file=sys.stderr)
        battle_settings = battle_settings.indiv_settings[0]

    attacker_types = attacker_criteria_multi.pokebattler_pokemon_types()
    payload = {
        "sort": parse_sort_option_str2code(sort_option),
        "weatherCondition": battle_settings.weather_code,
        "dodgeStrategy": battle_settings.dodge_strategy_code,
        "aggregation": "AVERAGE",
        "includeLegendary": attacker_criteria_multi.pokebattler_legendary(),
        "includeShadow": attacker_criteria_multi.pokebattler_shadow(),
        "includeMegas": attacker_criteria_multi.pokebattler_mega(),
        "randomAssistants": "-1",
        # "primalAssistants": "KYOGRE_PRIMAL",  # TEMPORARY_PRIMAL (another edit below)
        "friendLevel": battle_settings.friendship_code,
        "attackerTypes": "POKEMON_TYPE_ALL" if not attacker_types else attacker_types  # ["POKEMON_TYPE_ICE","POKEMON_TYPE_FIRE"]
    }
    if raid_boss:
        raid_boss_codename = raid_boss.pokemon_codename
        raid_tier = raid_boss.tier

    # url with API key:
    # https://www.pokebattler.com/raids/defenders/HEATRAN/levels/
    # RAID_LEVEL_5/attackers/users/757345/strategies/
    # CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC
    # ?sort=ESTIMATOR
    # &weatherCondition=CLEAR&dodgeStrategy=DODGE_REACTION_TIME&aggregation=AVERAGE
    # &includeMegas=true&randomAssistants=-1&numMegas=0#raid-estimator
    if trainer_id:
        url = f'{POKEBATTLER_SERVER}raids/defenders/{raid_boss_codename}/' \
              f'levels/{raid_tier}/attackers/users/{trainer_id}/' \
              f'strategies/{battle_settings.attack_strategy_code}/DEFENSE_RANDOM_MC'
    else:
        url = f'{POKEBATTLER_SERVER}raids/defenders/{raid_boss_codename}/' \
              f'levels/{raid_tier}/attackers/levels/{attacker_level}/' \
              f'strategies/{battle_settings.attack_strategy_code}/DEFENSE_RANDOM_MC'

    # aiohttp doesn't allow payload with True/False values, so convert to string
    for k, v in payload.items():
        if type(v) is bool:
            payload[k] = str(v)

    # print(url)
    # print(payload)
    return await do_http_request(url, payload)


async def get_pokebattler_single_battle(attacker=None, attacker_codename=None,
                                        attacker_fast_move=None, attacker_charged_move=None, attacker_ivs="15\\15\\15",
                                        raid_boss=None, raid_boss_codename=None, raid_tier="Tier 5",
                                        raid_boss_fast_move="RANDOM", raid_boss_charged_move="RANDOM",
                                        attacker_level=40,
                                        battle_settings=None,
                                        include_details=False):
    """
    Get the simulation results of a single attacker against a single raid boss and return it as JSON.

    :param attacker: Pokemon object.
    :param str attacker_codename: Code name of the attacker (e.g. "LANDORUS_THERIAN_FORM"),
            if an attacker Pokemon object is not provided.
    :param str attacker_fast_move: Fast move code name, e.g. "MUD_SLAP_FAST".
    :param str attacker_charged_move: Charged move code name, e.g. "EARTH_POWER".
    :param str attacker_ivs: IVs of the attacker, in "atk\\def\\hp" format.
    :param raid_boss: RaidBoss object.
    :param str raid_boss_codename: Code name of the raid boss (e.g. "LANDORUS_THERIAN_FORM"),
            if a RaidBoss object is not provided.
    :param int raid_tier: Raid tier, either as natural language or code name.
    :param str raid_boss_fast_move: Fast move code name, or "RANDOM".
    :param str raid_boss_charged_move: Charged move code name, or "RANDOM".
    :param int attacker_level: Attacker level.
    :param battle_settings: BattleSettings object, including friendship, weather, and attack/dodge strategies.
            Must be for a single set of settings.
    :param include_details: Whether details about each time step of the fight is included.
    :return: Pokebattler ranking results parsed as JSON, or an error string or None if applicable
    """
    # TODO: Add sanity check for attacker criteria
    if not battle_settings:
        print(f"Warning (get_pokebattler_raid_counters): BattleSettings not found. Using default settings.",
              file=sys.stderr)
        battle_settings = BattleSettings()
    if battle_settings.is_multiple():
        print(f"Warning (get_pokebattler_raid_counters): BattleSettings includes multiple settings. Using the first set.",
              file=sys.stderr)
        battle_settings = battle_settings.indiv_settings[0]

    # Parse IVs from my format (15/15/15) to Pokebattler format (FFF)
    ivs = [int(x) for x in attacker_ivs.split('\\')]
    ivs_pokebattler = '{}{}{}'.format(
        chr(ord('A') + ivs[0] - 10) if ivs[0] >= 10 else str(ivs[0]),
        chr(ord('A') + ivs[1] - 10) if ivs[1] >= 10 else str(ivs[1]),
        chr(ord('A') + ivs[2] - 10) if ivs[2] >= 10 else str(ivs[2]),
    )

    #attacker_types = attacker_criteria_multi.pokebattler_pokemon_types()
    payload = {
        #"sort": parse_sort_option_str2code(sort_option),
        "weatherCondition": battle_settings.weather_code,
        "dodgeStrategy": battle_settings.dodge_strategy_code,
        #"aggregation": "AVERAGE",
        #"includeLegendary": attacker_criteria_multi.pokebattler_legendary(),
        #"includeShadow": attacker_criteria_multi.pokebattler_shadow(),
        #"includeMegas": attacker_criteria_multi.pokebattler_mega(),
        "randomAssistants": "-1",
        # "primalAssistants": "KYOGRE_PRIMAL",  # TEMPORARY_PRIMAL (another edit above)
        "friendLevel": battle_settings.friendship_code,
        #"attackerTypes": "POKEMON_TYPE_ALL" if not attacker_types else attacker_types  # ["POKEMON_TYPE_ICE","POKEMON_TYPE_FIRE"]
        "includeDetails": include_details,
        "numMegas": 0,
        "monteCarlo": "DEFENSE_RANDOM_MC",
        "seed": 1660095119751,
    }
    if raid_boss:
        raid_boss_codename = raid_boss.pokemon_codename
        raid_tier = raid_boss.tier
    if attacker:
        attacker_codename = attacker.name

    # url with API key:
    # https://www.pokebattler.com/fights/attackers/KANGASKHAN_MEGA/
    # quickMoves/MUD_SLAP_FAST/cinMoves/EARTHQUAKE,MOVE_NONE/
    # levels/39.0/ivs/FFF/
    # defenders/NIHILEGO/quickMoves/RANDOM/cinMoves/RANDOM,MOVE_NONE/
    # levels/RAID_LEVEL_ULTRA_BEAST/
    # strategies/CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC
    # ?includeDetails=true&dodgeStrategy=DODGE_REACTION_TIME&weatherCondition=NO_WEATHER
    # &randomAssistants=-1&numMegas=0&monteCarlo=DEFENSE_RANDOM_MC&seed=1660095119751

    # if trainer_id:
    #     url = f'https://fight-beta.pokebattler.com/raids/defenders/{raid_boss_codename}/' \
    #           f'levels/{raid_tier}/attackers/users/{trainer_id}/' \
    #           f'strategies/{battle_settings.attack_strategy_code}/DEFENSE_RANDOM_MC'
    # else:
    url = f'{POKEBATTLER_SERVER}fights/attackers/{attacker_codename}/' \
          f'quickMoves/{attacker_fast_move}/cinMoves/{attacker_charged_move},MOVE_NONE/' \
          f'levels/{attacker_level}/ivs/{ivs_pokebattler}/' \
          f'defenders/{raid_boss_codename}/' \
          f'quickMoves/{raid_boss_fast_move}/cinMoves/{raid_boss_charged_move}/' \
          f'levels/{raid_tier}/' \
          f'strategies/{battle_settings.attack_strategy_code}/DEFENSE_RANDOM_MC'

    # aiohttp doesn't allow payload with True/False values, so convert to string
    for k, v in payload.items():
        if type(v) is bool:
            payload[k] = str(v)

    return await do_http_request(url, payload)


async def get_json_main():
    for metadata_name in ["raids", "pokemon", "moves"]:
        await get_pokebattler_metadata(metadata_name, write_file=True)


if __name__ == "__main__":
    asyncio.run(get_json_main())