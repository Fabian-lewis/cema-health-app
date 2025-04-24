from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    ROLES = ['admin', 'doctor', 'client']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client_profile = db.relationship('Client', backref='user', uselist=False)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    doctor_appointments = db.relationship('Appointment', backref='doctor', lazy=True, foreign_keys='Appointment.doctor_id')


    def __repr__(self):
        return f"<User {self.username}, role = {self.role}>"
    
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))

    enrollments = db.relationship('Enrollment', backref='client', lazy=True)
    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def __repr__(self):
        return f"<Client {self.id}, {self.full_name}>"
    
class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False) # How long a program lasts in weeks
    
    enrollments = db.relationship('Enrollment', backref='program', lazy=True)

    def __repr__(self):
        return f"<Program {self.name}>"
    
class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    enrollments = db.relationship('Enrollment', backref='status', lazy=True)
    notifications = db.relationship('Notification', backref='status', lazy=True)
    appointments = db.relationship('Appointment', backref='status', lazy=True)

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

    def __repr__(self):
        return f"<Enrollment {self.id}, {self.client_id}, {self.program_id}, {self.status_id}>"
    
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

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

    def __repr__(self):
        return f"<Appointment {self.id}, {self.client_id}, {self.doctor_id}, {self.appointment_date}>"


