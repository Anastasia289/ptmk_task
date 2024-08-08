from constants import (DATABASE, HOST, PASSWORD, PORT, USER)
from database_postgres import Database
from controller import Controller


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

# def check_db():
#     return2


def main():
    database = Database(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE,
        )
    controller = Controller(database)
    action = 0
    while action != '7':
        action = get_action()
        controller.act(action)
    database.close()


if __name__ == "__main__":
    main()
