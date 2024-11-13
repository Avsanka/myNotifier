import pymysql
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


class myDbConnection:
    def __init__(self):
        self.connection = None
    def connect(self):
        self.connection = pymysql.connect(
                            host="localhost",
                            user="root",
                            password="root",
                            db="idz",
                            cursorclass=pymysql.cursors.DictCursor
                            )
        return self.connection



@app.route('/',methods=['GET', 'POST'])
def index():
    with myDbConnection().connect() as db:
        cur = db.cursor()
        cur.execute('select * from task where status not like 2 order by Status')
        tasks = cur.fetchall()

        if request.method == 'GET':
            return render_template('index.html', tasks=tasks)

@app.route('/<int:status>', methods=['GET'])
def sort(status):
    with myDbConnection().connect() as db:
        cur = db.cursor()
        if status == 3:
            cur.execute("select * from task order by Status")
        else:
            cur.execute(f"select * from task where Status like {status} order by Status")
        tasks = cur.fetchall()
        return render_template('index.html', tasks=tasks)


@app.route('/allTasks',methods=['GET', 'POST'])
def showAllTasks():
    with myDbConnection().connect() as db:
        cur = db.cursor()
        cur.execute('select * from task order by Status')
        tasks = cur.fetchall()

        if request.method == 'GET':
            return render_template('index.html', tasks = tasks)


@app.route('/addTask',methods=['GET', 'POST'])
def addTask():
    if request.method == 'GET':
        return render_template('addTaskForm.html')
    elif request.method == 'POST':
        with myDbConnection().connect() as db:
            cur = db.cursor()
            title = request.form.get('title', 0)
            description = request.form.get('desc', 0)
            status = 0
            if title is not None and description is not None:
                cur.execute(f"insert into task (Title, Description, Status)"
                            f" values ('{title}', '{description}', '{status}');")
                db.commit()
        return redirect('/')


@app.route('/deleteTask', methods=['POST'])
def deleteTask():
    if request.method == 'POST':
        with myDbConnection().connect() as db:
            cur = db.cursor()
            iddel = request.form.get('id', None)
            if iddel is not None:
                cur.execute(f"delete from task where id = {iddel}")
            db.commit()
        return redirect('/')


@app.route('/taskInfo/<int:id>', methods=['GET'])
def taskInfo(id):
    if request.method == 'GET':
        with myDbConnection().connect() as db:
            cur = db.cursor()
            cur.execute(f"select * from task where ID = {id}")
            taskToShow = cur.fetchone()
            print(taskToShow)
            return render_template("taskInfo.html", task=taskToShow)

@app.route('/changeStatus', methods=['POST'])
def changeStatus():
    if request.method == 'POST':
        task_id = request.form.get('id', None)
        status = request.form.get('status', None)
        status = int(status) + 1
        print(task_id, status)
        if task_id is not None and status is not None:
            with myDbConnection().connect() as db:
                cur = db.cursor()
                cur.execute(f"update task set Status={status} where ID = {task_id}")
                db.commit()
        return "1"


@app.route('/editTask/<int:taskID>', methods=['GET', 'POST'])
def editTask(taskID):
    if request.method == 'GET':
        with myDbConnection().connect() as db:
            cur = db.cursor()
            cur.execute(f"select * from task where ID = {taskID}")
        return render_template('editTask.html', task=cur.fetchone())

    if request.method == 'POST':
        with myDbConnection().connect() as db:
            title = request.form.get('newTitle', None)
            description = request.form.get('newDesc', None)
            status = request.form.get('newStatus', None)
            if title is not None and description is not None and status is not None:
                print(status)
                cur = db.cursor()
                cur.execute(f"delete from task where id = {taskID}")
                cur.execute(f"insert into task (Title, Description, Status)"
                            f" values ('{title}', '{description}', '{status}');")
                db.commit()
        return "1"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8081)
