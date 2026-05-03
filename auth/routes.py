from flask import Blueprint, render_template, request, redirect, url_for, session
from action_db import register_user, login_user

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = register_user(username, password)
        if success:
            return redirect(url_for('auth.login'))
        error = message
    return render_template('auth/register.html', error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('calc.index'))
        error = "Invalid username or password"
    return render_template('auth/login.html', error=error)



@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))