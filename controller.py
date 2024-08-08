# class Сontroller:
#     def __init__(self, database):
#         self.database = database
    
#     def actions(action):
#         if action == '1':
#             try:
#                 database.create_table()
#                 print('Таблица создана')
#             except (Exception, Error) as error:
#                 print("Ошибка при создании таблицы", error)

#         if action == '2':
#             try:
#             if not employee:
#                 employee = get_employee()
#             employee.save(database)
#             print('Сотрудник добавлен')
#         except (Exception, Error) as error:
#             print("Ошибка при создании сотрудника", error)

#     if action == '3':
#         try:
#             employees = database.get_all_employees()
#             if not employees:
#                 print('База пуста')
#             list_employees(employees)
#         except (Exception, Error) as error:
#             print("Ошибка при получении списка сотрудников", error)

#     if action == '4':
#         try:

#             employees = create_a_lot_of_employees()
#             database.save_employees_batch(employees)
#             print("Сотрудники созданы")

#         except (Exception, Error) as error:
#             print("Ошибка при создании множества сотрудников", error)

#     if action == '5':
#         try:
#             start_time = time.time()
#             employees = database.get_male_employees_with_fname()
#             end_time = time.time()
#             elapsed_time = end_time - start_time
#             list_employees(employees)
#             print(elapsed_time)
#         except (Exception, Error) as error:
#             print("Ошибка при выборке", error)

#     if action == '6':
#         try:
#             database.create_index()
#             print("Индексы созданы")
#         except (Exception, Error) as error:
#             print("Ошибка при создании индексов", error)
a = '1'
a = a.split(',')
print(*a.split(','))