from functools import wraps
from flask import session, redirect, url_for, flash
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('main.login'))
        if current_user.role != 'admin':
            flash("You need to be an admin to access this page.", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function