# models.py or forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, NumberRange, ValidationError

class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])

    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Pet')

    def validate_species(self, species):
        allowed_species = ['cat', 'dog', 'porcupine']
        if species.data.lower() not in allowed_species:
            raise ValidationError('Species must be either cat, dog, or porcupine.')

class EditPetForm(FlaskForm):
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')
    submit = SubmitField('Update Pet')
