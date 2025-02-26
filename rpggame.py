import json
import random

# =========================
# Core RPG Game - Phase 1
# =========================

# Player Stats
player = {
    "name": "Hero",
    "health": 100,
    "attack": 10,
    "defense": 5,
    "xp": 0,
    "inventory": [],
    "location": "Town Center"
}

# Game Locations
locations = {
    "Town Center": {"description": "A bustling town filled with traders and adventurers.", "paths": ["Forest", "Dungeon Entrance"]},
    "Forest": {"description": "A dark and eerie forest filled with unknown dangers.", "paths": ["Town Center", "Deep Forest"]},
    "Dungeon Entrance": {"description": "A mysterious dungeon filled with monsters.", "paths": ["Town Center", "Dungeon Depths"]},
    "Deep Forest": {"description": "A place where powerful beasts roam.", "paths": ["Forest"]},
    "Dungeon Depths": {"description": "The deepest part of the dungeon, home to terrifying foes.", "paths": ["Dungeon Entrance"]}
}

# Enemy Types
enemies = [
    {"name": "Goblin", "health": 30, "attack": 5, "defense": 2, "xp": 10},
    {"name": "Skeleton", "health": 40, "attack": 7, "defense": 3, "xp": 15},
    {"name": "Dark Mage", "health": 50, "attack": 10, "defense": 5, "xp": 20},
]

# Save/Load Game Functions
def save_game():
    with open("savegame.json", "w") as f:
        json.dump(player, f)
    print("Game saved!")

def load_game():
    global player
    try:
        with open("savegame.json", "r") as f:
            player = json.load(f)
        print("Game loaded!")
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")

# Combat System
def combat(enemy):
    print(f"A wild {enemy['name']} appears!")
    
    while enemy["health"] > 0 and player["health"] > 0:
        action = input("Do you want to [A]ttack or [R]un? ").lower()
        
        if action == "a":
            damage = max(1, player["attack"] - enemy["defense"])
            enemy["health"] -= damage
            print(f"You attack the {enemy['name']} for {damage} damage!")

            if enemy["health"] > 0:
                enemy_damage = max(1, enemy["attack"] - player["defense"])
                player["health"] -= enemy_damage
                print(f"The {enemy['name']} attacks you for {enemy_damage} damage!")
        
        elif action == "r":
            print("You managed to escape!")
            return
        
    if player["health"] > 0:
        print(f"You defeated the {enemy['name']} and gained {enemy['xp']} XP!")
        player["xp"] += enemy["xp"]
    else:
        print("You have been defeated... Game Over!")

# Exploring the World
def explore():
    print(f"You are at {player['location']}. {locations[player['location']]['description']}")
    print("You can travel to:", ", ".join(locations[player['location']]["paths"]))

    choice = input("Where do you want to go? ").title()
    if choice in locations[player["location"]]["paths"]:
        player["location"] = choice
        print(f"You travel to {choice}.")
        
        # Random enemy encounter
        if random.random() < 0.3:  # 30% chance to encounter an enemy
            combat(random.choice(enemies))
        
    else:
        print("Invalid location. Try again.")

# Rest Feature
def rest():
    if player["location"] == "Town Center":
        if player["health"] < 100:
            player["health"] = 100
            print("You rest at the town and fully restore your health.")
        else:
            print("You are already at full health.")
    else:
        print("You can only rest in the Town Center.")

# Game Loop (Text-Based Navigation)
def game_loop():
    load_game()
    while True:
        print("\n==== RPG GAME ====")
        print(f"Location: {player['location']}, Health: {player['health']}, XP: {player['xp']}")
        print("[E]xplore | [R]est | [S]ave Game | [Q]uit")
        action = input("What do you want to do? ").lower()

        if action == "e":
            explore()
        elif action == "r":
            rest()
        elif action == "s":
            save_game()
        elif action == "q":
            print("Thanks for playing!")
            save_game()
            break
        else:
            print("Invalid option. Try again.")

# Start the Game
if __name__ == "__main__":
    game_loop()
