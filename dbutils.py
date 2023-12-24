import db
import dbexport

while True:
    option = input('''
    1. Create database
    2. Add task
    3. Delete task
    4. List tasks
    5. Export submissions
    6. Delete submission (by user and task)
    7. Create user
    8. Delete user
    9. List users
    10. Get submitted tasks
    11. Exit
    
    ''')
    match option:
        case '1':
            db.create_database()
        case '2':
            taskid = input('Identificador: ')
            description = input('Nom: ')
            db.add_task(taskid, description)
        case '3':
            taskid = input('Identificador: ')
            db.delete_task(taskid)
        case '4':
            tasks = db.get_tasks()
            for task in tasks:
                print(f'{task[0]} - {task[1]}')
        case '5':
            dbexport.export_submissions()
        case '6':
            user = input('Usuari: ')
            taskid = input('Identificador (tasca): ')
            db.delete_submission(user, taskid)
        case '7':
            user = input('Usuari: ')
            password = input('Contrasenya: ')
            db.add_user(user, password)
        case '8':
            user = input('Usuari: ')
            db.delete_user(user)
        case '9':
            users = db.get_users()
            for user in users:
                print(f'{user[0]}')
        case '10':
            user = input('Usuari: ')
            tasks = db.get_submitted_tasks(user)
            for task in tasks:
                print(f'{task[0]}')
        case '11':
            exit()
        case _:
            print('Opció incorrecta')
