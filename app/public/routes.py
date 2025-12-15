from flask import abort, render_template
from flask_login import current_user
from . import public_bp


@public_bp.route("/")
def index():
    posts =[] 
    return render_template("public/index.html", posts=posts)
