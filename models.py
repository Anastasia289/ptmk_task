from datetime import datetime

from dateutil.relativedelta import relativedelta


class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        self.gender = gender

    def calculate_age(self):
        today = datetime.today()
        age = relativedelta(today, self.birth_date).years
        return age

    def save(self, db):
        if db.create_employee(self):
            return True
        return False

    def __str__(self):
        return (f"{self.full_name}, "
                f" {self.birth_date.strftime('%Y-%m-%d')}, {self.gender}")
