import csv
import click

from . import app, db
from .models import Review


@app.cli.command('load_reviews')
def load_reviews_command():
    """Функция загрузки контента в БД."""
    with open('../reviews.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            review = Review(**row)
            db.session.add(review)
            db.session.commit()
            counter += 1
    click.echo(f'Добавлено нового контента: {counter}')
