from datetime import datetime
from random import randrange

from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aleks_rol:xofsep-pyjzoS-6cotqa@localhost:5432/what_watch'
app.config['SECRET_KEY'] = 'Gicbo9-qyxjoh-xybfyw'

db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    create_date = db.Column(db.DateTime, index=True, default=datetime.now)


class ReviewForm(FlaskForm):
    title = StringField(
        label='Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 128)],
    )
    text = TextAreaField(
        label='Напишите отзыв',
        validators=[DataRequired(message='Обязательное поле')],
    )
    source = URLField(
        label='Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()],
    )
    submit = SubmitField('Добавить')


@app.route('/')
def index_view():
    quantity = Review.query.count()
    if not quantity:
        abort(500)
    return render_template(
        'review.html',
        review=Review.query.offset(randrange(quantity)).first()
    )


@app.route('/add', methods=['GET', 'POST'])
def add_review_view():
    form = ReviewForm()
    if form.validate_on_submit():
        if Review.query.filter_by(text=form.text.data).first():
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_review.html', form=form)
        review = Review(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data,
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('review_view', id=review.id))
    return render_template('add_review.html', form=form)


@app.route('/reviews/<int:id>')
def review_view(id):
    return render_template(
        'review.html',
        review = Review.query.get_or_404(id),
    )


@app.errorhandler(500)
def internall_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
