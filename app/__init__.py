from flask import Flask
from flask_migrate import Migrate
from app.model import db, User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_program.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app 