import json
import requests
import csv
import os

# from regis.utilities import *

def parse_friendship(friendship_str):
    raid_friends = {
        'no': 0,
        'good': 1,
        'great': 2,
        'ultra': 3,
        'best': 4
        }   
    friendship_str = friendship_str.lower()
    result = [val for key,val in raid_friends.items() if key in friendship_str]
    return str(result[0]) if result else '0'

def get_pokemon_data(raid_boss, raid_level=5, pkm_level=35, 
                     friendship='0', weather='NO_WEATHER'):
    """
    :param str raid_boss: 
    :param int raid_level: raid boss level, 6 for mega raids.
    :param int pkm_level: pokemon level.
    :param int friendship: friendship level, default is 4 for best friend,
    :param str weather: weather, default is NO_WEATHER
           weather could be: SUNNY, RAINY, PARTLY_CLOUDY, CLOUDY, WINDY, SNOW, FOG
    :return: pokemon json file or None
    """
    payload = {
        "sort": "TIME",
        "weatherCondition": weather,
        "dodgeStrategy": "DODGE_REACTION_TIME",
        "aggregation": "AVERAGE",
        "includeLegendary": "true",
        "includeShadow": "true",
        "includeMegas": "true",
        "randomAssistants": "-1",
        "friendLevel": f"FRIENDSHIP_LEVEL_{friendship}"
    }
    if raid_level == 6:
        raid_level = "MEGA"

    url = f'https://fight.pokebattler.com/raids/defenders/{raid_boss}/'\
          f'levels/RAID_LEVEL_{raid_level}/attackers/levels/{pkm_level}/'\
            'strategies/CINEMATIC_ATTACK_WHEN_POSSIBLE/DEFENSE_RANDOM_MC'
    try:
        r = requests.get(url, params=payload)
        if r.ok:
            return r.json()
        else:
            return str(r)
    except Exception as e:
        print(e)
        return None

def format_str(pb_str):
    """
    :param str pb_str: string from pokebattler, like this: DRAGON_TAIL_FAST
    """
    if (pb_str.endswith('_FAST')):
        pb_str = pb_str[:pb_str.index('_FAST')]
    pb_str = map(str.capitalize, pb_str.split('_'))
    pb_str = ' '.join(pb_str)
    return pb_str

def sort_random_move_data(data, shadow=True, mega=True, pkm_num=None):
    """
    :param dict data: pokebattler json file
    """
    random_move = data["attackers"][0]["randomMove"]
    result = {
        'fast_move': 'Random',
        'charged_move': 'Random',
        'ranking': sort_by_move(random_move['defenders'], shadow, mega, pkm_num=None)
    }
    return result
  
def sort_data_by_move(data, shadow=True, mega=True, pkm_num=None):
    """
    Sort raid data by raid boss move and defender move. 
    Include moveset: random data. 
    :param dict data: pokebattler json file. 
    :return: a list of dicts. 
    """
    raid_moves = data["attackers"][0]["byMove"]
    results = []
    for moves in raid_moves:
        raid_boss_fast_move = format_str(moves["move1"])
        raid_boss_charged_move = format_str(moves["move2"])
        result = {
            'fast_move': raid_boss_fast_move,
            'charged_move': raid_boss_charged_move,
            'ranking': sort_by_move(moves["defenders"], shadow, mega, pkm_num=None)
            }
        results.append(result)
    results.append(sort_random_move_data(data, shadow=shadow, mega=mega, pkm_num=None))
    return results

