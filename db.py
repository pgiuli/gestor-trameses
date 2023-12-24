import sqlite3

def create_database():
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    # Create table for task submissions
    c.execute('''CREATE TABLE IF NOT EXISTS trameses
        (user text, taskid text, response text)''')
    # Create table for available tasks
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
        (taskid text, name text)''')
    # Create table for users
    c.execute('''CREATE TABLE IF NOT EXISTS users
        (user text, password text)''')
    conn.commit()
    conn.close()


def save_submission(user, password, taskid, response):
    # Check if user exists and password is correct
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user=?", (user,))
    user = c.fetchone()
    if user is None:
        return 'Usuari no trobat'
    if password != user[1]:
        return 'Contrasenya incorrecta'
    # Save submission
    # Check if submission already exists
    c.execute("SELECT * FROM trameses WHERE user=? AND taskid=?", (user[0], taskid))
    submission = c.fetchone()
    if submission is not None:
        # Update submission
        c.execute("UPDATE trameses SET response=? WHERE user=? AND taskid=?", (response, user[0], taskid))
        conn.commit()
        conn.close()
        return 'Tramesa actualitzada satisfactòriament!'
    else:
        # Create submission
        c.execute("INSERT INTO trameses VALUES (?, ?, ?)", (user[0], taskid, response))
        conn.commit()
        conn.close()
        return 'Tramesa enviada satisfactòriament!'

def get_submitted_tasks(user):
    #Get all submitted taskid by user
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("SELECT taskid FROM trameses WHERE user=?", (user,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def delete_submission(user, taskid):
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("DELETE FROM trameses WHERE user=? AND taskid=?", (user, taskid))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task(taskid, name):
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks VALUES (?, ?)", (taskid, name))
    conn.commit()
    conn.close()

def delete_task(taskid):
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE taskid=?", (taskid,))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

def add_user(user, password):
    # Check if user exists
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user=?", (user,))
    testuser = c.fetchone()
    if testuser is not None:
        return 'Usuari ja existent'
    # Save user
    c.execute("INSERT INTO users VALUES (?, ?)", (user, password))
    conn.commit()
    conn.close()

def delete_user(user):
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE user=?", (user,))
    conn.commit()
    conn.close()


def add_test_tasks():
    add_task('introduccio', 'Introducció')
    add_task('funcions', 'Funcions')
    add_task('final', 'Tramesa final')

if __name__ == '__main__':
    create_database()
    add_test_tasks()
