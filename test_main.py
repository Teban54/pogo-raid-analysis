from metadata import *
from config import *
from config_parser import *
from counters_list import *

if __name__ == "__main__":
    META = Metadata(init_from_pokebattler=True, init_from_JSON=False,
                    init_from_GM=True)

    META.debug_print_moves_to_csv()
    META.debug_print_pokemon_to_csv()
    META.debug_print_raids_to_csv()

    CONFIG = Config(metadata=META, config_raid_ensemble=CONFIG_RAID_BOSS_ENSEMBLE,
                    config_battle_settings=CONFIG_BATTLE_SETTINGS)

    # --- Comments below were  debug statements, newest to oldest.

    cl = CountersList(raid_boss_codename="KYOGRE", raid_tier="Tier 5", metadata=META,
                      attacker_level=40, battle_settings=CONFIG.battle_settings)
    #print(cl.rankings)
    cl.write_CSV_list(path=COUNTERS_DATA_PATH, best_attacker_moveset=True,
                       random_boss_moveset=True, specific_boss_moveset=True)