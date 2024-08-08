import random
import time
from datetime import datetime

from faker import Faker
from psycopg2 import Error

from constants import (CHAR_LEN, COUNT_EMPLOYEES_TO_CREATE,
                       COUNT_NAME_STARTWITH_F, DATABASE, HOST, MAX_AGE,
                       MIN_AGE, PASSWORD, PORT, USER)
from database_postgres import Database
from models import Employee
from tqdm import tqdm


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
                '7 - тестовая '
                '8 - завершить программу \n'
                               )
            if user_input == '8':
                break
            elif int(user_input) > 0 and int(user_input) < 8:
                return user_input
            else:
                raise ValueError
        except ValueError:
            print('Такого варианта нет, выбирайте из имеющихся')
    return user_input


def get_date():
    while True:
        try:
            user_input = input('\n Введите дату рождения в формате %Y-%m-%d')
            date = datetime.strptime(user_input, "%Y-%m-%d")
            if date and check_date(date):
                return user_input
            else:
                raise ValueError
        except ValueError:
            print('Дата введена неверно, используйте формат %Y-%m-%d')


def get_gender():
    while True:
        try:
            user_input = input('''\n Введите пол сотрудника.
                               Может быть Male или Female''')
            check_gender(user_input)
            if check_gender(user_input):
                return user_input
            else:
                raise ValueError
        except ValueError:
            print('''Пол введен неверно. Может быть Male или Female.
                  Введите пол: _''')


def check_gender(gender):
    if gender == 'Male' or gender == 'Female':
        return True
    return False


def check_date(date):
    today = datetime.today()
    if today.year - date.year < MIN_AGE:
        print('Работа только для совершеннолетних')
        return False
    elif today.year - date.year > MAX_AGE:
        print('Подозрительно возрастной кандидат')
        return False
    return True


def create_a_lot_of_employees():
    employees = []
    faker = Faker()
    for i in tqdm(range(COUNT_EMPLOYEES_TO_CREATE),
                  desc="Генерируем данные сотрудников"):  
        name = faker.name()
        birth_date = faker.date_of_birth(
            minimum_age=MIN_AGE,
            maximum_age=MAX_AGE).strftime('%Y-%m-%d')
        gender = random.choice(['Male', 'Female'])
        employees.append(Employee(name, birth_date, gender))

    for i in tqdm(range(COUNT_NAME_STARTWITH_F),
                  desc="Генерируем мужчин с именами на F"):
        name = 'F' + faker.name()  # здесь точно можно лучше
        birth_date = faker.date_of_birth(
            minimum_age=MIN_AGE,
            maximum_age=MAX_AGE).strftime('%Y-%m-%d')
        gender = 'Male'
        employees.append(Employee(name, birth_date, gender))
    return employees


def list_employees(employees):
    for employee in employees:
        age = employee.calculate_age()  # Расчет возраста сотрудника
        print(f'{employee.full_name:<{CHAR_LEN}} '
              f' {employee.birth_date.strftime('%Y-%m-%d')} '
              f'{employee.gender} {age} полных лет')


def get_employee():
    name = input('\n Введите имя')
    date = get_date()
    gender = get_gender()
    return Employee(name, date, gender)


def main():
    database = Database(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE,
        )

    action = get_action()

    if action == '1':
        try:
            database.create_table()
            print('Таблица создана')
        except (Exception, Error) as error:
            print("Ошибка при создании таблицы", error)

    if action == '2':
        try:
            employee = get_employee()
            employee.save(database)
            print('Сотрудник добавлен')
        except (Exception, Error) as error:
            print("Ошибка при создании сотрудника", error)

    if action == '3':
        try:
            employees = database.get_employees()
            if not employees:
                print('База пуста')
            list_employees(employees)
            print(f'Всего строк: {database.stat()}')
        except (Exception, Error) as error:
            print("Ошибка при получении списка сотрудников", error)

    if action == '4':
        try:
            employees = create_a_lot_of_employees()
            database.save_employees(employees)

        except (Exception, Error) as error:
            print("Ошибка при создании множества сотрудников", error)

    if action == '5':
        try:
            start_time = time.time()
            employees = database.get_male_employees_with_fname()
            end_time = time.time()
            final_time = end_time - start_time
            list_employees(employees)
            print(f'Время выполнения:  {final_time}')
        except (Exception, Error) as error:
            print("Ошибка при выборке", error)

    if action == '6':
        try:
            database.create_index()
            print("Индексы созданы")
        except (Exception, Error) as error:
            print("Ошибка при создании индексов", error)

    if action == '7':
        try:
            print(f'Всего строк: {database.stat()}')
            # print("Индексы созданы")
        except (Exception, Error) as error:
            print("Ошибка", error)


if __name__ == "__main__":
    main()
