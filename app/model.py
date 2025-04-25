from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

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
    doctor_appointments = db.relationship(
        'Appointment', 
        back_populates='doctor',
        foreign_keys='Appointment.doctor_id'
    )
    
    # As admin/doctor, clients I've registered
    clients_registered = db.relationship(
        'Client', 
        back_populates='registered_by_user',
        foreign_keys='Client.registered_by'
    )
    



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
    appointments = db.relationship(
        'Appointment', 
        back_populates='client',
        foreign_keys='Appointment.client_id'
    )

    enrollments = db.relationship(
        'Enrollment', 
        back_populates='client',
        foreign_keys='Enrollment.client_id',
        lazy=True
    )
    
    registered_by_user = db.relationship(
        'User', 
        back_populates='clients_registered',
        foreign_keys=[registered_by]
    )
   
    
class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in weeks
    
    # Single, clear relationship to enrollments
    enrollments = db.relationship(
        'Enrollment', 
        back_populates='program',
        lazy=True
    )

    def __repr__(self):
        return f"<Program {self.name}>"
    
class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


    def __repr__(self):
        return f"<Status {self.name}>"
    
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
    client = db.relationship(
        'Client', 
        back_populates='enrollments',
        foreign_keys=[client_id]
    )
    
    program = db.relationship(
        'Program', 
        back_populates='enrollments',
        foreign_keys=[program_id]
    )
    
    status = db.relationship(
        'Status', 
        backref='enrollments',
        foreign_keys=[status_id]
    )

    def __repr__(self):
        return f"<Enrollment {self.id}, Client: {self.client_id}, Program: {self.program_id}>"
    
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    user = db.relationship('User', backref='notifications')
    status = db.relationship('Status', backref='notifications')

    def __repr__(self):
        return f"<Notification {self.id}, {self.user_id}, {self.message}, {self.status_id}>"

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
    client = db.relationship(
        'Client', 
        back_populates='appointments',
        foreign_keys=[client_id]
    )
    
    doctor = db.relationship(
        'User', 
        back_populates='doctor_appointments',
        foreign_keys=[doctor_id]
    )
    
    program = db.relationship(
        'Program', 
        backref='appointments',
        foreign_keys=[program_id]
    )
    
    status = db.relationship(
        'Status', 
        backref='appointments',
        foreign_keys=[status_id]
    )


