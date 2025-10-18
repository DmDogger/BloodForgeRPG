from __future__ import annotations
from random import random, uniform
import constants
import state
from stats import Stats
from battle import Battle
from character import Weapon, Player, Enemy


if __name__ == "__main__":
    # Создаём оружие
    player_weapon = Weapon(name='меч', damage=10)  # Урон в диапазоне 1-25
    enemy_weapon = Weapon(name='топор', damage=10)
    
    # Создаём игроков
    player = Player(name='хХх_Злая_киса_ХхХ', health=100, weapon=player_weapon)
    enemy = Enemy(name='БлудякаГном28', health=100, weapon=enemy_weapon)
    
    # Создаём битву и запускаем
    battle = Battle(fighter_1=player, fighter_2=enemy)
    battle.fight()
    





