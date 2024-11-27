#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  27-11-2024
Last update: 27-11-2024
Version: 1.0
Description: A role play game in Python3 with rich and click.  
Example of use: python3 play.py
'''
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import print as rprint
import random
import time
from dataclasses import dataclass
from typing import List, Dict

console = Console()

@dataclass
class Player:
    name: str
    health: int = 100
    max_health: int = 100
    level: int = 1
    exp: int = 0
    gold: int = 50
    inventory: List[str] = None
    
    def __post_init__(self):
        if self.inventory is None:
            self.inventory = ['Health Potion']

@dataclass
class Enemy:
    name: str
    health: int
    damage: int
    exp_reward: int
    gold_reward: int

class Game:
    def __init__(self):
        self.console = Console()
        self.player = None
        self.enemies = {
            'Goblin': Enemy('Goblin', 30, 10, 20, 15),
            'Wolf': Enemy('Wolf', 25, 15, 25, 20),
            'Bandit': Enemy('Bandit', 40, 20, 35, 30),
            'Dragon': Enemy('Dragon', 100, 30, 100, 150)
        }
        
    def display_intro(self):
        console.print(Panel.fit(
            "[bold yellow]Welcome to the Fantasy RPG Adventure![/bold yellow]\n\n"
            "Embark on an epic journey through dangerous lands...",
            title="[red]Fantasy Quest[/red]",
            border_style="blue"
        ))
        time.sleep(1)
        
    def create_character(self):
        console.print("\n[bold blue]Character Creation[/bold blue]")
        name = Prompt.ask("[yellow]Enter your hero's name[/yellow]")
        self.player = Player(name)
        console.print(f"\n[green]Welcome, {name}! Your adventure begins...[/green]")
        
    def display_status(self):
        table = Table(title=f"{self.player.name}'s Status")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Health", f"{self.player.health}/{self.player.max_health}")
        table.add_row("Level", str(self.player.level))
        table.add_row("Experience", str(self.player.exp))
        table.add_row("Gold", str(self.player.gold))
        table.add_row("Inventory", ", ".join(self.player.inventory))
        
        console.print(table)
        
    def combat(self, enemy_type: str):
        enemy = self.enemies[enemy_type]
        enemy_instance = Enemy(
            enemy.name,
            enemy.health,
            enemy.damage,
            enemy.exp_reward,
            enemy.gold_reward
        )
        
        console.print(f"\n[red]A {enemy_instance.name} appears![/red]")
        
        while enemy_instance.health > 0 and self.player.health > 0:
            console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
            action = Prompt.ask("Choose", choices=["attack", "use potion", "run"])
            
            if action == "attack":
                damage = random.randint(15, 25)
                enemy_instance.health -= damage
                console.print(f"[green]You deal {damage} damage to the {enemy_instance.name}![/green]")
                
                if enemy_instance.health <= 0:
                    self.victory(enemy_instance)
                    return True
                
                player_damage = random.randint(5, enemy_instance.damage)
                self.player.health -= player_damage
                console.print(f"[red]The {enemy_instance.name} deals {player_damage} damage to you![/red]")
                
                if self.player.health <= 0:
                    self.game_over()
                    return False
                
            elif action == "use potion":
                if "Health Potion" in self.player.inventory:
                    self.player.inventory.remove("Health Potion")
                    heal_amount = 50
                    self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                    console.print("[green]You used a Health Potion and recovered 50 health![/green]")
                else:
                    console.print("[red]You don't have any Health Potions![/red]")
                    
            elif action == "run":
                if random.random() < 0.5:
                    console.print("[yellow]You successfully ran away![/yellow]")
                    return True
                else:
                    console.print("[red]You failed to run away![/red]")
                    
            self.display_status()
            
    def victory(self, enemy: Enemy):
        console.print(f"\n[green]You defeated the {enemy.name}![/green]")
        self.player.exp += enemy.exp_reward
        self.player.gold += enemy.gold_reward
        console.print(f"[yellow]You gained {enemy.exp_reward} experience and {enemy.gold_reward} gold![/yellow]")
        
        if self.player.exp >= 100:
            self.level_up()
            
    def level_up(self):
        self.player.level += 1
        self.player.exp -= 100
        self.player.max_health += 20
        self.player.health = self.player.max_health
        console.print(f"\n[bold green]Level Up! You are now level {self.player.level}![/bold green]")
        console.print("[green]Your maximum health has increased![/green]")
        
    def game_over(self):
        console.print(Panel.fit(
            "[bold red]Game Over![/bold red]\n\n"
            f"Your adventure ends here, {self.player.name}...",
            border_style="red"
        ))
        
    def shop(self):
        console.print("\n[bold yellow]Welcome to the Shop![/bold yellow]")
        items = {
            "Health Potion": 30,
            "Better Sword": 100,
            "Shield": 80
        }
        
        table = Table(title="Shop Items")
        table.add_column("Item", style="cyan")
        table.add_column("Price", style="yellow")
        
        for item, price in items.items():
            table.add_row(item, str(price))
            
        console.print(table)
        
        item = Prompt.ask("What would you like to buy? (or type 'exit' to leave)", 
                         choices=[*items.keys(), "exit"])
        
        if item != "exit":
            if self.player.gold >= items[item]:
                self.player.gold -= items[item]
                self.player.inventory.append(item)
                console.print(f"[green]You bought {item}![/green]")
            else:
                console.print("[red]Not enough gold![/red]")

@click.command()
def main():
    game = Game()
    game.display_intro()
    game.create_character()
    
    while True:
        game.display_status()
        
        action = Prompt.ask(
            "\n[bold cyan]What would you like to do?[/bold cyan]",
            choices=["explore", "shop", "quit"]
        )
        
        if action == "explore":
            enemy = random.choice(list(game.enemies.keys()))
            if not game.combat(enemy):
                break
                
        elif action == "shop":
            game.shop()
            
        elif action == "quit":
            console.print("[yellow]Thanks for playing![/yellow]")
            break
            
if __name__ == "__main__":
    main()

