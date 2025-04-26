from flask import Flask
from app.model import db, User, Status
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

# def create_status_if_not_exists():
#     existing_status = Status.query.filter_by(name='Enrolled').first()

#     if not existing_status:
#         # status for enrollment (Enrolled, Completed, Dropped)
#         status1 = Status(name='Enrolled' , description='Enrolled in the program')
#         status2 = Status(name='Completed' , description='Completed the program')
#         status3 = Status(name='Dropped' , description='Dropped out of the program')
#         # appointment notification (sent, is-read)
#         status4 = Status(name='sent' , description='sent appointment')
#         status5 = Status(name='is-read' , description='is-read appointment')

#         # appointment status (Pending, Confirmed, Cancelled)
#         status6 = Status(name='Pending' , description='Pending appointment')
#         status7 = Status(name='Confirmed' , description='Confirmed appointment')
#         status8 = Status(name='Cancelled' , description='Cancelled appointment')

#         db.session.add(status1)
#         db.session.add(status2)
#         db.session.add(status3)
#         db.session.add(status4)
#         db.session.add(status5)
#         db.session.add(status6)
#         db.session.add(status7)
#         db.session.add(status8)

#         db.session.commit()

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
    #     create_status_if_not_exists()
    #     #db.drop_all()
    #     alter_table_user()
        # create_admin_if_not_exists()

    

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'


    from app.routes import main
    app.register_blueprint(main)

    from app.api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app


