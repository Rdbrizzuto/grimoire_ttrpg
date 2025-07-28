import json
import os


class Stats:
    def __init__(self, strength, endurance, flexibility, perception, charisma, mana):
        self.strength = strength
        self.endurance = endurance
        self.flexibility = flexibility
        self.perception = perception
        self.charisma = charisma
        self.mana = mana

        # Derived stats
        self.power = self.strength + self.flexibility
        self.constitution = self.strength + self.endurance
        self.speed = self.flexibility + self.endurance

        self.max_health = (self.constitution * 3) + 5
        self.max_mp = self.mana * 3
    

class Ability:
    def __init__(self, name, base_damage, time_cost, mana_cost=0):
        self.name = name
        self.base_damage = base_damage
        self.time_cost = time_cost
        self.mana_cost = mana_cost



class Equipment:
    def __init__(self, name, damage=0, weight=0, armor=0, slot="weapon"):
        self.name = name
        self.damage = damage
        self.weight = weight
        self.armor = armor
        self.slot = slot  # e.g., "weapon", "armor", "accessory"


class Species:
    def __init__(self, name, stats, abilities, starting_equipment):
        self.name = name
        self.stats = stats               # Stats object
        self.abilities = abilities       # List of Ability objects
        self.starting_equipment = starting_equipment  # Dict of Equipment (e.g., {"weapon": ..., "armor": ...})


class Character:
    def __init__(self, name, species, is_player):
        self.name = name
        self.species = species
        self.stats = species.stats
        self.abilities = list(species.abilities)  # copy the list

        self.inventory = []
        self.equiped = dict(species.starting_equipment)  # {"weapon": Equipment(...), "armor": Equipment(...)}
        self.is_player = is_player

        # Combat state
        self.current_health = self.stats.max_health
        self.current_mp = self.stats.max_mp
        self.ready_time = 0

    def is_alive(self):
        return self.current_health > 0
    
    def add_to_inventory(self, item):
        if not isinstance(item, Equipment):
            raise ValueError(f"{item} is not a valid Equipment object.")
        if item in self.inventory:
            print(f"{item.name} is already in inventory.")
            return
        self.inventory.append(item)
        print(f"{self.name} added {item.name} to their inventory.")



    def perform_ability(self, ability, target):
        if ability.mana_cost > self.current_mp:
            print(f"{self.name} doesn't have enough MP to use {ability.name}!")
            return 0, 1  # No damage, 1 second used
        
        self.current_mp = self.current_mp - ability.mana_cost

        weapon = self.equiped.get('weapon')
        weapon_damage = weapon.damage if weapon else 0

        total_damage = ability.base_damage + self.stats.power + weapon_damage
        target.current_health = target.current_health - total_damage

        print(f"{self.name} uses {ability.name} on {target.name} for {total_damage} damage!")
        return total_damage, ability.time_cost


class Action:
    def __init__(self, user, ability, target, current_time):
        self.user = user
        self.ability = ability
        self.target = target
        
        weapon = user.equiped.get('weapon')
        weapon_weight = weapon.weight if weapon else 0

        self.action_speed = user.stats.speed + ability.time_cost + weapon_weight
        self.scheduled_time = current_time + self.action_speed
        

    def execute(self):
        if self.target.is_alive() and self.user.is_alive():
            self.user.perform_ability(self.ability, self.target)
        else:
            print(f"{self.user.name}'s action does nothing.")

    def __lt__(self, other):
        return self.scheduled_time < other.scheduled_time

    

