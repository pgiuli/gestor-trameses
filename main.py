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
            <style>
                h1 {{
                    color: #4CAF50;
                    text-align: center;
                }}
                a {{
                    display: block;
                    width: 200px;
                    height: 50px;
                    margin: 20px auto;
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    line-height: 50px;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a:hover {{
                    background-color: #45a049;
                }}
            </style>
            <h1>Estat de la tramesa: {save_status}</h1>
            <a href="/">Torna a l'inici.</a>
            '''
    else:
        print('Showing Form')
        tasks = db.get_tasks()
        options = ''.join(f'<option value="{task[0]}">{task[1]}</option>' for task in tasks) #Get taskid and task name from tasks
        return f'''
             <style>
                form {{
                    width: 300px;
                    margin: 0 auto;
                }}
                input, select {{
                    width: 100%;
                    margin: 10px 0;
                    padding: 10px;
                    box-sizing: border-box;
                }}
                input[type="submit"] {{
                    background-color: #4CAF50;
                    color: white;
                    cursor: pointer;
                }}
                input[type="submit"]:hover {{
                    background-color: #45a049;
                }}
            </style>
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
    return '''
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }

                    h1 {
                        color: #333;
                    }

                    p {
                        color: #666;
                    }

                    a {
                        color: #06f;
                        text-decoration: none;
                    }
                </style>
            </head>
            <body>
                <h1>Gestor de trameses de Programació i Robòtica</h1>
                <p>Utilitza aquesta pàgina per entregar les teves tasques.</p>
                <a href=https://giuli.cat>Creat per: Pau Giuli</p>
                <p>GitHub Repository: <a href="https://github.com/pgiuli/gestor-trameses">https://github.com/pgiuli/gestor-trameses</a></p>
                <a href="/enviament">Envia una tasca</a>
            </body>
        </html>
    '''
#Make any 404 error redirect to the index page
@flask_app.errorhandler(404)
def page_not_found(e):
    return index()


if __name__ == '__main__':
    flask_app.run(debug=True)