import json
import requests
import csv
import os

from get_json import *
from utils import *

# from regis.utilities import *
"""
Pokemon names:
Too lazy to write fuzzy match... So here are some pokemon name examples:
- None shadow none mega pokemon: "Lucario", "Entei";
- Shadow pokemon: "Arcanine Shadow Form", "Machamp Shadow Form",
- Mega pokemon: "Houndoom Mega", "Charizard Mega Y"
- Random notes: 
    - Ho-oh - "Ho Oh"/"Ho Oh Shadow Form" (I replaced "_" with " " D: )
    - Darmanitan - "Darmanitan Galarian Standard Form" (Not sure about other form lol)

Random functions:
1. Download data:
download_data(raid_level="MEGA", pkm_level=40, raid_type="RAID_LEVEL_MEGA_LEGACY")
raid_type: RAID_LEVEL_X_LEGACY, RAID_LEVEL_X, RAID_X_FUTURE (X could be: 1, 3, 5, MEGA)

2. Pokebattler json to csv: 
Example: (./example/Registeel.csv)
pokebattler_file_to_csv(filename='./level_40/legacy_T5_raid/REGISTEEL_no_weather.json')

3. Pokemon ranking in raids:
Example: 
Export Rhyperior, Rampardos, Tyranitar Shadow Form in all raids (./example/rock_type_pokemon.csv)
```
pokemon_names = ["Rhyperior", "Rampardos", "Tyranitar Shadow Form"]
export_pokemons_ranking_as_csv(pokemon_names=pokemon_names, filename="rock_type_pokemon.csv")
```
"""






def format_str(pb_str):
    """
    Format pokemon name/move id. Example: DRAGON_TAIL_FAST -> Dragon Tail
    :param str pb_str: string from pokebattler, like this: DRAGON_TAIL_FAST
    """
    if (pb_str.endswith('_FAST')):
        pb_str = pb_str[:pb_str.index('_FAST')]
    pb_str = map(str.capitalize, pb_str.split('_'))
    pb_str = ' '.join(pb_str)
    return pb_str


def sort_random_move_data(data, shadow=True, mega=True, pkm_num=None):
    """
    Extract the rankings pokemon_names_list.json when the raid boss uses random moves from the overall JSON results.
    This function is needed because Pokebattler lists the random move rankings
    separately from move-specific rankings.

    :param dict data: pokebattler json file
    """
    random_move = data["attackers"][0]["randomMove"]
    result = {
        'fast_move': 'Random',
        'charged_move': 'Random',
        'ranking': sort_rankings_list_by_move(random_move['defenders'], shadow, mega, pkm_num=None)
    }
    return result


def sort_data_by_move(data, shadow=True, mega=True, pkm_num=None):
    """
    Extract the rankings pokemon_names_list.json from the overall JSON results.
    Sort raid data for each raid boss move with all attacker moves.
    Include both random and specific boss movesets.

    :param dict data: pokebattler json file. 
    :return: a pokemon_names_list.json of dicts.
    """
    raid_moves = data["attackers"][0]["byMove"]
    results = []
    for moves in raid_moves:
        raid_boss_fast_move = format_str(moves["move1"])
        raid_boss_charged_move = format_str(moves["move2"])
        result = {
            'fast_move': raid_boss_fast_move,
            'charged_move': raid_boss_charged_move,
            'ranking': sort_rankings_list_by_move(moves["defenders"], shadow, mega, pkm_num=None)
            }
        results.append(result)
    results.append(sort_random_move_data(data, shadow=shadow, mega=mega, pkm_num=None))
    return results


