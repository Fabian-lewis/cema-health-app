from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    from api.client_api import api
    app.register_blueprint(api, url_prefix='/api')

    return app