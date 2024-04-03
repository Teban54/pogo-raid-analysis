from metadata import *
from config import *
from config_parser import *
from counters_list import *


async def main():
    META = Metadata()
    await META.init(init_from_pokebattler=True, init_from_JSON=False,
                    init_from_GM=True)

    META.debug_print_moves_to_csv()
    META.debug_print_pokemon_to_csv()
    META.debug_print_raids_to_csv()

    # for CONFIG_SORT_OPTION in CONFIG_SORT_OPTIONS:
    #     CONFIG = Config(metadata=META,
    #                     config_attacker_criteria=CONFIG_ATTACKER_CRITERIA,
    #                     config_raid_ensemble=CONFIG_RAID_BOSS_ENSEMBLE,
    #                     config_battle_settings=CONFIG_BATTLE_SETTINGS,
    #                     config_sort_option=CONFIG_SORT_OPTION,
    #                     config_scaling_settings=CONFIG_ESTIMATOR_SCALING_SETTINGS,
    #                     config_processing_settings=CONFIG_PROCESSING_SETTINGS)
    #
    #     # --- Comments below were debug statements, newest to oldest.
    #
    #     CONFIG.raid_ensemble.debug_print_to_csv()
    #
    #     clre = CountersListsRE(
    #         metadata=META,
    #         ensemble=CONFIG.raid_ensemble,
    #         attacker_criteria_multi=CONFIG.attacker_criteria_multi,
    #         scaling_settings=CONFIG.scaling_settings,
    #         processing_settings=CONFIG.processing_settings,
    #         sort_option=CONFIG.sort_option
    #     )
    #     await clre.load_and_process_all_lists()
    #     # clre.write_CSV_list(path=COUNTERS_DATA_PATH, raw=False,
    #     #                     best_attacker_moveset=False, random_boss_moveset=True, specific_boss_moveset=True)
    #     # clre.write_CSV_list(path=COUNTERS_DATA_PATH, raw=True,
    #     #                     best_attacker_moveset=False, random_boss_moveset=True, specific_boss_moveset=True)
    #     clre.temp_write_table(path=COUNTERS_DATA_PATH)


if __name__ == "__main__":
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
