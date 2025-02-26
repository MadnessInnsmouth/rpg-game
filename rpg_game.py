import json
import random
import os
import keyboard  # For key-based navigation
import time
import requests  # For auto-updater
import subprocess  # To convert to .exe after updating
from tqdm import tqdm  # For progress bar

# =========================
# Core RPG Game Rewrite - Full Version
# =========================

# Auto-Updater Settings
UPDATE_URL = "https://raw.githubusercontent.com/MadnessInnsmouth/rpg-game/main/version.json"  # Replace with real URL
GAME_FILE = "rpg_game.py"
EXE_FILE = "rpg_game.exe"

def check_for_updates():
    try:
        print("Checking for updates...")
        response = requests.get(UPDATE_URL)
        latest_version = response.json()["version"]
        
        with open("version.json", "r") as f:
            current_version = json.load(f)["version"]
        
        if latest_version > current_version:
            choice = input("A new update is available. Do you want to download it? (Y/N): ").strip().lower()
            if choice == "y":
                print("Downloading update...")
                download_update()
        else:
            print("You are running the latest version.")
    except Exception as e:
        print("Failed to check for updates:", e)

def download_update():
    try:
        update_url = requests.get(UPDATE_URL).json()["download_url"]
        response = requests.get(update_url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 KB
        t = tqdm(total=total_size, unit="B", unit_scale=True)
        
        with open(GAME_FILE, "wb") as f:
            for data in response.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        print("Update installed! Converting to .exe...")
        convert_to_exe()
    except Exception as e:
        print("Update failed:", e)

def convert_to_exe():
    try:
        print("Converting updated game to .exe...")
        subprocess.run(["pyinstaller", "--onefile", GAME_FILE], check=True)
        new_exe_path = os.path.join("dist", EXE_FILE)
        if os.path.exists(new_exe_path):
            os.replace(new_exe_path, EXE_FILE)
            print("Game successfully updated and converted to .exe! Restarting...")
            os.system(EXE_FILE)
            exit()
        else:
            print("Error: .exe file not found after conversion.")
    except Exception as e:
        print("Failed to convert to .exe:", e)

# Player Stats
player = {
    "name": "Hero",
    "health": 100,
    "attack": 10,
    "defense": 5,
    "xp": 0,
    "gold": 50,
    "inventory": [],
    "location": "Town Center",
    "level": 1,
    "quests": []
}

# Game Locations
locations = {
    "Town Center": {
        "description": "A bustling town filled with traders and adventurers.",
        "paths": ["Forest", "Dungeon Entrance"],
        "shop": True,
        "npc": "Elder Mage"
    },
    "Forest": {
        "description": "A dark and eerie forest filled with unknown dangers.",
        "paths": ["Town Center", "Deep Forest"],
        "shop": False,
        "npc": "Wandering Merchant"
    },
    "Dungeon Entrance": {
        "description": "A mysterious dungeon filled with monsters.",
        "paths": ["Town Center", "Dungeon Depths"],
        "shop": False,
        "npc": None
    },
}

# Save/Load Game Functions
def save_game():
    with open("savegame.json", "w") as f:
        json.dump(player, f)
    print("Game saved!")

def load_game():
    global player
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            player = json.load(f)
        print("Game loaded!")
    else:
        print("No saved game found. Starting a new game.")

# Game Loop
def game_loop():
    check_for_updates()
    load_game()
    while True:
        print("\n==== RPG GAME ====")
        print(f"Location: {player['location']}, Health: {player['health']}, XP: {player['xp']}, Gold: {player['gold']}")
        print("Press E to Explore, S to Save, or Q to Quit")
        action = keyboard.read_event().name
        
        if action == "e":
            explore()
        elif action == "s":
            save_game()
        elif action == "q":
            print("Thanks for playing!")
            save_game()
            break
        time.sleep(1)

# Start the Game
game_loop()
