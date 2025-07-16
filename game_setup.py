
class Stats:
    def __init__(self, strength, endurance, flexibility, perception, charisma, mana):
        self.strength = strength
        self.endurance = endurance
        self.flexibility = flexibility
        self.perception = perception
        self.charisma = charisma
        self.mana = mana
    

class Abilities:
    def __init__(self, name):
        self.name = name

        #Components of Abilities??


class Equipment:
    def __init__(self, name):
        self.name = name

        #Components of equipment????


class Species:
    def __init__(self, stats, abilities, equipment):
        self.stats = stats
        self.abilities = abilities
        self.equipment = equipment


class Character:
    def __init__(self, name, species, stats):
        self.name = name
        self.species = species
        self.stats = stats
        self.inventory = []


def create_player_characters():
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
    
    for _ in range(len(pc_count)):
        pc_name = input('Name: ')
        pc_race = input('Name: ')
        pc_strength = get_stat("Strength")
        pc_endurance = get_stat('Endurance: ')
        pc_flexibility = get_stat('Flexibility: ')
        pc_perception = get_stat('Perception: ')
        pc_charisma = get_stat('Charisma: ')
        pc_mana = get_stat('Mana: ')


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




