from flask import Flask, render_template,url_for,request,redirect
from flask.globals import request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testquestions.db'
db = SQLAlchemy(app)

"""class questions(db.Model):
    __tablename__="questions"
    qid = db.Column(db.Integer, primary_key=True)
    subject =db.Column(db.String(200), nullable=False)
    question =db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(100), nullable=True)
    option2 = db.Column(db.String(100), nullable=True)
    option3 = db.Column(db.String(100), nullable=True)
    option4 = db.Column(db.String(100), nullable=True)
    answer = db.Column(db.Integer, nullable=True)
    bcol = db.Column(db.String(100), nullable=True)   
    status = db.Column(db.String(100),nullable=True)"""

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id 




@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST' and len(request.form['content'])>1:
        #return "Helol"
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
            return "There was an issue deleting your task"

@app.route('/update/<int:id>',methods = ['POST','GET'])

def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html',task=task)



"""@app.route('/form',methods=['POST','GET'])
def adddata():
    if request.method == 'POST':
        sub = request.form['subject']
        qn = request.form['qn']
        op1 = request.form['op1']
        op2 = request.form['op2']
        op3 = request.form['op3']
        op4 = request.form['op4']
        op = request.form['op']

        new_qn = questions(subject = sub, question = qn, option1 = op1,
                            option2 = op2, option3 = op3, option4 = op4, answer=op,bcol="red")

        try:
            db.session.add(new_qn)
            db.session.commit()
            return redirect('/form')
        except:
            return "There was an issue adding your task"
    else:
       return render_template('form.html')

@app.route('/show')
def show():
     new_qn = questions.query.order_by(questions.qid).all()
     return render_template('show.html',new_qn = new_qn)

"""

if __name__ == '__main__':
    app.run(debug=True)
    


