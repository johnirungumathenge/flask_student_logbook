# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField,SelectField
from wtforms.validators import DataRequired

class StudentData(FlaskForm):
    work = TextAreaField('work', validators=[DataRequired()], render_kw={'rows': 5})
    # week = StringField('Week', validators=[DataRequired()])
    day = SelectField('Day', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                                        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
                                        ], validators=[DataRequired()])
    week = SelectField('Week', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                      ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')],
                      validators=[DataRequired()])
    date = DateField('Date')
