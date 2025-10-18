class Stats:
    '''Метод для работы со статистикой'''

    display_stats = {
        'total_wins' : 'Всего побед',
        'total_loses' : 'Всего поражений',
        'total_fights' : 'Всего боев',
        'total_draws' : 'Всего ничьих'
   }
    
    def record_win(self, winner, loser):
        '''Обновляем статистику при победе'''
        winner.stats['total_wins'] += 1
        winner.stats['total_fights'] += 1
        loser.stats['total_loses'] += 1
        loser.stats['total_fights'] += 1

    def make_draw(self, fighter_1, fighter_2):
        '''Обновляем статистику при ничьей'''
        fighter_1.stats['total_fights'] += 1
        fighter_1.stats['total_draws'] += 1
        fighter_2.stats['total_draws'] += 1
        fighter_2.stats['total_fights'] += 1   

    def print_all_stats(self, character):
        '''Печатаем статистику игрока'''
        print(f'--- Статистика {character.name} ---')
        for key, value in character.stats.items():
            label = Stats.display_stats.get(key, key)
            print (f'{label}: {value}')
        print('-' * 20)
