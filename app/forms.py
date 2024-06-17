from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


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
