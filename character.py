import constants
from random import random
import state

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
        self.state = state.NormalAttackState()
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
        return self.state.attack(self)
      
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
        if isinstance(self.state, state.NormalAttackState):
            self.state = state.RageAttackState()
        else:
            self.state = state.NormalAttackState()



    


                
class Enemy(Character):
    '''Дефолтный класс врага'''
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)



class Player(Character):
    '''Дефолтный класс персонажа'''
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)

