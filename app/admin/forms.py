from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    precio = DecimalField('Precio', validators=[DataRequired()])
    stock = DecimalField('Cantidad en Stock', default=0.00)
    submit = SubmitField('Agregar Producto')

class EditarProductoForm(FlaskForm):
    Nombre_Producto = StringField('Nombre', validators=[DataRequired()])
    Descripción = TextAreaField('Descripción')
    Precio = DecimalField('Precio', validators=[DataRequired()])
    Stock_Cantidad = DecimalField('Cantidad en Stock', default=0.00)
    submit = SubmitField('Editar Producto')

class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)],render_kw={"class": "form-control"})
    lastName = StringField('Apellido', validators=[DataRequired(), Length(max=64)],render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"class": "form-control"})
    submit = SubmitField('Registrar',render_kw={"class": "btn btn-primary"})