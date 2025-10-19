from __future__ import annotations
from abc import ABC, abstractmethod
import json
import os
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
    def __init__(self, file):
        self.file = file

    def _load_stats(self) -> dict:
        '''Загружаем статистику из JSON-объекта'''
        if os.path.exist(self.file) and os.path.getsize(self.file) > 0:
            try:
                with open(self.file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        else:
            return {}
        
# Будет реализация JSON + SQLite
# Here will be realised class of SQLite Stats