class Weapon:
    weapon_list = ['меч', 'топор', 'копье', 'кувалда']

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    @staticmethod
    def allowed_weapon(value):
        return value in Weapon.weapon_list
    
    @property
    def weapon(self):
        return Weapon.weapon_list

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError('[Ошибка ввода] -- Название не должно быть пустым')
        if not Weapon.allowed_weapon(name):
            raise ValueError(f'[Системная ошибка] -- Недопустиое название.\nРазрешенный тип оружия: {Weapon.weapon_list}')
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
        return f'{'-' * 15}\nНазвание оружия: {self._name}\nУрон от оружия: {self._damage}\n{'-' * 15}\n'
        
