from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField,Validators
from wtforms.validators import InputRequired
from ..models import User,Pitch, Comment

class PitchForm(FlaskForm):
    category = SelectField('Category', choices = [('Product','Interview'),('Promotion','Promotion'),('Pick-up','Pick-up')], validators = [InputRequired()])
    title = StringField('Pitch title',validators=[InputRequired()])
    pitch = TextAreaField('Pitch', )
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a commment', validators=[InputRequired()])
    submit = SubmitField('Add')