def sort_rankings_list_by_move(data, shadow=True, mega=True, pkm_num=None):
    """
    Sort an individual rankings pokemon_names_list.json by estimator, reformat to readable form,
    and retain only valid attributes (see example).

    :param str data: Rankings pokemon_names_list.json from the json file from pokebattler.
    :param bool shadow: if True, include shadow pokemon.
    :param bool mega: if True, include mega pokemon.
    :param int pkm_num: Number of Pokemon to be included in the pokemon_names_list.json.
    :return: Make a new pokemon_names_list.json of dicts like:
        {'name': 'PORYGON_Z_SHADOW_FORM', 
         'move1': 'tricky room', 
         'move2': 'recover',
         'estimator': 200,
         'effectiveDeaths': 0, # It a polygon2 with recover!
         'totalCombatTime': 83083}
        (Each attacker can have several entries with different moves)
    """
    results = []
    for defender in data:
        pkm_name = defender["pokemonId"]
        if ((not shadow) and pkm_name.endswith("_SHADOW_FORM")):
            continue
        if ((not mega) and ("_MEGA") in pkm_name):
            continue

        for moveset in defender["byMove"]:
            result = {
              'name': format_str(pkm_name),
              'move1': format_str(moveset['move1']),
              'move2': format_str(moveset['move2']),
              'estimator': moveset['result']['estimator'],
              'effectiveDeaths': moveset['result']['effectiveDeaths'],
              'effectiveCombatTime': moveset['result']['effectiveCombatTime']
            }
            results.append(result)
    results = sorted(results, key=lambda d: d['estimator'])
    return results[0:pkm_num] if (pkm_num) else results


def get_best_moveset(data):
    """
    Get the best moveset of an attacker in a raid.

    :param data: JSON block describing this attacker against a specific raid:
        {"pokemonId":"HYDREIGON",
         "byMove": [a pokemon_names_list.json] ..."
    :return: Best moveset for a raid counter with estimator/effective deaths/effective combat time.
    """
    pkm_name = format_str(data['pokemonId'])
    best_moveset = min(data['byMove'], key=lambda x: x['result']['estimator'])
    result = {
        'name': pkm_name,
        'move1': format_str(best_moveset['move1']),
        'move2': format_str(best_moveset['move2']),
        'estimator': best_moveset['result']['estimator'],
        'effectiveDeaths': best_moveset['result']['effectiveDeaths'],
        'effectiveCombatTime': best_moveset['result']['effectiveCombatTime']
    }
    return result


def sort_by_pkm(data, shadow=True, mega=True, pkm_num=None):
    """
    Extract the rankings pokemon_names_list.json from the overall JSON results.
    Sort raid data for raid boss move, but only keep the best moveset for each defender.
    Includes both random and specific boss movesets.

    :param data: json file from pokebattler
    :param int pkm_num: output pokemon number, default is all. 
    :pokemon_names_list.json return:
    """
    results = []
    # random_move = data["attackers"][0]["randomMove"]
    for raid_boss_moveset in [*data["attackers"][0]["byMove"], *[data["attackers"][0]["randomMove"]]]:
        ranking = []
        for pkm in raid_boss_moveset['defenders']:
            if ((not shadow) and pkm['pokemonId'].endswith("_SHADOW_FORM")):
                continue
            if ((not mega) and ('_MEGA' in pkm['pokemonId'])):
                continue
            ranking.append(get_best_moveset(pkm))
            ranking = sorted(ranking, key=lambda d: d['estimator'])
        result = {
            'fast_move': format_str(raid_boss_moveset['move1']),
            'charged_move': format_str(raid_boss_moveset['move2']),
            'ranking': ranking[:pkm_num] if pkm_num else ranking
        }
        results.append(result)
    return results


