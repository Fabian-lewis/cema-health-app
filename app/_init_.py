from flask import Flask
from app.model import db, User
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from flask_migrate import Migrate

# def create_admin_if_not_exists():
#     existing_admin = User.query.filter_by(role='admin').first()
#     if not existing_admin:
#         admin_user = User(
#             username='admin',
#             email='admin@example.com',
#             phone='0712345678',
#             password_hash=generate_password_hash('admin123'),
#             role='admin'
#         )
#         db.session.add(admin_user)
#         db.session.commit()
#         print("Admin user created.")
#     else:
#         print("Admin user already exists.")

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

    # with app.app_context():
    #     #db.drop_all()
    #     alter_table_user()
        # create_admin_if_not_exists()

    

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'


    from app.routes import main
    app.register_blueprint(main)

    from api.client_api import api
    app.register_blueprint(api, url_prefix='/api')

    return app


