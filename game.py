import logging

# 1. Конфигурация логгера в самом верху
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)

from stats import InMemoryStats
from character import Weapon, Player, Enemy
from battle import BattleEngine
from logger import Logger, ConsoleLogger


if __name__ == "__main__":
    # 2. Создаем все зависимости
    stats_manager = InMemoryStats()
    logger = ConsoleLogger()

    # 3. Создаем оружие и игроков
    player_weapon = Weapon(name='Ядовитый кинжал', damage=10)
    enemy_weapon = Weapon(name='Алмазный топор', damage=10)
    
    player = Player(name='ИГРОК_ДИМАС', health=100, weapon=player_weapon)
    enemy = Enemy(name='бот андрогин', health=100, weapon=enemy_weapon)
    
    # 4. Создаем экземпляр движка боя, передавая ему все зависимости
    battle_engine = BattleEngine(
        attacker=player, 
        defender=enemy, 
        stats_manager=stats_manager, 
        logger=logger
    )
    
    # 5. Запускаем бой
    battle_engine.fight()
