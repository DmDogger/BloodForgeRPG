from __future__ import annotations
from random import random, uniform
import constants

class Weapon:
    '''
    Класс для создания оружия.
    Принимает название и урон оружия.
    '''

    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage

    @staticmethod
    def allowed_weapon(value: str) -> bool:
        return value in constants.ALLOWED_WEAPONS

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise ValueError('Имя должно быть только непустой строкой. Формат: STR')
        if name not in constants.ALLOWED_WEAPONS:
            raise ValueError(f'Используйте только: {constants.ALLOWED_WEAPONS}')
        self._name = name

    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'Значения могут быть только INT и FLOAT')
        if not (0 < value <= 25):
            raise ValueError('Урон оружия должен быть в диапазоне от 1 до 25 ед.')
        self._damage = value
        

class Character:
    def __init__(self, name, health, weapon):
        self.name = name
        self.health = health
        self.power = constants.POWER
        self.level = constants.LEVEL
        self.xp = constants.XP
        self.weapon = weapon
        self.is_rage = False
        self.attack_handler = CharacterAttack(self)
        self.stats = {
            'total_wins' : 0,
            'total_loses' : 0,
            'total_draws' : 0,
            'total_fights' : 0,
        }

    def __str__(self):
        return f'{self.name}: {self.health} HP'

    def is_alive(self) -> bool:
        return self.health > 0
    
    def attack(self):
        return self.attack_handler.perform_attack()
      
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Значения могут быть только INT и FLOAT')
        self._health = min(constants.MAX_HEALTH, max(0,  value))

    def spend_power(self, cost: int) -> bool: 
        if self.power >= cost:
            self.power -= cost
            return True
        return False
    
    @staticmethod
    def rage_attack_success() -> float:
        return random() < constants.RAGE_SUCCESS_RATE
    
    def rage_mode(self):
        self.is_rage = not self.is_rage    

####
class RageMode:
    '''Здесь будет реализован RageMode (State Pattern)'''
    pass


class CharacterAttack:
    '''Класс для совершения атак игроками'''
    def __init__(self, character):
        self.character = character

    def perform_attack(self) -> float:
        '''Метод выбирает какую применить атаку, в зависимости от включенного Rage Mode'''
        if self.character.is_rage:
            return self._rage_attack()
        return self._normal_attack() # СДЕЛАТЬ КЛАСС РЕЙДЖ МОД и переписать

    def _normal_attack(self) -> float:
        '''Метод для обычной атаки'''
        if self.character.spend_power(constants.BASE_POWER_COST):
            miltiplied_damage = round(self.character.weapon.damage * self._rnd_multiplier(), 2) # Округляем до 2-х символов
            return miltiplied_damage
        else:
            self.character.health -= constants.NO_POWER_FINE
            return self.character.weapon.damage * constants.NO_POWER_DAMAGE

    def _rage_attack(self) -> float:
        '''Метод для яростной атаки'''
        # Если есть энергия -> мы ее тратим и заходим в проверку успеха
        if self.character.spend_power(constants.RAGE_POWER_COST):
            # Потратили энергию -> пробуем на успех
            if self.character.rage_attack_success():
                return self.character.weapon.damage * constants.DAMAGE_MULTIPLIER
            # Неудачная попытка -> тратим НР, наносим обычный урон
            else:
                self.character.health *= constants.UNSUCCESS_POWER_ATTACK_COST
                return self.character.weapon.damage * self._rnd_multiplier()
        # Если энергии нет -> просто наносим обычный урон
        miltiplied_damage = round(self.character.weapon.damage * self._rnd_multiplier(), 2) # Округляем до 2-х символов
        return miltiplied_damage
    
    def _rnd_multiplier(self) -> float:
        #Генерируем каждый раз рандомный мултиплаер для урона от 0.6 до 1.2
        return uniform(constants.RANDOM_DAMAGE_MIN, constants.RANDOM_DAMAGE_MAX)

                
