import psycopg2
from psycopg2 import sql
from tqdm import tqdm

from models import Employee


class Database:
    def __init__(self, database, user, password, host, port):

        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(50),
            birth_date DATE,
            gender CHAR(6)
        )
        ''')
        self.conn.commit()

    def create_employee(self, employee):
        self.cursor.execute(sql.SQL(
            '''INSERT INTO employees (full_name, birth_date, gender)
            VALUES (%s, %s, %s)'''),
                            [employee.full_name,
                             employee.birth_date,
                             employee.gender]
                            )
        self.conn.commit()

    def save_employees(self, employees):
        data = [
            (employee.full_name, employee.birth_date, employee.gender)
            for employee in tqdm((employees),
                                 desc="Сохраняем сотрудников в базу")]
        args_str = ','.join(
            self.cursor.mogrify("(%s,%s,%s)", x).decode('utf-8') for x in data)
        self.cursor.execute(
            '''INSERT INTO employees (
                full_name,
                birth_date,
                gender)
            VALUES''' + args_str)
        self.conn.commit()

    def get_employees(self):
        """Выбираем уникальные full_name - birth_date."""
        self.cursor.execute('''
        SELECT DISTINCT ON (full_name, birth_date)
        full_name, birth_date, gender
        FROM employees
        ORDER BY full_name, birth_date
        ''')
        rows = self.cursor.fetchall()
        employees = [Employee(row[0],
                              row[1].strftime('%Y-%m-%d'),
                              row[2]) for row in rows]
        return employees

    def get_male_employees_with_fname(self):
        self.cursor.execute('''
        SELECT full_name, birth_date, gender
        FROM employees
        WHERE gender = 'Male' AND full_name LIKE 'F%'
        ''')
        rows = self.cursor.fetchall()
        employees = [Employee(row[0], row[1].strftime('%Y-%m-%d'), row[2])
                     for row in rows]
        return employees

    def create_index(self):
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_gender_fullname
        ON employees (gender, full_name);
        ''')
        self.conn.commit()

    def stat(self):
        self.cursor.execute('SELECT count(*) FROM employees;')
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
