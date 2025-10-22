from __future__ import annotations
from abc import ABC, abstractmethod
import json
import logging
from character import Player, Enemy
from db import Database
from msgs import ERR_MESSAGES

class StatsManager(ABC):
    '''Абстрактный класс для менеджера статистики'''

    display_stats = {
        'total_wins' : 'Всего побед',
        'total_loses' : 'Всего поражений',
        'total_fights' : 'Всего боев',
        'total_draws' : 'Всего ничьих'
   }

    @abstractmethod
    def record_victory(self, winner: Player | Enemy, loser: Player | Enemy) -> None:
        pass
    
    @abstractmethod
    def make_draw(self, attacker: Player | Enemy, defender: Player | Enemy) -> None:
        pass   
    
    
    def format_stats(self, attacker: Player | Enemy, defender: Player | Enemy) -> str:
        report = [f'--- Статистика {attacker.name} ---']
        #ATTACKER STATS IN STRING
        attacker_line = [f'{self.display_stats.get(key, key)}:{value}' for key, value in attacker.stats.items()]
        report.extend(attacker_line)
        report.append('-' * 34)

        #DEFENDER STATS IN STRING
        report.append(f'--- Статистика {defender.name} ---')
        defender_line = [f'{self.display_stats.get(key,key)}: {value}' for key, value in defender.stats.items()]
        report.extend(defender_line)
        report.append('-' * 34)
        return '\n'.join(report)
        

class InMemoryStats(StatsManager):
    '''Класс для работы со статистикой (Записывает статистику в память)'''
    display_stats = {
        'total_wins' : 'Всего побед',
        'total_loses' : 'Всего поражений',
        'total_fights' : 'Всего боев',
        'total_draws' : 'Всего ничьих'
   }
    
    def record_victory(self, winner: Player | Enemy, loser: Player | Enemy) -> None:
        '''Обновляем статистику при победе'''
        winner.stats['total_wins'] += 1
        winner.stats['total_fights'] += 1
        loser.stats['total_loses'] += 1
        loser.stats['total_fights'] += 1

    def make_draw(self, attacker: Player | Enemy, defender: Player | Enemy) -> None:
        '''Обновляем статистику при ничьей'''
        attacker.stats['total_fights'] += 1
        attacker.stats['total_draws'] += 1
        defender.stats['total_draws'] += 1
        defender.stats['total_fights'] += 1   

class JsonManagerStats(StatsManager):
    '''Класс для сохранения статистики в JSON-объект'''
    def __init__(self, filename):
        self.filename = filename

    def _load_stats(self) -> dict:
        '''Метод загружает статистику персонажа из JSON'''
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                jsondata = json.load(f)
                return jsondata
        except json.JSONDecodeError:
            return {}

    def _save_stats(self, data: dict) -> None:
        '''Метод сохраняет статистику в JSON'''
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                # Сохраняем статистику в файл, отступ: 3
                json.dump(data, f, ensure_ascii=False, indent=3)
        except (OSError, TypeError) as e:
            logging.error(f'Не удалось выполнить операцию. Ошибка {e}')

    def _create_user(self, user: Player | Enemy, json_data: dict) -> None:
        '''Метод создает запись о игроке в JSON-файле, если их нет'''
        if user.name not in json_data:
            json_data[user.name] = {
                'total_fights' : 0,
                'total_wins' : 0,
                'total_loses' : 0,
                'total_draws' : 0
        }


    def record_victory(self, winner: Player | Enemy, loser: Player | Enemy) -> None:
        '''Метод записывает победу в JSON'''
        json_data = self._load_stats() # ЗАГРУЗКА СТАТИСТИКИ
        '''Создаем пользователя, если его нет в JSON-файле'''
        self._create_user(winner, json_data)
        self._create_user(loser, json_data)
           
        #записываем статистику победителю
        json_data[winner.name]['total_fights'] += 1
        json_data[winner.name]['total_wins'] += 1

        #записываем статистику проигравшему
        json_data[loser.name]['total_fights'] +=1
        json_data[loser.name]['total_loses'] += 1

        self._save_stats(json_data)

    def make_draw(self, attacker: Player | Enemy, defender: Player | Enemy) -> None:
        '''Метод записывает ничью в JSON'''
        json_data = self._load_stats()
        self._create_user(attacker, json_data)
        self._create_user(defender, json_data)

        #записываем в статистику ничьи 
        json_data[attacker.name]['total_fights'] += 1
        json_data[attacker.name]['total_draws'] += 1
        json_data[defender.name]['total_fights'] += 1
        json_data[defender.name]['total_draws'] += 1
        
        self._save_stats(json_data)

class SQLiteManagerStats(StatsManager):
    '''Работает с статистикой в SQLite'''
    def __init__(self, db: Database, attacker: Player | Enemy, defender: Player | Enemy):
        self.db = db
        if not self.db.user_exists(attacker.name):
            self.db.add_user(attacker.name)
        if not self.db.user_exists(defender.name):
            self.db.add_user(defender.name)

    def record_victory(self, winner: Player | Enemy, loser: Player | Enemy) -> None:
        '''Метод записывает победу (победителю) и проигрыш (проигравшему) В БД'''
        winner_stat = self.db.get_statistic(winner.name) # забираем дикт со статой
        loser_stat = self.db.get_statistic(loser.name)
        
        if winner_stat is None or loser_stat is None:
            logging.error(ERR_MESSAGES['DB_RETURNED_NONE'])
            return
        
        winner_stat['total_fights'] += 1
        winner_stat['total_wins'] += 1

        loser_stat['total_fights'] += 1
        loser_stat['total_losses'] += 1

        self.db.update_user_stats(winner.name, winner_stat)
        self.db.update_user_stats(loser.name, loser_stat)

    def make_draw(self, attacker: Player | Enemy, defender: Player | Enemy) -> None:
        '''Метод записывает игрокам ничьи'''
        attacker_stat = self.db.get_statistic(attacker.name)
        defender_stat = self.db.get_statistic(defender.name)

        if attacker_stat is None or defender_stat is None:
            logging.error(ERR_MESSAGES['DB_RETURNED_NONE'])
            return
        
        attacker_stat['total_fights'] += 1
        attacker_stat['total_draws'] += 1
        defender_stat['total_fights'] += 1
        defender_stat['total_draws'] += 1

        self.db.update_user_stats(attacker.name, attacker_stat)
        self.db.update_user_stats(defender.name, defender_stat)


