from abc import ABC, abstractmethod
import constants as c
from random import uniform

class AttackState(ABC):
    @abstractmethod
    def attack(self, character):
        '''Метод для дочерних классов, определяющий атаку'''
        pass

class NormalAttackState(AttackState):
    '''Класс для обычной атаки игрока'''
    def attack(self, character):
        if character.spend_power(c.BASE_POWER_COST):
            miltiplied_damage = round(character.weapon.damage * self._rnd_multiplier(), 2) # Округляем до 2-х символов
            return miltiplied_damage
        else:
            character.health -= c.NO_POWER_FINE
            return character.weapon.damage * c.NO_POWER_DAMAGE
        
    def _rnd_multiplier(self) -> float:
       #Генерируем каждый раз рандомный мултиплаер для урона от 0.6 до 1.2
        return uniform(c.RANDOM_DAMAGE_MIN, c.RANDOM_DAMAGE_MAX)
        

class RageAttackState(AttackState):
    '''Класс для совершения яростного удара игроком'''
    def attack(self, character) -> float:
        '''Метод для яростной атаки'''
        # Если есть энергия -> мы ее тратим и заходим в проверку успеха
        if character.spend_power(c.RAGE_POWER_COST):
            # Потратили энергию -> пробуем на успех
            if character.rage_attack_success():
                return character.weapon.damage * c.DAMAGE_MULTIPLIER
            # Неудачная попытка -> тратим НР, наносим обычный урон
            else:
                character.health *= c.UNSUCCESS_POWER_ATTACK_COST
                return character.weapon.damage * self._rnd_multiplier()
        # Если энергии нет -> просто наносим обычный урон
        miltiplied_damage = round(character.weapon.damage * self._rnd_multiplier(), 2) # Округляем до 2-х символов
        return miltiplied_damage
    
    def _rnd_multiplier(self) -> float:
       #Генерируем каждый раз рандомный мултиплаер для урона от 0.6 до 1.2
        return uniform(c.RANDOM_DAMAGE_MIN, c.RANDOM_DAMAGE_MAX)
    

class PoisonedAttackState(AttackState):
    '''Реализация отравления появится позже, пока просто метод атаки при отравлении'''
    def attack(self, character):
        if character.spend_power(c.BASE_POWER_COST):
            character.health -= c.POISONED_HEALTH
            return self._poisoned_multiplier(character)
        else:
            character.health -= c.NO_POWER_POISONED_FINE
            return self._poisoned_multiplier(character)
        

    def _poisoned_multiplier(self, character):
        return character.weapon.damage * c.POISONED_ATTACK



