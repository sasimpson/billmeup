questions = """How many bills do you pay a month?
How much time do you spend on paying bills?
How do you pay them (online, autopay, snail mail)? 
What part of the process do you like?
What part do you not like?
Have you ever had a billing mistake and how did you catch it?"""

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'

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
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/survey', methods=["POST"])
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

def reset_db():
    db.drop_all()
    db.create_all()
    for question in questions.split('\n'):
        db.session.add(Question(text=question))
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
