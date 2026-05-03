from flask import Flask
from models import init_db

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

from auth.routes import auth_bp
from calc.routes import calc_bp

app.register_blueprint(auth_bp)
app.register_blueprint(calc_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)