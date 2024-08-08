import logging
import random
import time
from datetime import datetime

from faker import Faker
from psycopg2 import Error
from tqdm import tqdm

from constants import (CHAR_LEN, COUNT_EMPLOYEES_TO_CREATE,
                       COUNT_NAME_STARTWITH_F, MAX_AGE, MIN_AGE)
from models import Employee

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, database):
        self.database = database

    def act(self, action):
        if action == '1':
            self.create_table()
        if action == '2':
            self.add_employee()
        if action == '3':
            self.get_employees()
        if action == '4':
            self.create_employees()
        if action == '5':
            self.get_male_employees_with_fname()
        if action == '6':
            self.create_index()

    def create_table(self):
        try:
            self.database.create_table()
            logger.info('Таблица создана')
            print('Таблица создана')
        except (Exception, Error) as error:
            logger.error("Ошибка при создании таблицы", error)

    def get_date(self):
        while True:
            try:
                msg = 'Дата введена неверно, используйте формат %Y-%m-%d'
                user_input = input(
                    '\n Введите дату рождения в формате %Y-%m-%d')
                date = datetime.strptime(user_input, "%Y-%m-%d")
                today = datetime.today()
                if today.year - date.year < MIN_AGE:
                    msg = 'Работа только для совершеннолетних'
                    raise ValueError
                elif today.year - date.year > MAX_AGE:
                    msg = 'Подозрительно возрастной кандидат'
                    raise ValueError
                else:
                    return user_input
            except ValueError:
                logger.error(msg)

    def get_gender(self):
        while True:
            try:
                user_input = input('''\n Введите пол сотрудника.
                                   Может быть Male или Female''')
                if user_input == 'Male' or user_input == 'Female':
                    return user_input
                else:
                    raise ValueError
            except ValueError:
                logger.error('''Пол введен неверно. Может быть Male или Female.
                      Введите пол: _''')

    def get_employee(self):
        name = input('\n Введите имя')
        date = self.get_date()
        gender = self.get_gender()
        return Employee(name, date, gender)

    def add_employee(self):
        try:
            employee = self.get_employee()
            employee.save(self.database)
            logger.info('Сотрудник добавлен')
            print('Сотрудник добавлен')
        except (Exception, Error) as error:
            logger.error("Ошибка при создании сотрудника", error)

    def get_employees(self):
        try:
            if not self.database.get_employees():
                print('База пуста')
            self.list_employees(self.database.get_employees())
            logger.info('Получены данные из базы, всего строк: '
                        f'{self.database.stat()}.')
            print(f'Всего строк: {self.database.stat()}')
        except (Exception, Error) as error:
            logger.error("Ошибка при создании сотрудников", error)

    def create_a_lot_of_employees(self):
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

    def create_employees(self):
        try:
            employees = self.create_a_lot_of_employees()
            self.database.save_employees(employees)
        except (Exception, Error) as error:
            logger.error("Ошибка при создании множества сотрудников", error)

    def get_male_employees_with_fname(self):
        try:
            start_time = time.time()
            employees = self.database.get_male_employees_with_fname()
            end_time = time.time()
            final_time = end_time - start_time
            self.list_employees(employees)
            print(f'Время выполнения:  {final_time}')
            logger.info(f'Сотрудники на f получены за:  {final_time}')
        except (Exception, Error) as error:
            logger.error("Ошибка при выборке", error)

    def create_index(self):
        try:
            self.database.create_index()
            print("Индексы созданы")
            logger.info("Индексы созданы")
        except (Exception, Error) as error:
            logger.error("Ошибка при создании индексов", error)

    def list_employees(self, employees):
        for employee in employees:
            age = employee.calculate_age()
            print(f'{employee.full_name:<{CHAR_LEN}} '
                  f' {employee.birth_date.strftime('%Y-%m-%d')} '
                  f'{employee.gender} {age} полных лет')
