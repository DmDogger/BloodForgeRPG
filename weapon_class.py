from __future__ import annotations
from random import random

class Weapon:
    weapon_list = ['меч', 'топор', 'копье', 'кувалда']

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    @staticmethod
    def allowed_weapon(value: str) -> bool:
        return value in Weapon.weapon_list

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError('name must be non-empty string')
        if not Weapon.allowed_weapon(name):
            raise ValueError(f'can use only: {','.join(Weapon.weapon_list)}')
        self._name = name

    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'value only int or float ')
        if value <= 0:
            raise ValueError('damage must be greater than 0')
        self._damage = value

    def __str__(self):
        return f'{self._name}\n{self._damage}'
        
class Character:
    def __init__(self, health, weapon):
        self.health = health
        self.power = 100
        self.level = 1
        self.xp = 0
        self.weapon = weapon
        self.is_rage = False
        self.stats = {
            'total_wins' : 0,
            'total_loses' : 0,
            'total_fights' : 0,
        }

    def __str__(self):
        return '\n'.join([f'{key}: {value}' for key, value in sorted(self.__dict__.items())])

    def is_alive(self):
        return self.health > 0
    
    def spend_power(self, cost: int) -> bool: 
        if self.power >= cost:
            self.power -= cost
            return True
        return False

    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('health can be only int or float')
        self._health = min(100, max(0,  value))

    
    @staticmethod
    def rage_attack_success():
        return random() < 0.5
    
    def rage_mode(self):
        self.is_rage = not self.is_rage

    def attack(self):
        # --- Обычный удар
        if not self.is_rage:
            if self.spend_power(5):
                return round(self.weapon.damage * random(), 2)
            else:
                self.health -= 5
                return round(self.weapon.damage * random(), 2)
            
        # --- Удар берсерка
        if self.is_rage:
            if not self.spend_power(30):
                return self.weapon.damage # возвращаем обычный урон если нет энергии
            if self.rage_attack_success(): # если успешный удар
                return self.weapon.damage  * 5 # вернем большой урон
            self.health *= 0.5
            return round(self.weapon.damage * random(), 2)
                