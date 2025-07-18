import game_setup
from game_setup import Stats
from game_setup import Ability
from game_setup import Equipment
from game_setup import Species



def create_all_abilities():
    ability_dict = {
        "Slash": Ability("Slash", base_damage=3, time_cost=2, mana_cost=0),
        "Punch": Ability("Punch", base_damage=2, time_cost=1, mana_cost=0),
        "Magic Missile": Ability("Magic Missile", base_damage=5, time_cost=3, mana_cost=3),
        "Quick Shot": Ability("Quick Shot", base_damage=2, time_cost=1, mana_cost=0),
        "Stone Skin": Ability("Stone Skin", base_damage=0, time_cost=2, mana_cost=3)
    }
    return ability_dict
    

def create_all_equipment():
    equipment_dict = {
        "Sword": Equipment("Sword", damage=2, weight=2, armor=0, slot="weapon"),
        "Shield": Equipment("Shield", damage=0, weight=1, armor=2, slot="armor"),
        "Helmet": Equipment("Helmet", damage=0, weight=1, armor=1, slot="head"),
    }
    return equipment_dict


def create_all_species(equipment_dict, ability_dict):
    species_info = {
        "Human": {
            "stats": Stats(10, 10, 10, 10, 10, 10),
            "equipment": ["Sword", "Shield"],
            "abilities": ["Slash", "Punch"]
        },
        "Elf": {
            "stats": Stats(8, 8, 10, 12, 12, 14),
            "equipment": ["Sword", "Helmet"],
            "abilities": ["Magic Missile", "Quick Shot"]
        },
        "Dwarf": {
            "stats": Stats(12, 12, 8, 8, 8, 8),
            "equipment": ["Sword", "Helmet"],
            "abilities": ["Stone Skin", "Slash"]
        }
    }

    species_dict = {}

    for name, data in species_info.items():
        # Get actual Equipment objects
        starting_equipment = {
            equipment_dict[item].slot: equipment_dict[item]
            for item in data["equipment"]
            if item in equipment_dict
        }

        # Get actual Ability objects
        ability_list = [
            ability_dict[ab] for ab in data["abilities"]
            if ab in ability_dict
        ]

        # Create Species object and add to dict
        species_dict[name] = Species(
            name=name,
            stats=data["stats"],
            abilities=ability_list,
            starting_equipment=starting_equipment
        )

    return species_dict

