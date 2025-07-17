import game_setup
import game_objects


def main():
    welcome()

    equipment_dict = create_all_equipment()
    ability_dict = create_all_abilities()
    species_dict = create_all_species(equipment_dict, ability_dict)
    #Initialize all the different Species, abilities, and equipment
    
    dm_menu()


def welcome():
    while True:
        print('Welcome to Grimcana')
        mainMenuChoice = input("1. New game\n2. Continue Game\n3. Game Explanation\n\n")

        if mainMenuChoice == "1":
            game_setup.create_player_characters()

            break

        elif mainMenuChoice == "2":
            # IMPORT JSON DATA
            break

        elif mainMenuChoice == "3":
            explain_game()
        
        else:
            print('Invalid input, please type "1", "2", or "3"\n')


def explain_game():
    print("Explanation\n")
    input('Press "Enter" to continue\n')


def dm_menu():
    while True:
        print('What would you like to do?')
        dmMenuChoice = input('1. Start Encounter\n2. Edit Player Character\n3. Save Game State\n\n')

        if dmMenuChoice == "1":
            # INITIALIZE AN Encounter
            create_enemies(species_dict)
            combat()

        elif dmMenuChoice == "2":
            # IDK

        elif dmMenuChoice == "3":
            # Update JSON FILE
        
        else:
            print('Invalid input, please type "1", "2", or "3"\n')



def combat(player_list, enemy_list):
    encounter_list = player_list + enemy_list
    current_time = 0
    encounter_continues = True
    action_queue = []
    

    while encounter_continues:
        for character in encounter_list:
            if not character.is_alive():
                continue
            
            #^ don't like the whole NOT thing

            #check for character action
                #if no action, then select one (aka action time is LESS than current time)
                #if action, then check time
                    #if time matches, perform action

            encounter_continues = encounter_status(player_list, enemy_list)

            current_time = current_time + 1
    
    #return to DM menu
    
    #turn determiner
    #action selector

    def encounter_status(players, enemies):
    if all(not p.is_alive() for p in players):
        print("The players have been defeated!")
        return False
    if all(not e.is_alive() for e in enemies):
        print("The enemies have been defeated!")
        return False
    return True


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

            if enemy_type in species_dict:
                break
            else:
                print("Invalid species. Please enter one of the following:")
                print(", ".join(species_dict.keys()))


        enemy = Character(f"Enemy {i+1}", species_dict[enemy_type], False)
        enemy_list.append(enemy)

    return enemy_list



main()