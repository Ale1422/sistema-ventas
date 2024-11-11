from flask import Blueprint

empleado_bp = Blueprint('empleado', __name__, template_folder='templates')

from . import routes