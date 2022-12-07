import re
from functools import wraps
from database import *
from flask import request, jsonify


def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "Authorization" not in request.headers:
            return jsonify({"message": "Authorization header not present"}), 401
        auth = request.headers.get("Authorization")
        admin = session.query(admin_table).filter(admin_table.c.auth_token == str(auth)).all()
        if admin:
            return f(*args, **kwargs)
        return jsonify({"message": "you need to be admin"}), 403

    return wrap


def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z-]+)*$", email):
        return False
    return True


def phone_number_validator(phone_number):
    if not re.findall("[0-9]{10}$", phone_number):
        return False
    return True


def is_password(password):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password):
        return False
    return True