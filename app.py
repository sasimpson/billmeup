questions = """How many bills do you pay a month?
How much time do you spend on paying bills?
How do you pay them (online, autopay, snail mail)? 
What part of the process do you like?
What part do you not like?
Have you ever had a billing mistake and how did you catch it?
How old are you?
Male or Female?"""

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.basicauth import BasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'billmedude'

basic_auth = BasicAuth(app)
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    data = db.Column(db.Text)

    question = db.relationship('Question', uselist=False, backref='answers')


@app.route('/')
@app.route('/survey', methods=["POST"])
def index():
    questions = Question.query.all()
    return render_template('thanks.html', questions=questions)

def get_answers():
    # print request.form
    for x in request.form.keys():
        qid = x.split('_')[1]
        question = Question.query.filter(Question.id==qid).one()
        answer = Answer(data=request.form.get(x), question_id=qid)
        db.session.add(answer)
        # print "%s => %s" % (, request.form.get(x))
    db.session.commit()
    return render_template('thanks.html')

@app.route('/questions')
@basic_auth.required
def questions():
    questions = Question.query.all()
    return render_template('questions_index.html', questions=questions)

@app.route('/questions/<int:id>')
@basic_auth.required
def questions_show(id):
    question = Question.query.filter(Question.id==id).one()
    return render_template('questions_show.html', question=question)

@app.route('/mockup')
def mockup_index():
    return render_template('mockup/index.html')

def reset_db():
    db.drop_all()
    db.create_all()
    for question in questions.split('\n'):
        db.session.add(Question(text=question))
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
