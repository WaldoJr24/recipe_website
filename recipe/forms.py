from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    submit = SubmitField('Add Recipe')