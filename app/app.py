from datetime import datetime
from random import randrange
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aleks_rol:xofsep-pyjzoS-6cotqa@localhost:5432/what_watch'

db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    create_date = db.Column(db.DateTime, index=True, default=datetime.now)


@app.route('/')
def index_view():
    quantity = Review.query.count()
    if not quantity:
        return 'В базе пусто!'
    return render_template(
        'review.html',
        review=Review.query.offset(randrange(quantity)).first()
    )


@app.route('/add')
def add_review_view():
    return render_template('add_review.html')


if __name__ == '__main__':
    app.run()