def create_player_characters(species_dict, equipment_dict, ability_dict):
    while True:
            pc_count = input('How many players are there? ')
            try:
                pc_count = int(pc_count)
                if pc_count > 0:
                    break
                else:
                    print('Please enter a valid integer\n')
            except ValueError:
                print('Please enter a valid integer\n')
    
    player_list = []
    
    for _ in range(pc_count):
        name = input('Name: ')

        #Selecting species of player character
        while True:
            species_name = input('Species: ').strip().capitalize()
            if species_name in species_dict:
                species = species_dict[species_name]
                break
            else:
                print("Invalid species. Please enter one of the following:")
                print(", ".join(species_dict.keys()))

        strength = get_stat("Strength: ")
        endurance = get_stat('Endurance: ')
        flexibility = get_stat('Flexibility: ')
        perception = get_stat('Perception: ')
        charisma = get_stat('Charisma: ')
        mana = get_stat('Mana: ')

        pc_stats = Stats(strength, endurance, flexibility, perception, charisma, mana)
        player = Character(name, species, is_player=True)

        player.stats = pc_stats
        player.current_health = player.stats.max_health
        player.current_mp = player.stats.max_mp
        

        player_list.append(player)
    
    return player_list




def get_stat(stat_name):
    while True:
        stat_value = input(f'{stat_name}')
        try:
            stat_value = int(stat_value)
            if 1 <= stat_value <= 20:
                return stat_value
            else:
                print('Please enter an integer from 1 to 20.\n')
        except ValueError:
            print('Please enter an integer from 1 to 20.\n')

def save_game(player_list):
    list_save_files()
    filename = input("Enter a filename to save (e.g., save1.json): ").strip()
    if not filename.endswith(".json"):
        filename += ".json"

    if not os.path.exists("saves"):
        os.makedirs("saves")

    full_path = os.path.join("saves", filename)

    save_data = []
    for player in player_list:
        save_data.append({
            "name": player.name,
            "species": player.species.name,
            "stats": vars(player.stats),
            "current_health": player.current_health,
            "current_mp": player.current_mp,
            "inventory": [item.name for item in player.inventory],
            "equipped": {slot: eq.name for slot, eq in player.equiped.items()},
            "abilities": [ab.name for ab in player.abilities],
        })

    with open(full_path, 'w') as f:
        json.dump(save_data, f, indent=2)
    
    print(f"Game saved to '{full_path}'.")


def load_game(species_dict, equipment_dict, ability_dict):
    list_save_files()
    while True:
        filename = input('Enter the filename to load (or type "q" to cancel): ').strip()
        if filename.lower() == 'q':
            return None
        if not filename.endswith('.json'):
            filename += '.json'

        full_path = os.path.join("saves", filename)

        try:
            with open(full_path, 'r') as f:
                save_data = json.load(f)
                break
        except FileNotFoundError:
            print("File not found.")

    player_list = []

    for pdata in save_data:
        species = species_dict[pdata["species"]]
        stats_data = pdata["stats"]
        stats = Stats(
            stats_data["strength"],
            stats_data["endurance"],
            stats_data["flexibility"],
            stats_data["perception"],
            stats_data["charisma"],
            stats_data["mana"]
        )

        character = Character(pdata["name"], species, is_player=True)
        character.stats = stats
        character.current_health = pdata["current_health"]
        character.current_mp = pdata["current_mp"]

        character.inventory = [
            equipment_dict[item_name]
            for item_name in pdata.get("inventory", [])
            if item_name in equipment_dict
        ]

        character.equiped = {
            slot: equipment_dict[item_name]
            for slot, item_name in pdata.get("equipped", {}).items()
            if item_name in equipment_dict
        }

        character.abilities = [
            ability_dict[ab_name]
            for ab_name in pdata.get("abilities", [])
            if ab_name in ability_dict
        ]

        player_list.append(character)

    print(f"Game loaded from '{filename}'.")
    return player_list


def list_save_files():
    if not os.path.exists("saves"):
        os.makedirs("saves")

    files = [f for f in os.listdir("saves") if f.endswith(".json")]
    
    if not files:
        print("No save files found.")
    else:
        print("Available save files:")
        for f in files:
            print(f"{f}")
    print()


