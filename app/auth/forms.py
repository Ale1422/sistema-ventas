from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()],render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"class": "form-control"})
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login',render_kw={"class": "btn btn-primary"})
