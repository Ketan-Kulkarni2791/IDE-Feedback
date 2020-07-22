from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from send_mail import send_email

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:arrehman@123@localhost/ide_feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nboibfiutibfjd' \
                                            ':a8c489e1a5d5574856f8ab2089ffa8a9cbad26ae72f9c88da2a1316f77b5fa06@ec2-18' \
                                            '-214-119-135.compute-1.amazonaws.com:5432/datiltbp0c5ssm '

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    editor = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, editor, rating, comments):
        self.customer = customer
        self.editor = editor
        self.rating = rating
        self.comments = comments


db.create_all()
db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        editor = request.form['IDE/Text Editor']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, editor, rating, comments)
        if customer == '' or editor == '':
            return render_template('index.html', message="Please enter required fields.")
        if db.session.query(feedback).filter(feedback.customer == customer).count() == 0:
            data = feedback(customer, editor, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_email(customer, editor, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message="You have already submitted the feedback.")


if __name__ == "__main__":
    app.run()
