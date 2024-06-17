from random import randrange

from flask import abort,flash, redirect, render_template, url_for

from . import app, db
from .models import Review
from .forms import ReviewForm


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
