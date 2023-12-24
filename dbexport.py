#Export all submissions in trameses.db to a directory structure with the code in .py format.
# The directory structure should be as follows:
# - submissions
#   - <task_name>
#     - user.py

import sqlite3
import os
import shutil

def export_submissions():
    conn = sqlite3.connect('trameses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM trameses")
    submissions = c.fetchall()
    conn.close()
    for submission in submissions:
        user = submission[0]
        taskid = submission[1]
        code = submission[2]
        if not os.path.exists(f'submissions/{taskid}'):
            os.makedirs(f'submissions/{taskid}')
        with open(f'submissions/{taskid}/{user}.py', 'w') as f:
            f.write(code)
    shutil.make_archive('submissions', 'zip', 'submissions')
    shutil.rmtree('submissions')


    