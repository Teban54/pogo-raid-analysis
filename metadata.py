"""
Module for processing and storing Pokebattler metadata,
including raids, Pokemon and moves.
"""
import csv

from utils import *
from get_json import *
from pokemon import *
from raid_boss import *
from move import *
from raid_ensemble import *
from config import *
from config_parser import *


class Metadata:
    """
    Metadata object that's used in all modules.
    Stores the original Pokebattler JSON files, as well as processed data (e.g. list of Pokemon).
    """
    def __init__(self, init_from_pokebattler=True, init_from_JSON=False, init_from_GM=True):
        """
        Initialize the Metadata.
        Prioritizes initialization from Pokebattler, and if it fails, initialize from local JSON.

        :param init_from_pokebattler: If True, initialize with current JSON from Pokebattler
        :param init_from_JSON: If True, initialize with local JSON from data/json/, but
                only if init_from_pokebattler is False or initialization
        :param init_from_GM: If True, also load local GM data from data/json/latest.json,
                which would be used to complement the Pokebattler data
        """
        self.raids_JSON = None
        self.Pokemon_JSON = None
        self.moves_JSON = None
        self.GM_JSON = None

        self.moves = {}  # Lookup by code name: {"SMACK_DOWN_FAST": <Move object>, ...}
        self.fast_moves = []
        self.charged_moves = []

        self.Pokedex = {}  # Lookup by code name: {"BULBASAUR_SHADOW_FORM": <Pokemon object>, ...}

        self.raids = []  # May be unnecessary?
        self.raids_by_category = {}  # {"RAID_LEVEL_5_LEGACY": [list of RaidBoss objects], ...}
        self.raids_by_tier = {}  # {"RAID_LEVEL_5": [list of RaidBoss objects, current, legacy, future], ...}
        self.raid_categories_by_tier = {}  # {"RAID_LEVEL_5": set("RAID_LEVEL_5_LEGACY", ...), ...}

        if init_from_pokebattler:
            self.raids_JSON = get_pokebattler_metadata("raids", write_file=False)
            self.Pokemon_JSON = get_pokebattler_metadata("pokemon", write_file=False)
            self.moves_JSON = get_pokebattler_metadata("moves", write_file=False)
        if self.raids_JSON is None:
            if init_from_JSON:
                # TODO: Add a warning if local JSON is too old
                self.raids_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "raids.json"))
            if self.raids_JSON is None:
                print(f"Warning (Metadata.__init__): Loading raids JSON failed", file=sys.stderr)
        if self.Pokemon_JSON is None:
            if init_from_JSON:
                self.Pokemon_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "pokemon.json"))
            if self.Pokemon_JSON is None:
                print(f"Warning (Metadata.__init__): Loading Pokemon JSON failed", file=sys.stderr)
        if self.moves_JSON is None:
            if init_from_JSON:
                self.moves_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "moves.json"))
            if self.moves_JSON is None:
                print(f"Warning (Metadata.__init__): Loading moves JSON failed", file=sys.stderr)

        self.load_moves()

        self.load_pokedex()

        if init_from_GM:
            self.GM_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "latest.json"))
            self.load_pokedex_from_GM()

        self.load_raids()

    # ----------------- Moves -----------------

    def load_moves(self):
        """
        Process the Move JSON file and fill the lists of moves with Move objects.
        """
        for move_json in self.moves_JSON['move']:
            if 'moveId' not in move_json or move_json['moveId'] in IGNORED_MOVES:
                continue
            move = Move(pokebattler_JSON=move_json)
            move_codename = move.name
            if move_codename in self.moves:
                print(f"Warning (Metadata.load_moves): Duplicate move with code name {move_codename}",
                    file=sys.stderr)
            else:
                self.moves[move_codename] = move
            if move.is_fast:
                self.fast_moves.append(move)
            else:
                self.charged_moves.append(move)

    def find_move(self, codename):  # TODO(maybe): Make it support natural names too
        """
        Find a move with a given code name.
        :param codename: Pokebattler code name of move (e.g. SMACK_DOWN_FAST)
        :return: Move object
        """
        if codename and codename in self.moves:
            return self.moves[codename]
        #print(f"Error (Metadata.find_pokemon): Pokemon {codename} not found", file=sys.stderr)
        return None

    def find_moves(self, codenames):
        """
        Find all moves with given code names.
        Strictly match the code names (e.g. searching HIDDEN_POWER_FAST will not return Hidden Powers of specific types).
        :param codenames: Pokebattler code names of moves as list
        :return: List of Move objects
        """
        lst = [self.find_move(name) for name in codenames]
        return [move for move in lst if move is not None]

    def debug_print_moves_to_csv(self, filename="data/metadata/moves.csv"):
        """
        Debug function that outputs all moves to CSV.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Code name', 'Display name', 'Type', 'Is fast', 'Power', 'Energy delta',
                          'Duration', 'Window start', 'Window end']
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for move_codename, move in self.moves.items():
                writer.writerow([
                    move.name, move.displayname, move.type, move.is_fast, move.power, move.energy_delta,
                    move.duration, move.window_start, move.window_end
                ])

    # ----------------- Pokedex -----------------

    def load_pokedex(self):
        """
        Process the Pokemon JSON file and fill the Pokedex in meta data with Pokemon objects.
        """
        for pkm_json in self.Pokemon_JSON['pokemon']:
            pkm = Pokemon(pokebattler_JSON=pkm_json, metadata=self)
            pkm_codename = pkm.name
            if pkm_codename in self.Pokedex:
                print(f"Warning (Metadata.load_pokedex): Duplicate Pokemon with code name {pkm_codename}",
                    file=sys.stderr)
            else:
                self.Pokedex[pkm_codename] = pkm

    def load_pokedex_from_GM(self):
        """
        Process the GM JSON file and add additional information to the current Pokedex
        (which should have been filled with Pokebattler data).
        Currently, the main purpose of this is to add evolution lines to the Pokedex.

        Note: Megas are ignored in this process, as they have separate entries only in Pokebattler, not in GM.
        """
        for item in self.GM_JSON:
            # First, filter out items that describe Pokemon
            gm_codename = GM_templateId_to_pokemon_codename(item['templateId'])
            if not gm_codename:
                continue
            obsolete = (
                gm_codename.endswith('_NORMAL')  # This is primarily a remnant of past shadow-eligible Pokemon,
                                                  # which used to have "_NORMAL", "_SHADOW" and "_PURIFIED" forms.
                                                  # It does erronously remove some Pokemon with a Normal form (e.g. Arceus),
                                                  # But those forms don't seem to exist in Pokebattler anyway.
                or gm_codename.endswith('_HOME_FORM_REVERSION') or gm_codename.endswith('_HOME_REVERSION')
            )
            if obsolete:
                continue
            pkm_data = item['data']
            pb_codename = gm_codename
            pkm_obj = self.find_pokemon(codename=pb_codename)
            if not pkm_obj:
                pb_codename = gm_codename + "_FORM"
                pkm_obj = self.find_pokemon(codename=pb_codename)
            if not pkm_obj:  # This is for Nidoran and Giratina-A
                pb_codename = pkm_data['pokemonSettings']['pokemonId']
                pkm_obj = self.find_pokemon(codename=pb_codename)

            if pkm_obj:
                pkm_obj.init_from_GM(pkm_data)
                pkm_shadow = self.find_pokemon(codename=pb_codename+"_SHADOW_FORM")
                if pkm_shadow:
                    pkm_shadow.init_from_GM(pkm_data, shadow=True)
        # Currently, after all this, any megas and NIDORAM_SHADOW FORM (pb codenames) have no corresponding GM data.
        # But that's ok.
        # Also, the following evolutions listed do not actually exist:
        """
        Evolution not found: SYLVEON_SHADOW_FORM
        Evolution not found: WORMADAM_PLANT_FORM_SHADOW_FORM
        Evolution not found: CHERRIM_OVERCAST_FORM_SHADOW_FORM
        Evolution not found: CHERRIM_SUNNY_FORM_SHADOW_FORM
        Evolution not found: GASTRODON_EAST_SEA_FORM_SHADOW_FORM
        Evolution not found: DARMANITAN_STANDARD_FORM_SHADOW_FORM
        """
        # However, none of them are actually in Pokebattler's data yet.

    def find_pokemon(self, codename):  # TODO: Make it support natural names too
        """
        Find a Pokemon with a given code name.
        :param codename: Pokebattler code name of Pokemon (e.g. BULBASAUR_SHADOW_FORM)
        :return: Pokemon object
        """
        if codename and codename in self.Pokedex:
            return self.Pokedex[codename]
        #print(f"Error (Metadata.find_pokemon): Pokemon {codename} not found", file=sys.stderr)
        return None

    def get_all_pokemon(self, remove_ignored=True):
        """
        Get a list of all Pokemon.
        :param remove_ignored: If True, Pokemon and forms that should be ignored
            (including cosmetic forms) will not be included.
        :return: All Pokemon as a list of Pokemon objects
        """
        lst = list(self.Pokedex.values())
        if remove_ignored:
            lst = remove_pokemon_to_ignore(lst)
        return lst

    def debug_print_pokemon_to_csv(self, filename="data/metadata/pokemon.csv"):
        """
        Debug function that outputs all Pokemon to CSV.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Code name', 'Type 1', 'Type 2', 'Attack', 'Defense', 'Stamina',
                          'Pre-evolution', 'Evolutions', 'Is legendary', 'Is mythical', 'Is shadow', 'Is mega',
                          'Base code name', 'Base display name',
                          'Form code name', 'Form display name', 'Mega code name', 'Mega display name',
                          'Display name', 'Fast moves', 'Charged moves']
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for pkm_codename, pkm in self.Pokedex.items():
                writer.writerow([
                    pkm.name, pkm.type, pkm.type2, pkm.base_attack, pkm.base_defense, pkm.base_stamina,
                    pkm.pre_evo, pkm.evolutions, pkm.is_legendary, pkm.is_mythical, pkm.is_shadow, pkm.is_mega,
                    pkm.base_codename, pkm.base_displayname, pkm.form_codename, pkm.form_displayname,
                    pkm.mega_codename, pkm.mega_displayname, pkm.displayname,
                    pkm.fast_moves, pkm.charged_moves
                ])

    def debug_lookup_GM(self, keyword):
        """
        Debug function that prints all terms in GM with a given keyword.
        """
        for item in self.GM_JSON:
            if keyword.lower() in item.get('templateId', '').lower():
                print(item)

    # ----------------- Raids -----------------

    def load_raids(self):
        """
        Process the Raid JSON file and fill the lists of raid bosses with RaidBoss objects.
        Should only be called after the Pokedex is loaded!
        """
        for category_JSON in self.raids_JSON['tiers']:
            category = category_JSON['tier']  # Code name, "RAID_LEVEL_5_LEGACY"
            tier = category_JSON['info']['guessTier']  # Code name, "RAID_LEVEL_5"
            if category == 'RAID_LEVEL_UNSET':
                # Important! Skip this.
                # It's basically a list of all Pokemon.
                # Contains obsolete data such as BLASTOISE_NOEVOLVE_FORM and MEWTWO_A_INTRO_FORM.
                continue

            if category not in self.raids_by_category:
                self.raids_by_category[category] = []
            if tier not in self.raids_by_tier:
                self.raids_by_tier[tier] = []
            if tier not in self.raid_categories_by_tier:
                self.raid_categories_by_tier[tier] = set()
            self.raid_categories_by_tier[tier].add(category)

            for boss_JSON in category_JSON['raids']:
                boss = RaidBoss(pokebattler_JSON=boss_JSON, tier_codename=tier, category_codename=category,
                                metadata=self)
                self.raids.append(boss)
                self.raids_by_category[category].append(boss)
                self.raids_by_tier[tier].append(boss)

    def get_raid_bosses_by_tier(self, tier, remove_ignored=True):
        """
        Get all raid bosses of a certain raid tier (e.g. Tier 5) recorded on Pokebattler.
        :param tier: Raid tier, either as natural language or code name
        :param remove_ignored: If True, raids that should be ignored will not be included.
        :return: List of RaidBoss objects describing all bosses of that tier
        """
        lst = self.raids_by_tier.get(parse_raid_tier_str2code(tier), [])
        if remove_ignored:
            lst = remove_raids_to_ignore(lst)
        return lst

    def get_raid_bosses_by_category(self, category, remove_ignored=True):
        """
        Get all raid bosses of a certain raid category (e.g. Legacy Tier 5) recorded on Pokebattler.
        :param category: Raid category, either as natural language or code name
        :param remove_ignored: If True, raids that should be ignored will not be included.
        :return: List of RaidBoss objects describing all bosses of that category
        """
        lst =  self.raids_by_category.get(parse_raid_category_str2code(category), [])
        if remove_ignored:
            lst = remove_raids_to_ignore(lst)
        return lst

    def debug_print_raids_to_csv(self, filename="data/metadata/raids.csv"):
        """
        Debug function that outputs all raids (RaidBoss objects) to CSV.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Tier', 'Category', 'Pokemon codename', 'Base', 'Form', 'Is mega']
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for boss in self.raids:
                writer.writerow([
                    parse_raid_tier_code2str(boss.tier),
                    boss.category,
                    boss.pokemon_codename, boss.pokemon_base,
                    boss.pokemon_form if boss.pokemon_form else '',
                    boss.is_mega
                ])


if __name__ == "__main__":
    META = Metadata(init_from_pokebattler=True, init_from_JSON=False,
                    init_from_GM=True)

    META.debug_print_moves_to_csv()
    META.debug_print_pokemon_to_csv()
    META.debug_print_raids_to_csv()

    CONFIG = Config(metadata=META, config_raid_ensemble=CONFIG_RAID_BOSS_ENSEMBLE,
                    config_battle_settings=CONFIG_BATTLE_SETTINGS)

    # --- Comments below were newer debug statements, newest to oldest.
    # I'm too lazy to revert the old ones lol

    """CONFIG.raid_ensemble.debug_print_to_csv()
    CONFIG.battle_settings.debug_print()"""

    # --- Comments below were old debug statements, oldest to newest.

    #print([pkm['pokemonId'] for pkm in META.Pokemon_JSON['pokemon']])
    #print(META.Pokemon_JSON['pokemon'][9])
    #print(META.find_pokemon('GOLEM').JSON)

    #for pkm_codename, pkm in META.Pokedex.items():
    #    print(pkm_codename, pkm.evolutions)
    #print(META.find_pokemon("VENUSAUR_SHADOW_FORM").JSON)
    """
    for pkm_codename, pkm in META.Pokedex.items():
        print(pkm.JSON['pokedex']['pokemonId'], '\t\t', pkm_codename, '\t\t', pkm.JSON['pokedex'].get('form', "---"),
              '\t\t', pkm.JSON.get('form', "---"))
    """

    #META.debug_lookup_GM("piloswine")

    """
    bosses = META.get_raid_bosses_by_tier("Tier 5")
    for boss in bosses:
        print(boss.pokemon.displayname)
    print('--------')
    bosses = META.get_raid_bosses_by_category("Legacy Tier 5")
    for boss in bosses:
        print(boss.pokemon.displayname)
    """

    """
    pkms = META.get_all_pokemon(remove_ignored=True)
    #pkms = filter_pokemon_by_criteria(pkms, criterion_weak_to_contender_type, attack_type='Water')
    #pkms = filter_pokemon_by_criteria(pkms, criterion_evo_stage, keep_final_stage=False, keep_pre_evo=True)
    #pkms = filter_pokemon_by_criteria(pkms, criterion_shadow_mega, is_shadow=True, is_not_shadow=True,
    #                                  is_mega=True, is_not_mega=False)
    pkms = filter_pokemon_by_criteria(pkms, criterion_legendary_or_mythical, negate=True)
    for pkm in pkms:
        print(pkm.displayname)
    """

    """
    pkms = META.get_all_pokemon(remove_ignored=True)
    dct = group_pokemon_by_basename(pkms, separate_shadows=True, separate_megas=True)
    for key, val in dct.items():
        print(key + ", ", end='')
        for pkm in val:
            print(pkm.displayname + ", ", end='')
        print()
    """

    """
    pkms = META.get_all_pokemon(remove_ignored=True)
    #ensemble = RaidEnsemble(pokemons=pkms, tier='RAID_LEVEL_5', weight_multiplier=3,
    #                        forms_weight_strategy='combine', separate_shadows=True, separate_megas=True)
    ensemble = RaidEnsemble(raid_bosses=[])
    ensemble.extend(RaidEnsemble(raid_bosses=remove_raids_to_ignore(META.get_raid_bosses_by_tier('Tier 5')),
                                 weight_multiplier=5))
    ensemble.extend(RaidEnsemble(raid_bosses=remove_raids_to_ignore(META.get_raid_bosses_by_tier('Mega')),
                                 weight_multiplier=3))
    ensemble.extend(RaidEnsemble(raid_bosses=remove_raids_to_ignore(META.get_raid_bosses_by_tier('Tier 3')),
                                 weight_multiplier=1))
    ensemble = filter_ensemble_by_criteria(ensemble, criterion_pokemon=criterion_weak_to_contender_types,
                                           attack_types=["Ice", "Steel"])
    ensemble.debug_print_to_csv()
    """

