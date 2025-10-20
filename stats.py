from __future__ import annotations
from abc import ABC, abstractmethod
import json
import os
import logging
from character import Player, Enemy # type: ignore

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


    def record_victory(self, winner: Player | Enemy, loser: Player | Enemy) -> None:
        '''Метод записывает победу в JSON'''
        json_stats = self._load_stats() # ЗАГРУЗКА СТАТИСТИКИ
        # получаем ключи - имея победителя и проигравшего
        if not winner.name in json_stats:
            json_stats[winner.name] = { 'total_fights' : 0,
                                       'total_wins' : 0,
                                       'total_loses' : 0,
                                       'total_draws' : 0
            }

        if not loser.name in json_stats:
            json_stats[loser.name] = { 'total_fights' : 0,
                                       'total_wins' : 0,
                                       'total_loses' : 0,
                                       'total_draws' : 0
            }
            

           
        #записываем статистику победителю
        json_stats[winner.name]['total_fights'] += 1
        json_stats[winner.name]['total_wins'] += 1

        #записываем статистику 
        json_stats[loser.name]['total_fights'] +=1
        json_stats[loser.name]['total_loses'] += 1

        self._save_stats(json_stats)































    def make_draw(self, attacker, defender): #добавить аннотации
        json_data = self._load_stats()

        atckr_name = json_data.get(attacker.name, 'unkown_char_1')
        dfndr_name = json_data.get(defender.name, 'unkown_char_2')

        pass



        
# Будет реализация JSON + SQLite
# Here will be realised class of SQLite Stats