def export_as_csv(data,
                  filename='export.csv',
                  shadow=True, mega=True,
                  export_data_by_move=True,
                  highlight_pkm=[]):
    """
    Parse the Pokebattler JSON data and write to a CSV file.
    :param data: Pokebattler data,
    :param filename: csv name,
    :param bool shadow: True if export shadow pokemon,
    :param bool mega: True if export mega pokemon,
    :param bool export_data_by_move: 
                True: export data with all raid counters' possible movesets. 
                False: export best moveset of raid counters
    ### :param int export_pkm_num: pokemon/pokemon moveset number.
    :param list highlight_pkm: Export pokemon in highlight pokemon pokemon_names_list.json only.
                If empty, all Pokemon are exported.
    """
    if export_data_by_move:
        dataset = sort_data_by_move(data, shadow=shadow, mega=mega)
    else:
        dataset = sort_by_pkm(data, shadow=shadow, mega=mega)
    with open(filename, mode='a+') as csv_file:
        fieldnames = ['Rank', 'Raidboss', 'raid_move1', 'raid_move2',
                      'defender_name', 'defender_move1', 'defender_move2',
                      'estimator', 'effective_deaths', 'effective_combat_time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if os.path.getsize(filename) == 0:
            writer.writeheader()
        for moveset in dataset:  # dataset is already extracted and sorted
            fast_move = moveset['fast_move']  #format_str(moveset['fast_move'])
            charged_move = moveset['charged_move']  #format_str(moveset['charged_move'])
            for atker_index, atker_data in enumerate(moveset['ranking']):
                if (len(highlight_pkm) == 0) or \
                        atker_data['name'] in highlight_pkm:
                        # Case sensitive, might need to write another func to match pokemon lol
                    writer.writerow({
                        'Rank': atker_index+1,
                        'Raidboss': format_str(data['attackers'][0]['pokemonId']),
                        'raid_move1': fast_move,
                        'raid_move2': charged_move,
                        'defender_name': atker_data['name'],
                        'defender_move1': atker_data['move1'],
                        'defender_move2': atker_data['move2'],
                        'estimator': atker_data['estimator'],
                        'effective_deaths': atker_data['effectiveDeaths'],
                        'effective_combat_time': atker_data['effectiveCombatTime']
                    })


def find_pokemon_ranking(dir_path='.',
                         filename='export.csv',
                         shadow=True, mega=True,
                         export_data_by_move=True,
                         highlight_pkm=[]):
    """
    Almost the same with `export_as_csv` lol
    """
    filenames = os.listdir(dir_path)
    for f in filenames:
        if not (f.endswith('.json')):
            continue
        with open(dir_path+f, 'r') as fin:
            data = json.load(fin)
        export_as_csv(data, shadow=shadow, mega=mega,
                      filename=filename,
                      export_data_by_move=export_data_by_move,
                      highlight_pkm=highlight_pkm)


def format_print(result):
    # Random function for test.
    print("pokemon name | Fast move | Charged move | estimator | time")
    for pkm in result:
        print(f"{pkm['name']} | {pkm['move1']} | {pkm['move2']} | {pkm['estimator']} | {pkm['effectiveCombatTime']/1000}")








def export_pokemons_ranking_as_csv(pokemon_names, filename="raid.csv"):
    """
    Find rankings against all T5 and mega bosses,
    and write the results in CSV files, one for each boss.

    :param pokemon_names: List of attackers to be considered.
                    If None, all attackers will be included.
    :param filename: Name of the output CSV file.
    """
    keywords = ['future_mega', 'legacy_mega', 'future_T5', 'legacy_T5']
    for keyword in keywords:
        find_pokemon_ranking(dir_path=f"level_40/{keyword}_raid/",
                        export_data_by_move=False,
                        filename=filename,
                        highlight_pkm=pokemon_names)


def pokebattler_file_to_csv(filename, shadow=True, mega=True,
                            fout='filename.csv',
                            export_data_by_move=False):
    """
    Yet another function similar to export_as_csv.
    :param shadow:
    :param mega:
    :param fout: Output file name
    :param export_data_by_move: 
    """
    with open(filename, 'r') as fin:
        data = json.load(fin)
    export_as_csv(data, shadow=shadow, mega=mega,
                      filename=fout,
                      export_data_by_move=export_data_by_move,
                      highlight_pkm=[])


if __name__ == "__main__":



    """
    data = get_pokemon_data("RAYQUAZA", raid_level=5, pkm_level=35, 
                            friendship='no friend', weather='NO_WEATHER')
    """


    """data = get_pokebattler_raid_ranking("KYOGRE", raid_level=5, pkm_level=40,
                                        friendship='best friend', weather='NO_WEATHER',
                                        attack_strategy='dodge specials',
                                        mega=False)
    with open("test.json", "w") as fout:
        json.dump(data, fout)


    #
    with open('test.json', 'r') as f:
        data = json.load(f)
    export_as_csv(data, export_data_by_move=True)
                    #gighlight_pkm=["Darmanitan Galarian Standard Form"])
    """

    """
    download_data(raid_type="RAID_LEVEL_5_LEGACY")
    pokemon_names = ["Rhyperior", "Rampardos", "Tyranitar Shadow Form"]
    export_pokemons_ranking_as_csv(pokemon_names=pokemon_names, filename="rock_type_pokemon_TEST.csv")
    """
