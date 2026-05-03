from flask import Blueprint, render_template, request, session, redirect, url_for
from action_db import save_calculation, get_history

calc_bp = Blueprint('calc', __name__, template_folder='templates')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@calc_bp.route('/')
@login_required
def index():
    history = get_history(session['user_id'])
    return render_template('calc/index.html', history=history)


@calc_bp.route('/calculate', methods=['POST'])
@login_required
def calculate():
    expression = request.form.get('expression', '').strip()
    result = None
    error = None
    try:
        allowed = set('0123456789+*/().')
        if not all(c in allowed for c in expression):
            raise ValueError("Invalid characters in expression")
        result = str(eval(expression))
        save_calculation(session['user_id'], expression, result)
    except Exception:
        error = "Invalid expression"
    history = get_history(session['user_id'])
    return render_template('calc/index.html',
                           expression=expression,
                           result=result,
                           error=error,
                           history=history)