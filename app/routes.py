from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from app.forms import ClientRegistrationForm, LoginForm
from werkzeug.security import check_password_hash
from app.model import User
from app.utils import login_required
main = Blueprint('main', __name__)



@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/create-program')
@login_required
def create_program():
    return render_template('create_program.html')

@main.route('/register', methods=['GET', 'POST'])
@login_required
def register_client():
    form = ClientRegistrationForm()
    
    if form.validate_on_submit():
        # Handle registration logic here
        flash("Client registered successfully!", "success")
        return redirect(url_for('main.register_client'))

    return render_template('register_client.html', form=form)

@main.route('/enroll-client')
@login_required
def enroll_client():
    return render_template('enroll_client.html')

@main.route('/search-client')
@login_required
def search_client():
    return render_template('search_client.html')

@main.route('/client/<client_id>')
@login_required
def client_profile(client_id):
    return render_template('client_profile.html', client_id=client_id)

@main.route('/admin/clients')
@login_required
def view_clients():
    return render_template('view_clients.html')