class Enemy(Character):
    '''Дефолтный класс врага'''
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)



class Player(Character):
    '''Дефолтный класс персонажа'''
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.stats_handler = Stats(self.player, self.enemy)

    def fight(self):
        round_counter = 1
        print('--- [Начало боя] ---')
        print(f'Игрок {self.player.name} VS {self.enemy.name}')

        while self.player.is_alive() and self.enemy.is_alive():
            if round_counter >= constants.ROUND_TIMEOUT:
                print(f'Игроки {self.player.name} и {self.enemy.name} изнеможены')
                print(f'Объявляется ничья!')
                self.stats_handler.make_draw()
                break

            #каунтер раундов
            print(f'Раунд: {round_counter}')

            # враг атакует, снимает НР у героя
            enemy_damage = self.enemy.attack()
            self.player.health -= enemy_damage

            print(f'Враг [{self.enemy.name}] наносит [{enemy_damage}] урона. Осталось: {self.player.health} HP у игрока.')

            #проверка жив ли игрок
            if not self.player.is_alive():
                print(f'Победитель: {self.enemy.name}')
                self.stats_handler.enemy_win()
                break

            #игрок атакует, снимает НР у врага
            player_damage = self.player.attack()
            self.enemy.health -= player_damage
            print(f'Игрок [{self.player.name}] наносит [{player_damage}] урона. Осталось: {self.enemy.health} HP у врага.')

            #проверка жив ли враг
            if not self.enemy.is_alive():
                print(f'Победитель: {self.player.name}')
                self.stats_handler.player_win()
                self.player.xp += constants.MIN_XP_REWARD
                break

            round_counter += 1
        print('--- Конец битвы ---')
        print(f'У игрока всего боев {self.player.stats['total_fights']} из которых {self.player.stats['total_wins']} побед и {self.player.stats['total_loses']} поражений.')

class Stats:
    '''Метод для работы со статистикой'''

    display_stats = {
        'total_wins' : 'Всего побед',
        'total_loses' : 'Всего поражений',
        'total_fights' : 'Всего боев',
        'total_draws' : 'Всего ничьих'
   }

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy


    def player_win(self):
        '''Обновляем статистику при победе игрока'''
        self.player.stats['total_wins'] += 1
        self.player.stats['total_fights'] += 1
        self.enemy.stats['total_loses'] += 1
        self.enemy.stats['total_fights'] += 1

    def enemy_win(self):
        '''Обновляем статистику при победе врага'''
        self.enemy.stats['total_wins'] += 1
        self.enemy.stats['total_fights'] += 1
        self.player.stats['total_loses'] += 1
        self.player.stats['total_fights'] += 1

    def make_draw(self):
        '''Обновляем статистику при ничьей'''
        self.player.stats['total_fights'] += 1
        self.player.stats['total_draws'] += 1
        self.enemy.stats['total_draws'] += 1
        self.enemy.stats['total_fights'] += 1   

    def print_all_stats(self):
        '''Печатаем статистику игрока'''
        print(f'--- Статистика {self.player.name} ---')
        for key, value in self.player.stats.items():
            label = Stats.display_stats.get(key, key)
            print (f'{label}: {value}')
        print('-' * 20)


if __name__ == "__main__":
    # Создаём оружие
    player_weapon = Weapon(name='меч', damage=10)  # Урон в диапазоне 1-25
    enemy_weapon = Weapon(name='топор', damage=10)
    
    # Создаём игроков
    player = Player(name='хХх_Злая_киса_ХхХ', health=100, weapon=player_weapon)
    enemy = Enemy(name='БлудякаГном28', health=100, weapon=enemy_weapon)
    
    # Создаём битву и запускаем
    battle = Battle(player=player, enemy=enemy)
    battle.fight()
    
    # Опционально: печатаем статистику после боя
    battle.stats_handler.print_all_stats()




