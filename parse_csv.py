import csv 

"""
Output: Pokemon ranking with random raid boss move
@charles: Why don't you use pandas T_T 
"""
def load_file(filename, sort_by="estimator"):
    """
    :param filename: csv filename. 
    :return: Not sure, a list of dicts? Or just dict? 
    {
        "Kyurem": {
            "Tyranitar Shadow Form": 7,
            "Rhyperior": 12,
            "Rampardos": 27
        },
    },

    """
    result = {}
    with open(filename, 'r') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            if (row['raid_move1'] != 'Random') or (row['raid_move2'] != 'Random'):
                continue 
            if (row['Raidboss'] not in result):
                result[row['Raidboss']] = {'Raidboss': row['Raidboss']}
            result[row['Raidboss']][row['defender_name']] = row[sort_by]
            # current_defenders = [raid_boss[0] for raid_boss in result[row['Raidboss']]]
            # result[row['Raidboss']].append([row['defender_name'], row['Rank']])
    return result

def find_all_counters(result):
    """
    Even not sure why this func exists. 
    For generating csv header I believe. 
    """
    res = []
    for raid_boss in result:
        res += list(result[raid_boss].keys())
        res = list(set(res))
    res.remove('Raidboss')
    return res

def write_as_csv(result, fout='test.csv'):
    """
    Another csv! That's really shocked pikachu!!
    """
    headers = ['Raidboss']
    headers += find_all_counters(result)
    with open(fout, 'w', newline='') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for raid_boss in result:
            writer.writerow(result[raid_boss])

def parse_csv(filename, output_file_name='result.csv', sort_by='estimator'):
    """
    :param filename: csv filename. The file from "pokebattler.py"
    :param output_file_name: 
    :param sort_by: Rank, estimator,effective_deaths,effective_combat_time
    """
    result = load_file(filename, sort_by=sort_by)
    write_as_csv(result, fout=output_file_name)

if (__name__ == "__main__"):
    parse_csv("./examples/rock_type_pokemon.csv")