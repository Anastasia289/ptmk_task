from datetime import datetime


class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        self.gender = gender

    def calculate_age(self):
        today = datetime.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) <
            (self.birth_date.month, self.birth_date.day)  #
        )
        return age

    def save(self, db):
        if db.create_employee(self):
            return True
        return False

    def __str__(self):
        return (f"{self.full_name}, "
                f" {self.birth_date.strftime('%Y-%m-%d')}, {self.gender}")
