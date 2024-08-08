import logging
import sys

from psycopg2 import Error

from constants import DATABASE, HOST, PASSWORD, PORT, USER
from controller import Controller
from database_postgres import Database

logger = logging.getLogger(__name__)


def get_action():
    while True:
        try:
            user_input = input(
                '\n Что хотите сделать? Введите число: \n'
                '1 - создать таблицу employees, '
                '2 - сделать в нее запись, '
                '3 - вывести все строки, \n'
                '4 - заполнить 1000000 строк, '
                '5 - получить выборку, '
                '6 - провести оптимизацию базы, \n'
                '7 - завершить программу \n'
                               )
            if int(user_input) > 0 and int(user_input) < 8:
                return user_input
            else:
                raise ValueError
        except ValueError:
            print('Такого варианта нет, выбирайте из имеющихся')


def main():
    try:
        database = Database(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE,
            )
    except (Exception, Error) as error:
        logger.critical('Программа принудительно остановлена.'
                        'Проверьте данные для подключения к бд',
                        error)
        sys.exit()

    controller = Controller(database)
    action = 0
    while action != '7':
        action = get_action()
        controller.act(action)
    database.close()


if __name__ == "__main__":
    log_format = ('%(asctime)s [%(levelname)s] - '
                  '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s')
    logging.basicConfig(
        level=logging.INFO,
        filename='program.log',
        filemode='w',
        encoding='utf-8',
        format=log_format,)
    logger.setLevel(logging.DEBUG)
    main()
