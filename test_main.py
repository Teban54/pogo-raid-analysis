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

    CONFIG = Config(metadata=META,
                    config_attacker_criteria=CONFIG_ATTACKER_CRITERIA,
                    config_raid_ensemble=CONFIG_RAID_BOSS_ENSEMBLE,
                    config_battle_settings=CONFIG_BATTLE_SETTINGS,
                    config_sort_option=CONFIG_SORT_OPTION,
                    config_scaling_settings=CONFIG_ESTIMATOR_SCALING_SETTINGS)

    # --- Comments below were debug statements, newest to oldest.

    #CONFIG.raid_ensemble.debug_print_to_csv()

    clre = CountersListsRE(ensemble=CONFIG.raid_ensemble, attacker_criteria_multi=CONFIG.attacker_criteria_multi,
                           scaling_settings=CONFIG.scaling_settings)
    """clre.load_and_parse_JSON()
    clre.filter_rankings()
    clre.scale_estimators(baseline_boss_moveset="easiest")"""
    clre.load_and_process_all_lists()
    clre.write_CSV_list(path=COUNTERS_DATA_PATH, raw=False,
                        best_attacker_moveset=True, random_boss_moveset=True, specific_boss_moveset=True)
    clre.write_CSV_list(path=COUNTERS_DATA_PATH, raw=True,
                        best_attacker_moveset=True, random_boss_moveset=True, specific_boss_moveset=True)

    """ACM = CONFIG.attacker_criteria_multi
    for AC in ACM.sets:
        print(AC.pokemon_types,AC.fast_types,AC.charged_types,AC.min_level,AC.max_level,
              AC.level_step,AC.pokemon_codenames,AC.trainer_id,AC.is_legendary,AC.is_not_legendary,
              AC.is_mythical,AC.is_not_mythical,AC.is_legendary_or_mythical,AC.is_not_legendary_or_mythical,
              AC.is_shadow,AC.is_not_shadow,AC.is_mega,AC.is_not_mega)
        print(AC.check_attacker(pokemon_codename="ZARUDE",
                                fast_codename="BITE_FAST",
                                charged_codename="GRASS_KNOT",
                                level="40"))
    print(ACM.check_attacker(pokemon_codename="ZARUDE",
                                fast_codename="BITE_FAST",
                                charged_codename="GRASS_KNOT",
                                level="40"))
    print(ACM.all_levels())
    print(ACM.pokebattler_legendary(), ACM.pokebattler_shadow(), ACM.pokebattler_mega())"""

    """cl = CountersList(raid_boss_codename="ALOMOMOLA", raid_tier="Tier 3", metadata=META,
                      attacker_level=40, battle_settings=CONFIG.battle_settings)
    #print(cl.rankings)
    cl.write_CSV_list(path=COUNTERS_DATA_PATH, best_attacker_moveset=True,
                       random_boss_moveset=True, specific_boss_moveset=True)"""