def edit_player_character(player_list, equipment_dict, ability_dict):
    # 1. Choose a character
    print('\nChoose a player character to edit:')
    for i, player in enumerate(player_list, 1):
        print(f'{i}. {player.name}')
    
    while True:
        choice = input('Select a player (or type "q" to cancel): ').strip()
        if choice.lower() == 'q':
            return
        if choice.isdigit() and 1 <= int(choice) <= len(player_list):
            character = player_list[int(choice) - 1]
            break
        print('Invalid input.')

    # 2. Character edit menu
    while True:
        print(f"\nEditing {character.name}:")
        print("1. Edit Stats")
        print("2. Edit Inventory")
        print("3. Edit Equipped Gear")
        print("4. Edit Abilities")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            edit_stats(character)
        elif choice == "2":
            edit_inventory(character, equipment_dict)
        elif choice == "3":
            edit_equipment(character, equipment_dict)
        elif choice == "4":
            edit_abilities(character, ability_dict)
        elif choice == "5":
            break
        else:
            print("Invalid input.")


def edit_stats(character):
    print("\nEditing Stats:")
    for attr in vars(character.stats):
        current = getattr(character.stats, attr)
        new = input(f"{attr.capitalize()} (current: {current}) → ")
        if new.strip().isdigit():
            setattr(character.stats, attr, int(new))

    # Recalculate derived stats and health/MP
    character.stats.power = character.stats.strength + character.stats.flexibility
    character.stats.constitution = character.stats.strength + character.stats.endurance
    character.stats.speed = character.stats.flexibility + character.stats.endurance
    character.stats.max_health = (character.stats.constitution * 3) + 5
    character.stats.max_mp = character.stats.mana * 3

    character.current_health = character.stats.max_health
    character.current_mp = character.stats.max_mp

    print("Stats updated.")


def edit_inventory(character, equipment_dict):
    print("\nInventory Editor")
    print("1. Add item")
    print("2. Remove item")
    print("3. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("Available equipment:")
        for name in equipment_dict:
            print(f"- {name}")
        item_name = input("Enter item to add: ").strip()
        if item_name in equipment_dict:
            character.add_to_inventory(equipment_dict[item_name])
    elif choice == "2":
        print("Inventory:")
        for i, item in enumerate(character.inventory, 1):
            print(f"{i}. {item.name}")
        index = input("Enter item number to remove: ").strip()
        if index.isdigit():
            idx = int(index) - 1
            if 0 <= idx < len(character.inventory):
                removed = character.inventory.pop(idx)
                print(f"Removed {removed.name}.")
    else:
        return



def edit_equipment(character, equipment_dict):
    print("\nEquipped Gear:")
    for slot, item in character.equiped.items():
        print(f"{slot.capitalize()}: {item.name}")

    slot = input("Enter slot to change (e.g., weapon, armor, head): ").strip().lower()
    if slot not in ["weapon", "armor", "head"]:
        print("Invalid slot.")
        return

    print("Available equipment:")
    for name, item in equipment_dict.items():
        if item.slot == slot:
            print(f"- {name}")

    item_name = input(f"Enter new item for {slot}: ").strip()
    if item_name in equipment_dict and equipment_dict[item_name].slot == slot:
        character.equiped[slot] = equipment_dict[item_name]
        print(f"{slot.capitalize()} updated.")


def edit_abilities(character, ability_dict):
    print("\nAbilities:")
    for i, ab in enumerate(character.abilities, 1):
        print(f"{i}. {ab.name}")

    print("1. Add ability")
    print("2. Remove ability")
    print("3. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("Available abilities:")
        for name in ability_dict:
            print(f"- {name}")
        ab_name = input("Enter ability name to add: ").strip()
        if ab_name in ability_dict and ability_dict[ab_name] not in character.abilities:
            character.abilities.append(ability_dict[ab_name])
            print("Ability added.")
    elif choice == "2":
        index = input("Enter ability number to remove: ").strip()
        if index.isdigit():
            idx = int(index) - 1
            if 0 <= idx < len(character.abilities):
                removed = character.abilities.pop(idx)
                print(f"Removed {removed.name}.")




