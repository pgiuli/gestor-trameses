from flask import Flask, request, send_file, redirect, send_from_directory, render_template
import db
import dbexport

website = Flask(__name__)

@website.route('/enviament', methods=['GET', 'POST'])
def enviament():
    if request.method == 'POST':
        print('Saving Submission')
        user = request.form.get('user')
        task = request.form.get('task')
        password = request.form.get('password')

        # Handle file upload
        code_file = request.files['code']
        if code_file and code_file.filename.endswith('.py'):
            code = code_file.read().decode('utf-8')
        else:
            return 'Invalid file type. Only .py files are allowed.'

        save_status = db.save_submission(user, password, task, code)
        print(save_status)
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