def sort_by_move(data, shadow=True, mega=True, pkm_num=None):
    """
    Sort pokemon 
    :param str data: the json file from pokebattler. 
    :param bool shadow: if True, include shadow pokemon.
    :param bool mega: if True, include mega pokemon.
    :param int pkm_num: 
    Make a new list of dict like:
        {'name': 'PORYGON_Z_SHADOW_FORM', 
         'move1': 'tricky room', 
         'move2': 'recover',
         'estimator': 200,
         'effectiveDeaths': 0, # It a polygon2 with recover!
         'totalCombatTime': 83083}
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
    :param data:
        {"pokemonId":"HYDREIGON",
         "byMove": [a list] ..."
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
    Sorted data by pokemon (with the best pokemon move)
    :param data: json file from pokebattler
    :param int pkm_num: output pokemon number, default is all. 
    :list return: 
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
    :param data: Pokebattler data,
    :param filename: csv name,
    :param bool shadow: True if export shadow pokemon,
    :param bool mega: True if export mega pokemon,
    :param bool export_data_by_move: 
                True: export data with all raid counters' possible movesets. 
                False: export best moveset of raid counters
    :param int export_pkm_num: pokemon/pokemon moveset number.
    :param list highlight_pkm: Export pokemon in highlight pokemon list
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
        for moveset in dataset:
            fast_move = format_str(moveset['fast_move'])
            charged_move = format_str(moveset['charged_move'])
            for index_pkm in range(len(moveset['ranking'])):
                if (len(highlight_pkm) == 0) or \
                    moveset['ranking'][index_pkm]['name'] in highlight_pkm:
                    # Case sensitive, might need to write another func to match pokemon lol
                    writer.writerow({
                    'Rank': index_pkm+1,
                    'Raidboss': format_str(data['attackers'][0]['pokemonId']),
                    'raid_move1': fast_move,
                    'raid_move2': charged_move,
                    'defender_name': moveset['ranking'][index_pkm]['name'],
                    'defender_move1': moveset['ranking'][index_pkm]['move1'],
                    'defender_move2': moveset['ranking'][index_pkm]['move2'],
                    'estimator': moveset['ranking'][index_pkm]['estimator'],
                    'effective_deaths': moveset['ranking'][index_pkm]['effectiveDeaths'],
                    'effective_combat_time': moveset['ranking'][index_pkm]['effectiveCombatTime']
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

def load_raid_info(filename='raids.json', raid_type="RAID_LEVEL_5_LEGACY"):
    with open(filename, 'r') as fin:
        data = json.load(fin)
    # data:
    result = []
    for tier in data['tiers']:
        if tier['tier'] == raid_type:
            # Future raid: "RAID_LEVEL_5_FUTURE"
            # Legacy raid: "RAID_LEVEL_5_LEGACY"
            # Current raid: "RAID_LEVEL_5"
            raids = tier['raids']

    for raid in raids:
        result.append(raid['pokemon'])
    return result

def download_data(raid_level=5, pkm_level=40, raid_type='RAID_LEVEL_5'):
    #
    pokemon_list = load_raid_info(raid_type=raid_type)
    print(f"{len(pokemon_list)} Pokemon found. Downloading data. ")
    for pkm in pokemon_list:
        try:
            data = get_pokemon_data(raid_boss=pkm, raid_level=raid_level, pkm_level=pkm_level)
        except Exception as e:
            print(e)
        if (data):
            print(f"Downloading {pkm} data. ")
            filename = f"{pkm}_no_weather.json"
            with open(filename, 'w') as fout:
                json.dump(data, fout)

def pkm_ranking_in_all_raids(pokemon_name):
    keywords = ['future_mega', 'legacy_mega', 'future_T5', 'legacy_T5']
    for keyword in keywords:
        find_pokemon_ranking(dir_path=f"level_40/{keyword}_raid/",
                        export_data_by_move=False,
                        filename=f'{keyword}.csv',
                        highlight_pkm=[pokemon_name])

if (__name__ == "__main__"):
    # Download data:
    # download_data(raid_level="MEGA", pkm_level=40, raid_type="RAID_LEVEL_MEGA")
    # download_data(raid_level="MEGA", pkm_level=40, raid_type="RAID_LEVEL_MEGA_LEGACY")
    # download_data(raid_level="MEGA", pkm_level=40, raid_type="RAID_LEVEL_MEGA_FUTURE")
    pkm_ranking_in_all_raids("Kyurem")
    """
    data = get_pokemon_data("RAYQUAZA", raid_level=5, pkm_level=35, 
                        friendship='0', weather='NO_WEATHER')
    with open("test.json", "w") as fout:
        json.dump(data, fout)
    
    # 
    with open('test.json', 'r') as f:
        data = json.load(f)
    export_as_csv(data, export_data_by_move=False,
                    highlight_pkm=["Darmanitan Galarian Standard Form"])
    """
