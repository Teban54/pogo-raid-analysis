"""
Module for processing and storing Pokebattler metadata,
including raids, Pokemon and moves.
"""
import csv

from utils import *
from get_json import *
from pokemon import Pokemon


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
        self.Pokedex = {}  # Lookup by code name: {"BULBASAUR_SHADOW_FORM": <Pokemon object>, ...}
        self.GM_JSON = None

        if init_from_pokebattler:
            self.raids_JSON = get_pokebattler_metadata("raids", write_file=False)
            self.Pokemon_JSON = get_pokebattler_metadata("pokemon", write_file=False)
            self.moves_JSON = get_pokebattler_metadata("moves", write_file=False)
        if self.raids_JSON is None or self.Pokemon_JSON is None or self.moves_JSON is None:
            if init_from_JSON:
                self.raids_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "raids.json"))
                self.Pokemon_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "pokemon.json"))
                self.moves_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "moves.json"))
        if self.raids_JSON is None or self.Pokemon_JSON is None or self.moves_JSON is None:
            print(f"Warning (Metadata.__init__): Loading JSON failed", file=sys.stderr)

        self.load_pokedex()

        if init_from_GM:
            self.GM_JSON = load_json_from_file(os.path.join(JSON_DATA_PATH, "latest.json"))
            self.load_pokedex_from_GM()

    def load_pokedex(self):
        """
        Process the Pokemon JSON file and fill the Pokedex in meta data with Pokemon objects.
        """
        for pkm_json in self.Pokemon_JSON['pokemon']:
            pkm = Pokemon(pokebattler_JSON=pkm_json)
            pkm_codename = pkm.name
            if pkm_codename in self.Pokedex:
                print(f"Warning (Metadata.load_pokedex): Duplicate Pokemon with code name {pkm_codename}",
                    file=sys.stderr)
            else:
                self.Pokedex[pkm_codename] = pkm

        # Add evolutions (Removed as it fails on forms like shadows and Alolans)
        """
        for pkm_codename, pkm in self.Pokedex.items():
            if pkm.pre_evo:
                pre_evo = self.find_pokemon(codename=pkm.pre_evo)
                pre_evo.evolutions.append(pkm_codename)
        """

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

    def debug_print_pokemon_to_csv(self, filename="data/pokemon.csv"):
        """
        Debug function that outputs all Pokemon to CSV.
        """
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Code name', 'Type 1', 'Type 2', 'Attack', 'Defense', 'Stamina',
                          'Pre-evolution', 'Evolutions', 'Is legendary', 'Is mythical', 'Is shadow', 'Is mega',
                          'Base code name', 'Base display name',
                          'Form code name', 'Form display name', 'Mega code name', 'Mega display name',
                          'Display name']
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for pkm_codename, pkm in self.Pokedex.items():
                writer.writerow([
                    pkm.name, pkm.type, pkm.type2, pkm.base_attack, pkm.base_defense, pkm.base_stamina,
                    pkm.pre_evo, pkm.evolutions, pkm.is_legendary, pkm.is_mythical, pkm.is_shadow, pkm.is_mega,
                    pkm.base_codename, pkm.base_displayname, pkm.form_codename, pkm.form_displayname,
                    pkm.mega_codename, pkm.mega_displayname, pkm.displayname
                ])

    def debug_lookup_GM(self, keyword):
        """
        Debug function that prints all terms in GM with a given keyword.
        """
        for item in self.GM_JSON:
            if keyword.lower() in item.get('templateId', '').lower():
                print(item)


if __name__ == "__main__":
    META = Metadata(init_from_pokebattler=True, init_from_JSON=False,
                    init_from_GM=True)
    #print([pkm['pokemonId'] for pkm in META.Pokemon_JSON['pokemon']])
    #print(META.Pokemon_JSON['pokemon'][9])

    #for pkm_codename, pkm in META.Pokedex.items():
    #    print(pkm_codename, pkm.evolutions)
    #print(META.find_pokemon("VENUSAUR_SHADOW_FORM").JSON)
    """
    for pkm_codename, pkm in META.Pokedex.items():
        print(pkm.JSON['pokedex']['pokemonId'], '\t\t', pkm_codename, '\t\t', pkm.JSON['pokedex'].get('form', "---"),
              '\t\t', pkm.JSON.get('form', "---"))
    """

    META.debug_print_pokemon_to_csv()

    #META.debug_lookup_GM("piloswine")