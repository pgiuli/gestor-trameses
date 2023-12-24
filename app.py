from flask import Flask, request, send_file, redirect, send_from_directory
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
        print(save_status)
        return f'''
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
            <h1>Estat de la tramesa: {save_status}</h1>
            <a href="/">Torna</a>
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

@flask_app.route('/descarrega')
def download():
    #Create submissions .zip file
    dbexport.export_submissions()
    #Return submissions .zip file and redirect to index
    return send_file('submissions.zip', as_attachment=True)

@flask_app.route('/favicon.ico')
def favicon():
    return flask_app.send_static_file('favicon.ico')

#Make any 500 error show contact info
@flask_app.errorhandler(500)
def server_error(e):
    return """
        <html>
            <head>
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
@flask_app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == '__main__':
    flask_app.run(debug=True)