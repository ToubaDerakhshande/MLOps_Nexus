from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CancerDataForm(FlaskForm):
    mean_radius = FloatField('Mean Radius', validators=[DataRequired(), NumberRange(min=0, max=50, message="Radius must be between 0 and 50")])
    mean_perimeter = FloatField('Mean Perimeter', validators=[DataRequired(), NumberRange(min=0, max=200, message="Perimeter must be between 0 and 200")])
    mean_area = FloatField('Mean Area', validators=[DataRequired(), NumberRange(min=0, max=2500, message="Area must be between 0 and 2500")])
    mean_concavity = FloatField('Mean Concavity', validators=[DataRequired(), NumberRange(min=0, max=1, message="Concavity must be between 0 and 1")])
    mean_concave_points = FloatField('Mean Concave Points', validators=[DataRequired(), NumberRange(min=0, max=0.3, message="Concave Points must be between 0 and 0.3")])
    worst_radius = FloatField('Worst Radius', validators=[DataRequired(), NumberRange(min=0, max=50, message="Radius must be between 0 and 50")])
    worst_perimeter = FloatField('Worst Perimeter', validators=[DataRequired(), NumberRange(min=0, max=300, message="Perimeter must be between 0 and 300")])
    worst_area = FloatField('Worst Area', validators=[DataRequired(), NumberRange(min=0, max=3000, message="Area must be between 0 and 3000")])
    worst_concavity = FloatField('Worst Concavity', validators=[DataRequired(), NumberRange(min=0, max=1.5, message="Concavity must be between 0 and 1.5")])
    worst_concave_points = FloatField('Worst Concave Points', validators=[DataRequired(), NumberRange(min=0, max=0.4, message="Concave Points must be between 0 and 0.4")])
    submit = SubmitField('Predict')