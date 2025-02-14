import random
import json
from rich.console import Console
from colorama import init

init(autoreset=True)
console = Console()

def load_data():
    try:
        with open("save_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("save_data.json", "w") as file:
        json.dump(data, file)

def reset_game():
    console.print("[bold red]ตัวละครตายแล้ว! เริ่มต้นใหม่...[/bold red]")
    data = {
        "name": "",
        "level": 1,
        "hp": 100,
        "max_hp": 100,
        "attack": 10,
        "defense": 5,
        "exp": 0,
        "gold": 50,
        "inventory": []
    }
    save_data(data)
    main()

def create_character():
    name = input("กรุณากรอกชื่อตัวละครของคุณ: ")
    data = {
        "name": name,
        "level": 1,
        "hp": 100,
        "max_hp": 100,
        "attack": 10,
        "defense": 5,
        "exp": 0,
        "gold": 50,
        "inventory": []
    }
    save_data(data)
    return data

def attack_enemy(player, enemy):
    damage = max(1, player["attack"] - enemy["defense"] + random.randint(-2, 2))
    enemy["hp"] -= damage
    console.print(f"{player['name']} โจมตี {enemy['name']} ทำดาเมจ {damage} HP", style="bold green")

def take_damage(player, damage):
    player["hp"] -= damage
    console.print(f"{player['name']} ถูกโจมตีเสีย {damage} HP", style="bold red")
    if player["hp"] <= 0:
        reset_game()

def gain_exp(player, amount):
    player["exp"] += amount
    console.print(f"{player['name']} ได้รับ {amount} EXP", style="yellow")
    if player["exp"] >= player["level"] * 20:
        level_up(player)

def level_up(player):
    player["level"] += 1
    player["max_hp"] += 10
    player["hp"] = player["max_hp"]
    player["attack"] += 2
    player["defense"] += 1
    player["exp"] = 0
    console.print(f"{player['name']} เลเวลอัพเป็น {player['level']}! HP: {player['max_hp']}, ATK: {player['attack']}, DEF: {player['defense']}", style="bold cyan")

def battle(player):
    monster_type = random.choice([("Goblin", 1, 1), ("Orc", 1.2, 1.2), ("Slime", 0.8, 0.5)])
    monster = {"name": monster_type[0], "level": random.randint(1, player["level"] + 1), "hp": 20 * monster_type[1], "attack": 5 * monster_type[1], "defense": 2 * monster_type[2]}
    
    console.print(f"[bold red]เริ่มการต่อสู้! {player['name']} vs {monster['name']}[/bold red]")
    while player["hp"] > 0 and monster["hp"] > 0:
        input("กด Enter เพื่อโจมตี...")
        attack_enemy(player, monster)
        if monster["hp"] > 0:
            take_damage(player, max(1, monster["attack"] - player["defense"] + random.randint(-2, 2)))
    
    if player["hp"] > 0:
        exp_gain = monster["level"] * 10
        gold_gain = monster["level"] * 5
        console.print(f"[bold green]{player['name']} ชนะ! ได้รับ {exp_gain} EXP และ {gold_gain} Gold[/bold green]")
        gain_exp(player, exp_gain)
        player["gold"] += gold_gain
    save_data(player)

def main():
    console.print("[bold blue]เกม RPG ข้อความ[/bold blue]")
    data = load_data()
    if not data.get("name"):
        data = create_character()
    
    while True:
        console.print("\n[1] ออกล่ามอนสเตอร์  [2] ดูสถานะ  [3] ออกจากเกม", style="bold yellow")
        choice = input("เลือกคำสั่ง: ")
        if choice == "1":
            battle(data)
        elif choice == "2":
            console.print(f"\n[bold cyan]{data['name']} (LV {data['level']}) HP: {data['hp']}/{data['max_hp']} ATK: {data['attack']} DEF: {data['defense']} EXP: {data['exp']} Gold: {data['gold']}")
        elif choice == "3":
            console.print("[bold red]ออกจากเกม...[/bold red]")
            save_data(data)
            break
        else:
            console.print("[bold red]ตัวเลือกไม่ถูกต้อง![/bold red]")

if __name__ == "__main__":
    main()
