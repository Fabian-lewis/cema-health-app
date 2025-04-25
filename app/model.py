from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

# User model
# This is the model for the users of the application
# It has a username, email, phone, password, role, and created_at
# It also has a relationship to the clients that it has registered
# It also has a relationship to the appointments that it has created
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    ROLES = ['admin', 'doctor', 'client']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    # As a doctor, appointments where I'm the doctor
    # This is a relationship to the appointments that I have created
    doctor_appointments = db.relationship(
        'Appointment', 
        back_populates='doctor',
        foreign_keys='Appointment.doctor_id'
    )
    
    # As admin/doctor, clients I've registered
    # This is a relationship to the clients that I have registered
    clients_registered = db.relationship(
        'Client', 
        back_populates='registered_by_user',
        foreign_keys='Client.registered_by'
    )
    



# Client model
# This is the model for the clients of the application
# It has a full_name, date_of_birth, gender, phone, email, registered_at, and registered_by
# It also has a relationship to the appointments that I have created
# It also has a relationship to the enrollments that I have created
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    registered_by = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_client_registered_by'), nullable=False)

    # Relationships
    # This is a relationship to the appointments that I have created/the doctors that I have seen
    appointments = db.relationship(
        'Appointment', 
        back_populates='client',
        foreign_keys='Appointment.client_id'
    )

    # This is a relationship to the enrollments that I have created/the programs that I am enrolled in
    enrollments = db.relationship(
        'Enrollment', 
        back_populates='client',
        foreign_keys='Enrollment.client_id',
        lazy=True
    )

    # This is a relationship to the user that registered the client
    registered_by_user = db.relationship(
        'User', 
        back_populates='clients_registered',
        foreign_keys=[registered_by]
    )
   
# Program model
# This is the model for the programs of the application
# It has a name, description, start_date, and duration
# It also has a relationship to the enrollments that I have created
class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in weeks
    
    # This is a relationship to the enrollments that I have created/the clients that are enrolled in the program
    enrollments = db.relationship(
        'Enrollment', 
        back_populates='program',
        lazy=True
    )

    def __repr__(self):
        return f"<Program {self.name}>"
    

# Status model
# This is the model for the statuses of the application
# It has a name, description, and created_at
# It also has a relationship to the enrollments that I have created

    """
    # status for enrollment (Enrolled, Completed, Dropped)
        1 = name='Enrolled' , description='Enrolled in the program'
        2 = name='Completed' , description='Completed the program'
        3 = name='Dropped' , description='Dropped out of the program'

    # appointment notification (sent, is-read)
        4 = name='sent' , description='sent appointment'
        5 = name='is-read' , description='is-read appointment'

    # appointment status (Pending, Confirmed, Cancelled)
        6 = name='Pending' , description='Pending appointment's
        7 = name='Confirmed' , description='Confirmed appointment'
        8 = name='Cancelled' , description='Cancelled appointment'
    """
class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


    def __repr__(self):
        return f"<Status {self.name}>" 


# Enrollment model
# This is the model for the enrollments of the application
# It has a client_id, program_id, status_id, enrollment_date, start_date, end_date, and notes
# It also has a relationship to the client that is enrolled in the program
# It also has a relationship to the program that the client is enrolled in
# It also has a relationship to the status of the enrollment
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    # Relationships
    # This is a relationship to the client that is enrolled in the program
    client = db.relationship(
        'Client', 
        back_populates='enrollments',
        foreign_keys=[client_id]
    )

    # This is a relationship to the program that the client is enrolled in
    program = db.relationship(
        'Program', 
        back_populates='enrollments',
        foreign_keys=[program_id]
    )

    # This is a relationship to the status of the enrollment
    status = db.relationship(
        'Status', 
        backref='enrollments',
        foreign_keys=[status_id]
    )

    def __repr__(self):
        return f"<Enrollment {self.id}, Client: {self.client_id}, Program: {self.program_id}>"


# Notification model
# This is the model for the notifications of the application
# It has a user_id, message, created_at, and status_id
# It also has a relationship to the user that the notification is for
# It also has a relationship to the status of the notification
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    # This is a relationship to the user that the notification is for
    user = db.relationship('User', backref='notifications')

    # This is a relationship to the status of the notification
    status = db.relationship('Status', backref='notifications')

    def __repr__(self):
        return f"<Notification {self.id}, {self.user_id}, {self.message}, {self.status_id}>"

# Appointment model
# This is the model for the appointments of the application
# It has a client_id, doctor_id, program_id, appointment_date, status_id, and notes
# It also has a relationship to the client that the appointment is for
# It also has a relationship to the doctor that the appointment is for
# It also has a relationship to the program that the appointment is for
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    notes = db.Column(db.Text)

    # Relationships

    # This is a relationship to the client that the appointment is for
    client = db.relationship(
        'Client', 
        back_populates='appointments',
        foreign_keys=[client_id]
    )

    # This is a relationship to the doctor that the appointment is for
    doctor = db.relationship(
        'User', 
        back_populates='doctor_appointments',
        foreign_keys=[doctor_id]
    )
    
    # This is a relationship to the program that the appointment is for
    program = db.relationship(
        'Program', 
        backref='appointments',
        foreign_keys=[program_id]
    )
    
    # This is a relationship to the status of the appointment
    status = db.relationship(
        'Status', 
        backref='appointments',
        foreign_keys=[status_id]
    )


