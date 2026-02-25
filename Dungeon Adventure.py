import random
import json
import os

SAVE_FILE = "savegame.json"


# ================== КЛАСС ИГРОКА ==================
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 15
        self.gold = 0
        self.exp = 0
        self.level = 1
        self.potions = 2

    def level_up(self):
        if self.exp >= self.level * 50:
            self.level += 1
            self.max_hp += 20
            self.attack += 5
            self.hp = self.max_hp
            print(f"\n🎉 Level UP! Now level {self.level}!")


# ================== КЛАСС ВРАГА ==================
class Enemy:
    def __init__(self):
        self.name = random.choice(["Goblin", "Skeleton", "Orc"])
        self.hp = random.randint(40, 80)
        self.attack = random.randint(5, 15)


# ================== ФУНКЦИИ ==================
def save_game(player):
    data = player.__dict__
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("💾 Game saved!")


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    player = Player(data["name"])
    player.__dict__.update(data)
    return player


def fight(player):
    enemy = Enemy()
    print(f"\n⚔ You encountered a {enemy.name}!")

    while enemy.hp > 0 and player.hp > 0:
        print(f"\n{player.name} HP: {player.hp}")
        print(f"{enemy.name} HP: {enemy.hp}")
        print("1. Attack")
        print("2. Use Potion")
        print("3. Run")

        choice = input("Choose action: ")

        if choice == "1":
            damage = random.randint(player.attack - 5, player.attack + 5)
            enemy.hp -= damage
            print(f"You deal {damage} damage!")

        elif choice == "2":
            if player.potions > 0:
                heal = 30
                player.hp = min(player.max_hp, player.hp + heal)
                player.potions -= 1
                print(f"You healed {heal} HP!")
            else:
                print("No potions left!")
                continue

        elif choice == "3":
            print("You ran away!")
            return

        else:
            continue

        if enemy.hp > 0:
            damage = random.randint(enemy.attack - 3, enemy.attack + 3)
            player.hp -= damage
            print(f"{enemy.name} hits you for {damage} damage!")

    if player.hp > 0:
        print(f"\n🏆 You defeated {enemy.name}!")
        reward_gold = random.randint(10, 30)
        reward_exp = random.randint(20, 40)
        player.gold += reward_gold
        player.exp += reward_exp
        print(f"You gained {reward_gold} gold and {reward_exp} EXP.")
        player.level_up()
    else:
        print("\n💀 You died...")


def explore(player):
    print("\n🔍 Exploring dungeon...")
    event = random.choice(["enemy", "treasure", "nothing"])

    if event == "enemy":
        fight(player)

    elif event == "treasure":
        gold = random.randint(10, 50)
        player.gold += gold
        player.potions += 1
        print(f"💰 Found treasure! +{gold} gold and +1 potion!")

    else:
        print("Nothing happened...")


def show_stats(player):
    print("\n===== PLAYER STATS =====")
    print(f"Name: {player.name}")
    print(f"Level: {player.level}")
    print(f"HP: {player.hp}/{player.max_hp}")
    print(f"Attack: {player.attack}")
    print(f"Gold: {player.gold}")
    print(f"EXP: {player.exp}")
    print(f"Potions: {player.potions}")
    print("========================")


# ================== ГЛАВНОЕ МЕНЮ ==================
def main():
    print("🏰 DUNGEON ADVENTURE")

    print("1. New Game")
    print("2. Load Game")

    choice = input("Select option: ")

    if choice == "2":
        player = load_game()
        if not player:
            print("No save found. Starting new game.")
            name = input("Enter your name: ")
            player = Player(name)
    else:
        name = input("Enter your name: ")
        player = Player(name)

    while player.hp > 0:
        show_stats(player)

        print("\nChoose action:")
        print("1. Fight")
        print("2. Explore")
        print("3. Save Game")
        print("4. Exit")

        action = input("Action: ")

        if action == "1":
            fight(player)

        elif action == "2":
            explore(player)

        elif action == "3":
            save_game(player)

        elif action == "4":
            print("Goodbye!")
            break

    if player.hp <= 0:
        print("\n☠ GAME OVER")


if __name__ == "__main__":
    main()