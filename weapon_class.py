from random import choice, random

class Weapon:
    weapon_list = ['меч', 'топор', 'копье', 'кувалда']

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    @staticmethod
    def allowed_weapon(value):
        return value in Weapon.weapon_list

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError('[Ошибка ввода] -- Название не должно быть пустым')
        if not Weapon.allowed_weapon(name):
            raise ValueError(f'[Системная ошибка] -- Недопустиое название.\nРазрешенный тип оружия: {','.join(Weapon.weapon_list)}')
        self._name = name

    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'[Ошибка ввода] -- Урон не может быть представлен в формате str.\nНельзя: {value} ')
        if value <= 0:
            raise ValueError('Урон не может быть меньше или равен 0')
        self._damage = value

    def __str__(self):
        return f'Название оружия: {self._name}\nУрон от оружия: {self._damage}\n'
        
class Character:
    
    random_critical_bonus = [2, 5, 6, 0]

    def __init__(self, health, power, strenght, agility, level, xp, weapon):
        self.health = health
        self.power = power
        self.strenght = strenght
        self.agility = agility
        self.level = level
        self.xp = xp
        self.weapon = weapon
        self.is_rage = False

    def is_alive(self):
        return self.health > 0
    
    def is_enough_power(self):
        return self.power >= 50
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('[Ошибка ввода]: Здоровье может быть только числом')
        if not (0 <= value <= 100):
            raise ValueError('[Ошибка ввода]: Здоровье может быть установлено только от 0 до 100')
        self._health = value

    
    @staticmethod
    def generate_random_critical_bonus():
        random_bonus = [0, 0, 0.04, 0, 0.05, 0, 15, 0, 1, 0.1, 0.2, 0]
        bonus = choice(random_bonus)
        return bonus
    
    def rage_mode(self):
        '''
        RAGE MODE: При включенном режиме яросте у персонажа есть шанс нанести
        критический удар в пять раз выше с вероятностью 20%.
        Если шанс не выпадет - у игрока отнимается 50% здоровья.
        '''
        if not self.is_rage:
            self.is_rage = True
            print('[RADE MODE: ON]')
        else:
            self.is_rage = False
            print('[RADE MODE: OFF]')


    def attack(self):
        if self.is_rage:
            if random() < 0.2:
                self.power = 0
                return self.weapon.damage * 5
            else:
                self.health *= 0.5 
                return self.weapon.damage

        if self.is_enough_power():
            self.power -= 50
            return self.weapon.damage + Character.generate_random_critical_bonus()
        return self.weapon.damage