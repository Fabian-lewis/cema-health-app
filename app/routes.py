from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from app.forms import ClientRegistrationForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from app.model import User, Client, db, Program, Enrollment
from app.utils import login_required, admin_required, doctor_required
from datetime import datetime, timedelta
from sqlalchemy import func

from flask_login import login_user, current_user, logout_user

main = Blueprint('main', __name__)



@main.route('/')
@login_required
def index():
    # Get basic statistics for all users
    total_programs = Program.query.count()
    total_clients = Client.query.count()
    active_enrollments = Enrollment.query.filter_by(status_id=1).count()  # Assuming status_id 1 is active

    # Initialize admin statistics
    admin_stats = {}
    
    # If user is admin, calculate additional statistics
    if current_user.is_authenticated and current_user.role == 'admin':
        # Total users
        admin_stats['total_users'] = User.query.count()
        
        # Active users (users who have logged in within the last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        admin_stats['active_users'] = User.query.filter(User.last_login >= seven_days_ago).count()
        
        # Admin users
        admin_stats['admin_users'] = User.query.filter_by(role='admin').count()
        
        # New users in last 24 hours
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        admin_stats['new_users_24h'] = User.query.filter(User.created_at >= one_day_ago).count()

    # Get recent activities (last 5 activities)
    recent_activities = [
        {
            'title': 'System Update',
            'description': 'System maintenance completed successfully',
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        }

    ]

    return render_template('index.html',
                         total_programs=total_programs,
                         total_clients=total_clients,
                         active_enrollments=active_enrollments,
                         recent_activities=recent_activities,
                         **admin_stats)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_user()
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            # Update last_login timestamp
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/create-program')
@login_required
def create_program():
    programs = Program.query.all()
    return render_template('create_program.html', programs=programs)

@main.route('/register-client', methods=['GET', 'POST'])
@login_required
def register_client():
    #check if the user is admin or doctor
    if current_user.role != 'admin' and current_user.role != 'doctor':
        flash('You are not authorized to register a client', 'danger')
        return redirect(url_for('main.index'))
    
    form = ClientRegistrationForm()
    
    #check if the form is valid
    if form.validate_on_submit():

        #create a new client
        new_client = Client(
            full_name=f"{form.first_name.data} {form.last_name.data}",
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            phone=form.phone.data,
            email=form.email.data,
            registered_by=current_user.id,
            registered_at=datetime.utcnow()
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Client registered successfully!", "success")
        return redirect(url_for('main.register_client'))

    return render_template('register_client.html', form=form)

@main.route('/enroll-client')
@login_required
def enroll_client():
    return render_template('enroll_client.html')

@main.route('/search-client' , methods=['GET', 'POST'])
@login_required
def search_client():
    programs = Program.query.all()
    return render_template('search_client.html', programs=programs)

@main.route('/client/<client_id>')
@login_required
def client_profile(client_id):
    return render_template('client_profile.html', client_id=client_id)

@main.route('/admin/clients')
@login_required
def view_clients():
    return render_template('view_clients.html')

@main.route('/manage-users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@main.route('/add-user', methods=['POST'])
@login_required
@admin_required
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    phone = request.form.get('phone')
    full_name = request.form.get('full_name')

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'danger')
        return redirect(url_for('main.manage_users'))

    # Create new user
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        phone=phone
    )
    db.session.add(new_user)
    db.session.commit()

    # If it's a client, create client profile
    if role == 'client' and full_name:
        client = Client(
            id=new_user.id,
            full_name=full_name,
            email=email,
            phone=phone
        )
        db.session.add(client)
        db.session.commit()

    flash('User added successfully', 'success')
    return redirect(url_for('main.manage_users'))

@main.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow deleting the last admin
    if user.role == 'admin' and User.query.filter_by(role='admin').count() <= 1:
        flash('Cannot delete the last admin user', 'danger')
        return redirect(url_for('main.manage_users'))

    # Delete associated client profile if exists
    if user.role == 'client':
        client = Client.query.get(user_id)
        if client:
            db.session.delete(client)

    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('main.manage_users'))

@main.route('/view-user/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    client_profile = None
    if user.role == 'client':
        client_profile = Client.query.get(user_id)
    return render_template('view_user.html', user=user, client_profile=client_profile)

@main.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@main.route('/add-program', methods=['POST'])
@login_required
def add_program():
    name = request.form.get('program_name')
    description = request.form.get('description')
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
    
    duration = int(request.form.get('duration'))

    #check if the program already exists
    if Program.query.filter_by(name=name).first():
        flash('Program already exists', 'danger')
        return redirect(url_for('main.create_program'))
    
    #check if the start_date is in the future
    if start_date < datetime.utcnow().date():
        flash('Start date must be in the future', 'danger')
        return redirect(url_for('main.create_program'))
    

    if current_user.role == 'admin' or current_user.role == 'doctor':
        program = Program(name=name, description=description, start_date=start_date, duration=duration)
        db.session.add(program)
        db.session.commit()
        flash('Program added successfully', 'success')
        return redirect(url_for('main.create_program'))
    else:
        flash('You are not authorized to add a program', 'danger')
        return redirect(url_for('main.create_program'))

@main.route('/edit-program/<int:program_id>', methods=['GET', 'POST'])
@login_required
def edit_program(program_id):
    if current_user.role != 'admin' and current_user.role != 'doctor':
        flash('You are not authorized to edit a program', 'danger')
        return redirect(url_for('main.create_program'))
    
    program = Program.query.get_or_404(program_id)

    if request.method == 'POST':
        try:
            program.name = request.form.get('program_name')
            program.description = request.form.get('description')
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()

            if start_date < datetime.utcnow().date():
                flash('Start date must be today or in the future.', 'warning')
                return redirect(url_for('main.edit_program', program_id=program.id))

            program.start_date = start_date
            program.duration = int(request.form.get('duration'))

            db.session.commit()
            flash('Program updated successfully', 'success')
            return redirect(url_for('main.create_program'))
        
        except Exception as e:
            flash(f'Error updating program: {e}', 'danger')
            return redirect(url_for('main.edit_program', program_id=program.id))
    
    return render_template('edit_program.html', program=program)


@main.route('/delete-program/<int:program_id>', methods=['POST'])
@login_required
def delete_program(program_id):
    if current_user.role != 'admin' and current_user.role != 'doctor':
        flash('You are not authorized to delete a program', 'danger')
        return redirect(url_for('main.create_program'))
    
    program = Program.query.get_or_404(program_id)
    db.session.delete(program)
    db.session.commit()
    flash('Program deleted successfully', 'success')
    return redirect(url_for('main.create_program'))
