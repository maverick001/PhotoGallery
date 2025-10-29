from flask import session, redirect, flash, url_for
from functools import wraps


def admin_required(func):
 
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in before moving on.', 'error')
            return redirect(url_for('main.login'))
        if session['user']['user_type'] != 'admin':
            flash('You do not have permission to view this page.', 'error')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return wrapper