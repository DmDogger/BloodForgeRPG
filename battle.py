import constants as c
from stats import Stats

class Battle:
    def __init__(self, fighter_1, fighter_2):
        self.fighter_1 = fighter_1
        self.fighter_2 = fighter_2
        self.stats_handler = Stats()

    def _handle_turn(self, fighter_1, fighter_2):
        fighter_1_damage = fighter_1.attack()
        fighter_2.health -= fighter_1_damage
        print(f'Игрок: [{fighter_1.name}] нанес удар {fighter_1_damage} ед.\
              Здоровье {fighter_2.name} - [{fighter_2.health}]')
        
        if not fighter_2.is_alive():
            print(f'Победитель: {fighter_1.name}')
            self.stats_handler.record_win(fighter_1, fighter_2)
            return True
        return False
    
    def _print_start_battle(self):
        print(f'--------- Внимание: Начался бой -----------\n\
              ----{self.fighter_1} VS {self.fighter_2} ----\n\
              -----------------------------------------------')   


  

    def fight(self):
        # Счетчик раунда
        round_counter = 0
        print(f'Раунд: {round_counter}')

        # Выводим начальное сообщение о начале боя
        self._print_start_battle()

        # game-loop, начало боя
        while self.fighter_1.is_alive() and self.fighter_2.is_alive():
            if round_counter >= c.ROUND_TIMEOUT:
                print(f'Игроки {self.fighter_1.name} и {self.fighter_2.name} изнеможены')
                print(f'Объявляется ничья!')
                self.stats_handler.make_draw(self.fighter_1, self.fighter_2)
                break

            if self._handle_turn(self.fighter_1, self.fighter_2):
                self.stats_handler.print_all_stats(self.fighter_1)
                break

            if self._handle_turn(self.fighter_2, self.fighter_1):
                self.stats_handler.print_all_stats(self.fighter_2)
                break

            round_counter += 1