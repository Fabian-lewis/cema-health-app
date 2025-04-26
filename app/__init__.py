from flask import Flask
from app.model import db, User, Status
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'health-app'

    db.init_app(app)
    migrate = Migrate(app, db)


    login_manager.init_app(app)
    login_manager.login_view = 'main.login'


    from app.routes import main
    app.register_blueprint(main)

    from app.api.routes import api
    app.register_blueprint(api, url_prefix='/api')


    # Configure CORS for the public api - get client profile
    CORS(app, resources={
        r"/api/client/*": {
            "origins": ["https://cemaexternalsite.netlify.app/"],  # Replace with your frontend URL
            "methods": ["GET"],
            "allow_headers": ["Content-Type"]
        }
    })

    return app


