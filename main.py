import game_setup
import game_objects
import heapq
from game_setup import Character
from game_setup import Action


def main():

    equipment_dict = game_objects.create_all_equipment()
    ability_dict = game_objects.create_all_abilities()
    species_dict = game_objects.create_all_species(equipment_dict, ability_dict)
    #Initialize all the different Species, abilities, and equipment

    player_list = welcome(species_dict, equipment_dict, ability_dict)
    dm_menu(player_list, species_dict)


def welcome(species_dict, equipment_dict, ability_dict):
    while True:
        print('Welcome to Grimcana')
        mainMenuChoice = input("1. New game\n2. Continue Game\n3. Game Explanation\n\n")

        if mainMenuChoice == "1":
            player_list = game_setup.create_player_characters(species_dict, equipment_dict, ability_dict)

            return player_list

        elif mainMenuChoice == "2":
            # TODO: player_list = IMPORT function to retrieve JSON DATA

            return player_list

        elif mainMenuChoice == "3":
            explain_game()
            continue
        
        else:
            print('Invalid input, please type "1", "2", or "3"\n')


def explain_game():
    print("Explanation\n")
    # TODO: make an actual explanation 
    input('Press "Enter" to continue\n')


def dm_menu(player_list, species_dict):
    while True:
        print('What would you like to do?')
        dmMenuChoice = input('1. Start Encounter\n2. Edit Player Character\n3. Save Game State\n\n')

        # DM selects monster the players will fight, and combat begins
        if dmMenuChoice == "1":
            enemy_list = create_enemies(species_dict)
            combat(player_list, enemy_list)

        elif dmMenuChoice == "2":
            continue # temp until logic added
            # TODO: add function to edit player character stats
            # Create a function to choose a character to edit. Maybe add a method to character, that allows one to change a stat

        elif dmMenuChoice == "3":
            continue # temp until logic added
            # TODO: Update JSON FILE
        
        else:
            print('Invalid input, please type "1", "2", or "3"\n')



def combat(player_list, enemy_list):
    encounter_list = player_list + enemy_list
    current_time = 0
    action_queue = []

    # Priority queue requires actions to be orderable by scheduled_time

    while True:
        # End condition
        if not any(p.is_alive() for p in player_list):
            print("The players have been defeated!")
            break
        if not any(e.is_alive() for e in enemy_list):
            print("The enemies have been defeated!")
            break

        # 1. Add actions for characters ready to act
        for character in encounter_list:
            if not character.is_alive():
                continue

            if character.ready_time <= current_time:
                print(f"\n{character.name} select an action")
                
                # TEMP: Auto-pick first ability and random target (replace with player input)
                # TODO: player inputs the ability they want to use
                ability = character.abilities[0]

                # Determine who is alive to target, and Target a character
                alive_targets = []
                for e in encounter_list:
                    if e.is_alive():
                        alive_targets.append(e)

                if not alive_targets:
                    continue

                target = alive_targets[0]  # TEMP: pick first target (replace with player input)
                # TODO: player inputs who to target
                
                # Create and schedule action
                action = Action(character, ability, target, current_time)
                heapq.heappush(action_queue, action)

                # Set when this character will next be ready
                character.ready_time = action.scheduled_time

        # 2. If action queue is empty, just skip time forward
        if not action_queue:
            current_time += 1
            continue

        # 3. If next action is ready, execute it
        next_action = action_queue[0]
        if next_action.scheduled_time <= current_time:
            heapq.heappop(action_queue)
            print(f"\n--- Time {current_time} ---")
            next_action.execute()
        else:
            # No one ready yet, tick time forward
            current_time = current_time + 1





def create_enemies(species_dict):
    while True:
        enemy_count = input("How many enemies are there?\n")
        try:
            enemy_count = int(enemy_count)
            if enemy_count > 0:
                break
            else:
                print('Please enter a valid integer\n')
        except ValueError:
            print('Please enter a valid integer\n')

    enemy_list = []

    for i in range(enemy_count):
        while True:
            
            enemy_type = input(f"Enter species for enemy {i+1}: ").strip().capitalize()

            # not sure if try except is neccesary here ??????
            try: 
                if enemy_type in species_dict:
                    break
                else:
                    print("Invalid species. Please enter one of the following:")
                    print(", ".join(species_dict.keys()))
            except:
                print("Invalid species. Please enter one of the following:")
                print(", ".join(species_dict.keys()))


        enemy = Character(f"Enemy {i+1}", species_dict[enemy_type], False)
        enemy_list.append(enemy)

    return enemy_list



main()