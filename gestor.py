from flask import Flask, request, send_file, redirect, send_from_directory, render_template
import db
import dbexport

website = Flask(__name__)

@website.route('/enviament', methods=['GET', 'POST'])
def enviament():
    if request.method == 'POST':
        user = request.form.get('user')
        task = request.form.get('task')
        password = request.form.get('password')

        # Handle file upload
        code_file = request.files['code']
        if code_file and code_file.filename.endswith('.py'):
            code = code_file.read().decode('utf-8')
        else:
            return '''
            <head>
            <title>Tramesa</title>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
            </head>
            <h1>Estat de la tramesa: Format de l'arxiu incorrecte, revisa que acabi en .py</h1>
            <a href="/">Torna</a>
            '''

        save_status = db.save_submission(user, password, task, code)
        return f'''
            <head>
            <title>Tramesa</title>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
            </head>
            <h1>Estat de la tramesa: {save_status}</h1>
            <a href="/">Torna</a>
            '''
    else:
        tasks = db.get_tasks()
        users = db.get_users()
        userlist = ''.join(f'<option value="{user[0]}">{user[2]}</option>' for user in users)
        options = ''.join(f'<option value="{task[0]}">{task[1]}</option>' for task in tasks)
        return render_template('enviament.html', options=options, userlist=userlist)

#THIS IS ALL WRONG I WANT TO DIE
qualifs = {
    0: 'NQ',
    1: 'NA',
    2: 'AS',
    3: 'AN',
    4: 'AE'
    }

@website.route('/estat')
def estat():
    tasks = db.get_tasks()
    users = db.get_users()
    user_task_status = []

    for user in users:
        user_status = {'user': user[2]}  # Use the display name directly from the user tuple
        for task in tasks:
            submitted_tasks = db.get_submitted_tasks(user[0])
            if task[0] in [t[0] for t in submitted_tasks]:
                grade = db.get_grade(user[0], task[0])
                #replace grade with qualification
                grade = qualifs[int(grade)]
                user_status[task[1]] = f"✅ - {grade}"  # Green emoji for submitted task
            else:
                user_status[task[1]] = "❌"  # Red emoji for not submitted task
        user_task_status.append(user_status)

    return render_template('estat.html', tasks=[task[1] for task in tasks], user_task_status=user_task_status)

@website.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'GET':
        tasks = db.get_tasks()
        users = db.get_users()
        userlist = ''.join(f'<option value="{user[0]}">{user[2]}</option>' for user in users)
        options = ''.join(f'<option value="{task[0]}">{task[1]}</option>' for task in tasks)
        return render_template('consulta_form.html', options=options, userlist=userlist)
    else: #POST
        user = request.form.get('user')
        task = request.form.get('task')
        password = request.form.get('password')
        status, code = db.get_submission(user, password, task)
        return render_template('consulta_result.html', status=status, code=code)

@website.route('/grade', methods=['GET', 'POST']) 
def grade():
    if request.method == 'GET':
        tasks = db.get_tasks()
        users = db.get_users()
        admins = db.get_admin_users()
        userlist = ''.join(f'<option value="{user[0]}">{user[2]}</option>' for user in users)
        options = ''.join(f'<option value="{task[0]}">{task[1]}</option>' for task in tasks)
        adminlist = ''.join(f'<option value="{user[0]}">{user[2]}</option>' for user in admins)
        return render_template('grade_form.html', options=options, userlist=userlist, adminlist=adminlist, status='')
    else:
        user = request.form.get('user')
        task = request.form.get('task')
        grade = request.form.get('grade')
        adminuser = request.form.get('adminuser')
        password = request.form.get('password')
        status = db.grade_submission(user, task, grade, adminuser, password)
        statustag = f"<h3>Estat de la petició: {status}</h3>"
        #Show form again
        tasks = db.get_tasks()
        users = db.get_users()
        userlist = ''.join(f'<option value="{user[0]}">{user[2]}</option>' for user in users)
        options = ''.join(f'<option value="{task[0]}">{task[1]}</option>' for task in tasks)
        adminlist = ''.join(f'<option value="{user[0]}">{user[2]}</option>' for user in users if user[3])
        return render_template('grade_form.html', options=options, userlist=userlist, adminlist=adminlist, statustag=statustag)


@website.route('/')
def index():
    return render_template('index.html')

@website.route('/descarrega')
def download():
    #Create submissions .zip file
    dbexport.export_submissions()
    #Return submissions .zip file and redirect to index
    return send_file('submissions.zip', as_attachment=True)

@website.route('/favicon.ico')
def favicon():
    return website.send_static_file('favicon.ico')

#Make any 500 error show contact info
@website.errorhandler(500)
def server_error(e):
    return """
        <html>
            <head>
                <title>500 Error</title>
                <link rel="stylesheet" type="text/css" href="/static/styles.css">
            </head>
            <body>
                <h1>500 Error</h1>
                <h3>Hi ha hagut un error al servidor. Contacta amb l'administrador.</h3>
                <p href=https://giuli.cat>Creat per: Pau Giuli</p>
            </body>
        </html>
    """

#Make any 404 error redirect to the index page
@website.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == '__main__':
    website.run(debug=True)