from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired


class PostForm(FlaskForm):
    post = TextAreaField(('Say something'), validators=[DataRequired()])
    submit = SubmitField(('Submit'))