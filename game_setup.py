
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

        #Components of Abilities??


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

        #would it be better for me to add a list of all equipment, that is how abilities and characters work rn
        #or maybe those should be updated to this

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
            pc_count = input('How many players are there?')
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
        
        
        # TODO: Add inventory and abilities 

        player_list.append(player)
    
    return player_list




def get_stat(stat_name):
    while True:
        stat_value = input(f'{stat_name}: ')
        try:
            stat_value = int(stat_value)
            if 1 <= stat_value <= 20:
                return stat_value
            else:
                print('Please enter an integer from 1 to 20.\n')
        except ValueError:
            print('Please enter an integer from 1 to 20.\n')




