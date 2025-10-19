from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from character import Player, Enemy # type: ignore

# логгеры: ConsoleLogger(done), JsonLogger(in progress), FileLogger(in progress), SilentLogger(in progress)

class Logger(ABC):
    @abstractmethod
    def log_attack(self, attacker: Player | Enemy , defender: Player | Enemy, attack_damage: int | float) -> None: pass

    @abstractmethod
    def log_victory(self, winner: Player | Enemy) -> None: pass

    @abstractmethod
    def log_start_battle(self, attacker: Player | Enemy, defender: Player | Enemy) -> None: pass

    @abstractmethod
    def log_round_changing(self, round_counter: int) -> None: pass

    @abstractmethod
    def log_make_draw(self, attacker: Player | Enemy, defender: Player| Enemy) -> None: pass

    @abstractmethod
    def log_end_battle(self, attacker: Player | Enemy, defender: Player | Enemy) -> None: pass

    @abstractmethod
    def log_msg(self, string: str) -> None: pass



class ConsoleLogger(Logger):
    def log_attack(self, attacker: Player | Enemy, defender: Player | Enemy, attack_damage: int | float):
        '''Метод выводит в консоль сообщение об атаке игрока / противника и его уроне'''
        logging.info(f'[{attacker.name}] атаковал -> {defender.name} и нанес удар -[{attack_damage:.2f}] ед.')
        logging.info(f'У [{defender.name}] остается [{defender.health:.2f} из 100] HP ')


    def log_victory(self, winner: Player | Enemy): 
        '''Метод выводит в консоль сообщение о победе игрока / противника'''
        logging.info(' ')
        logging.info(f'Победитель в сегодняшней схватке: [{winner.name}]')
        

    def log_start_battle(self, attacker: Player | Enemy, defender: Player | Enemy): 
        logging.info('-' * 25 + ' Внимание ! ' + '-' * 25  + '|')
        logging.info(f'Начался бой между {attacker.name} [{attacker.level} ур.] и {defender.name} [{defender.level} ур.]  |')
        logging.info('-' * 62 + '|')

    def log_round_changing(self, round_counter: int): 
       logging.info('^' * 25)
       logging.info(f'Начался новый раунд: {round_counter}')
       logging.info('^' * 25)
    

    def log_make_draw(self, attacker: Player | Enemy, defender: Player| Enemy): 
        '''Метод выводит в консоль сообщение о ничьей'''
        logging.info('Объявляется ничья!')
        logging.info('и бой подходит к концу, потому что бойцы изнеможены')
        logging.info(f'{attacker.name} и {defender.name} отправляются на отдых')

    def log_end_battle(self, attacker: Player | Enemy, defender: Player | Enemy): 
        '''Метод выводит в консоль сообщение об окончании боя'''
        logging.info('-' * 10 + ' Внимание ! ' + '-' * 10 )
        logging.info(f'Бой между {attacker.name} и {defender.name} завершился')

    def log_msg(self, string: str):
        '''Метод принимает строку и печатает лог этой строки'''
        logging.info(string)






