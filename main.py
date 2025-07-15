import game_setup
import encounters
import game_objects


def main():
    welcome()
    
    dm_menu()


def welcome():
    while True:
        print('Welcome to "[GAME NAME]"')
        mainMenuChoice = input("1. New game\n2. Continue Game\n3. Game Explanation\n\n")

        if mainMenuChoice == "1":
            # INITIALIZE A NEW GAME, name new Save file
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
            encounter()

        elif dmMenuChoice == "2":
            # IDK

        elif dmMenuChoice == "3":
            # Update JSON FILE
        
        else:
            print('Invalid input, please type "1", "2", or "3"\n')


main()