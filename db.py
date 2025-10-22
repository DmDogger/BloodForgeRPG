import sqlite3 
import logging
from msgs import ERR_MESSAGES, INFO_MESSAGES

class Database:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._create_table()

    def _conn(self) -> sqlite3.Connection | None:
        '''Метод для создания объекта-коннектора'''
        try:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row # удобный формат дикт
            return connection # создаем объект коннектора и возвращаем для последующей работы
        except sqlite3.Error as e:
            logging.error(f'Ошибка подключения к БД: {e}')
            return None
    
    def _create_table(self) -> None:
        '''Метод для создания таблицы игроков если не существует'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return
        try:
            with conn:
                conn.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        total_fights INTEGER NOT NULL DEFAULT 0,
        total_wins INTEGER NOT NULL DEFAULT 0,
        total_losses INTEGER NOT NULL DEFAULT 0,
        total_draws INTEGER NOT NULL DEFAULT 0 
                             )               
                             ''')
                logging.info(INFO_MESSAGES['TABLE_CREATED_SUCCESS'])
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
        finally:
            conn.close()

    def user_exists(self, user: str) -> bool:
        '''Метод проверяет существует ли пользователь в таблице Базы Данных'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return False
        try:
            with conn:
                cursor = conn.execute('SELECT EXISTS(SELECT 1 FROM Users WHERE username = ?)', (user,))
                result = cursor.fetchone()
                logging.info(INFO_MESSAGES['OPERATION_SUCCESS'])
                return bool(result[0])
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
            return False
        finally:
            conn.close()

    def add_user(self, user: str) -> None:
        '''Метод добавлят нового игрока в таблицу Базы Данных'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return
        try:
            with conn:
                conn.execute('INSERT INTO Users (username) VALUES (?)', (user,))
                logging.info(INFO_MESSAGES['OPERATION_SUCCESS'])
                logging.info(f'{user} был добавлен в таблицу успешно!')
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
        finally:
            conn.close()

    def update_user_stats(self, user: str, stats: dict) -> None:
        '''Метод обновляет статистику игрока'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return
        try:
            with conn:
                conn.execute('''
                        UPDATE Users SET
                            total_fights = ?,
                            total_wins = ?,
                            total_losses = ?,
                            total_draws = ?
                        WHERE username = ?''', (stats['total_fights'], stats['total_wins'],\
                                            stats['total_losses'], stats['total_draws'], user))
                logging.info(INFO_MESSAGES['OPERATION_SUCCESS'])
                logging.info(f'Юзер: {user} успешно обновлен!')
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
        finally:
            conn.close()

    def delete_user(self, user: str) -> None:
        '''Метод удаляет игрока по имени'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return
        try:
            with conn:
                conn.execute('DELETE FROM Users WHERE username = ?', (user,))
                logging.info(INFO_MESSAGES['OPERATION_SUCCESS'])
                logging.info(f'Пользователь {user} успешно удален из базы данных!')        
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
        finally:
            conn.close()


    def get_all_users(self) -> list | None: 
        '''Метод получает список имен игроков'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return None
        try:
            with conn:
                cursor = conn.execute('SELECT username FROM Users')
                res = cursor.fetchall()
                res = [line['username'] for line in res]
                logging.info(INFO_MESSAGES['OPERATION_SUCCESS'])
                return res
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
        finally:
            conn.close()


    def get_statistic(self, char: str) -> dict | None:
        '''Метод для получения статистики игрока в виде словаря'''
        conn = self._conn()
        if conn is None:
            logging.error(ERR_MESSAGES['CONNECTION_ERROR'])
            return
        try:
            with conn:
                stats = conn.execute('SELECT * FROM Users WHERE username = ?', (char,))
                stats = stats.fetchone()
                if stats is None:
                    logging.error(ERR_MESSAGES['USER_NOT_FOUND'])
                    return None
                return dict(stats)
        except sqlite3.Error as e:
            logging.error(ERR_MESSAGES['SQLITE3_ERROR'] + str(e))
        finally:
            conn.close()


