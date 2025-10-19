from __future__ import annotations
import logging
import constants as c
from stats import StatsManager # type: ignore
from random import shuffle
from character import Player, Enemy, Character # type: ignore
from logger import Logger, ConsoleLogger # type: ignore

class BattleEngine:
    def __init__(self, attacker: Player | Enemy, defender: Player | Enemy, stats_manager: StatsManager, logger: Logger) -> None:
        self.attacker = attacker
        self.defender = defender
        self.stats_manager = stats_manager # Stats_manager будет гибким
        self.logger = logger
        self.round_counter = 1

    def _handle_turn(self, attacker: Player | Enemy, defender: Player | Enemy) -> bool:
        attacker_damage = attacker.attack() 
        defender.health -= attacker_damage
        self.logger.log_attack(attacker, defender, attacker_damage) #LOGGING ATTACK
    
        if not defender.is_alive():
            return True
        return False
    
    def _shuffle_fighters(self) -> list:
        fighters = [self.attacker, self.defender]
        shuffle(fighters)
        return fighters
    
    def _round_timeout(self) -> bool:
        if self.round_counter >= c.ROUND_TIMEOUT:
            return True
        return False
    
    def _turn_round(self) -> None:
         self.round_counter += 1
    
    def fight(self) -> None:
        
        fighters = self._shuffle_fighters() # SHUFFLING FIGHTERS (WHO IS ATTACKING FIRST?)
        self.logger.log_start_battle(fighters[0], fighters[1]) 
        ### START OF THE BATTLE ###
        while self.attacker.is_alive() and self.defender.is_alive():
            self.logger.log_round_changing(self.round_counter)
            if self._round_timeout():
                self.stats_manager.make_draw(self.attacker, self.defender)
                self.logger.log_make_draw(fighters[0], fighters[1]) #-> it doesnt matter whos first
                break

            if self._handle_turn(fighters[0], fighters[1]): 
                self.stats_manager.record_victory(fighters[0], fighters[1])
                self.logger.log_victory(fighters[0])
                break

            if self._handle_turn(fighters[1], fighters[0]):
                self.stats_manager.record_victory(fighters[1], fighters[0])
                self.logger.log_victory(fighters[1])
                break
            
            self._turn_round() #-> round changer
        ### END OF THE BATTLE ### 
        report = self.stats_manager.format_stats(fighters[0], fighters[1])
        self.logger.log_end_battle(fighters[0], fighters[1])
        self.logger.log_msg(report)