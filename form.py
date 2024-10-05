from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CancerDataForm(FlaskForm):
    mean_radius = FloatField('Mean Radius', validators=[DataRequired(), NumberRange(min=6.98, max=28.11, message="Radius must be between 6.98 and 28.11")])
    mean_perimeter = FloatField('Mean Perimeter', validators=[DataRequired(), NumberRange(min=43.79, max=188.50, message="Perimeter must be between 43.79 and 188.50")])
    mean_area = FloatField('Mean Area', validators=[DataRequired(), NumberRange(min=143.50, max=2501.00, message="Area must be between 143.50 and 2501.00")])
    mean_concavity = FloatField('Mean Concavity', validators=[DataRequired(), NumberRange(min=0.00, max= 0.43, message="Concavity must be between 0.00 and  0.43")])
    mean_concave_points = FloatField('Mean Concave Points', validators=[DataRequired(), NumberRange(min=0.00, max=0.20, message="Concave Points must be between 0.00 and 0.20")])
    worst_radius = FloatField('Worst Radius', validators=[DataRequired(), NumberRange(min=7.93, max=36.04, message="Radius must be between 7.93 and 36.04")])
    worst_perimeter = FloatField('Worst Perimeter', validators=[DataRequired(), NumberRange(min=50.41, max=251.20, message="Perimeter must be between 50.41 and 251.20")])
    worst_area = FloatField('Worst Area', validators=[DataRequired(), NumberRange(min=185.20, max=4254.00, message="Area must be between 185.20 and 4254.00")])
    worst_concavity = FloatField('Worst Concavity', validators=[DataRequired(), NumberRange(min=0.00, max=1.25, message="Concavity must be between 0.00 and 1.25")])
    worst_concave_points = FloatField('Worst Concave Points', validators=[DataRequired(), NumberRange(min=0.00, max=0.29, message="Concave Points must be between 0.00 and 0.29")])
    submit = SubmitField('Predict')