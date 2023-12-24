from flask import Flask, request
import db
import dbexport

flask_app = Flask(__name__)

@flask_app.route('/enviament', methods=['GET', 'POST'])
def enviament():
    if request.method == 'POST':
        print('Saving Submission')
        user = request.form.get('user')
        task = request.form.get('task')
        code = request.form.get('code')
        password = request.form.get('password')
        save_status = db.save_submission(user, password, task, code)
        return f'''
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
            <h1>Estat de la tramesa: {save_status}</h1>
            <a href="/">Torna a l'inici.</a>
            '''
    else:
        print('Showing Form')
        tasks = db.get_tasks()
        options = ''.join(f'<option value="{task[0]}">{task[1]}</option>' for task in tasks) #Get taskid and task name from tasks
        return f'''
             <link rel="stylesheet" type="text/css" href="/static/styles.css">
            <form method="POST">
                Usuari: <input type="text" name="user"><br>
                Contrasenya: <input type="password" name="password"><br>
                Tasca: <select name="task">
                    {options}
                </select><br>
                Codi: <textarea name="code"></textarea><br>
                <input type="submit" value="Submit">
            </form>
        '''

@flask_app.route('/')
def index():
    return """
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="/static/styles.css">
            </head>
            <body>
                <h1>Gestor de trameses de Programació i Robòtica</h1>
                <p>Utilitza aquesta pàgina per entregar les teves tasques.</p>
                <h3 href=https://giuli.cat>Creat per: Pau Giuli</h3>
                <a href=https://github.com/pgiuli/gestor-trameses>GitHub Repository</a>
                <a href="/enviament">Envia una tasca</a>
            </body>
        </html>
    """
#Make any 404 error redirect to the index page
@flask_app.errorhandler(404)
def page_not_found(e):
    return index()


if __name__ == '__main__':
    flask_app.run(debug=True)