from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create-program')
def create_program():
    return render_template('create_program.html')

@main.route('/register-client')
def register_client():
    return render_template('register_client.html')

@main.route('/enroll-client')
def enroll_client():
    return render_template('enroll_client.html')

@main.route('/search-client')
def search_client():
    return render_template('search_client.html')

@main.route('/client/<client_id>')
def client_profile(client_id):
    return render_template('client_profile.html', client_id=client_id)

