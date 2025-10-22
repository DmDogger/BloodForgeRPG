from character import Player, Enemy

class XPManager:
    '''Менеджер XP (Опыт игрока)'''

    # табличка, будет вынесена в отдельный /config/
    level_tab = { 0:0,
                1:50,
                2:150,
                3:350,
                4:600,
                5:1000,
                6:1500
    }

    def __init__(self, character: Player | Enemy) -> None:
        self.character = character

    @property
    def xp(self) -> int:
        return self.character.xp

    @xp.setter
    def xp(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError('XP может быть только целым числом')
        if value < 0:
            raise ValueError('XP не может быть установлен ниже нуля')
        self.xp = value

    def add_xp(self, value: int) -> None:
        self.xp += value


    def reset_xp(self) -> None:
        self.character.xp = 0

    def _is_enough_xp(self) -> bool:
        next_level = self.character.level + 1
        need_points = self.level_tab.get(next_level)
        if need_points is None:
            return False
        return self.character.xp >= need_points


    def xp_to_next_level(self) -> int:
        next_level = self.character.level + 1
        points_next_level = self.level_tab.get(next_level)
        if points_next_level is None:
            raise ValueError(f'Следующий уровень: {next_level} еще не определен')
        return points_next_level - self.character.xp
    
    def level_up(self) -> None:
        next_level = self.character.level + 1
        points_to_nxt_lvl = self.level_tab.get(next_level)
        if points_to_nxt_lvl is None:
            raise ValueError(f'Уровень {self.character.level} является максимальным')
        if self.character.xp >= points_to_nxt_lvl:
            self.character.level = next_level
            self.character.xp -= points_to_nxt_lvl












