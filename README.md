# Health Program Management System

This project is a Flask-based web application designed to manage health programs, clients, and user interactions for clinics or health organizations. It supports role-based access for admins, doctors, and clients, and allows the scheduling of appointments, enrollment into programs, and sending notifications.

## 🔧 Technologies Used

- **Flask** – Lightweight Python web framework
- **Flask-SQLAlchemy** – ORM for handling SQLite database
- **SQLite** – Simple and fast database for development
- **HTML/CSS/JavaScript** – Frontend (currently under development)


## 📂 Features Implemented

---
### ✅ Views/ Pages
### 1. **Admin Dashboard**
   - **Purpose**: Admins will be able to manage the entire system, including overseeing client profiles, program enrollments, appointments, and notifications.
   - **Features**:
     - View and manage all users (Doctors, Clients)
     - Create, edit, and delete programs
     - Track client enrollments
     - Review appointment statuses and notes
     - Send notifications to users
     - Admin-related reports and analytics (future)

### 2. **Doctor Dashboard**
   - **Purpose**: Doctors can manage their appointments and client interactions for the programs they oversee.
   - **Features**:
     - View and manage appointments for their clients
     - Add notes to appointments after client visits
     - Review client program enrollments and status updates
     - Update the status of appointments (Scheduled, Completed, etc.)

### 3. **Client Profile Page**
   - **Purpose**: Clients can view and manage their profiles and appointment details.
   - **Features**:
     - View personal information (name, date of birth, contact info)
     - Track program enrollments and statuses
     - Review upcoming appointments and appointment notes
     - Receive notifications about their enrollment or appointments

### 4. **Registration Page**
   - **Purpose**: Clients can register and create their profile in the system.
   - **Features**:
     - Input personal information like full name, date of birth, gender, phone, email
     - Choose a program to enroll in
     - Submit registration details and become part of the system
     - Email confirmation upon successful registration (future feature)

### 5. **Appointment Scheduling Page**
   - **Purpose**: Allows doctors and clients to view and schedule appointments.
   - **Features**:
     - Clients can request appointments for specific programs
     - Doctors can view and accept/reject appointment requests
     - Set and update appointment statuses (Scheduled, Completed)
     - Doctors can add notes after client visits

### 6. **Notification Center**
   - **Purpose**: Users can view notifications related to their appointments, enrollments, or other updates.
   - **Features**:
     - Notifications for new appointments, status updates, or system-wide changes
     - Mark notifications as read/unread
     - View messages related to program status changes

---

### ✅ Core Models

1. **User**
   - Fields: `username`, `email`, `phone`, `password_hash`, `role`, `created_at`
   - Roles: `'admin'`, `'doctor'`, `'client'`
   - Relationships:
     - One-to-one with `Client` (for client profile)
     - One-to-many with `Notification`
     - One-to-many with `Appointment` (as doctor)

2. **Client**
   - Fields: `full_name`, `date_of_birth`, `gender`, `phone`, `email`
   - Linked to `User`
   - Relationships:
     - Many-to-many with `Program` via `Enrollment`
     - One-to-many with `Appointment`

3. **Program**
   - Fields: `name`, `description`, `start_date`, `duration`
   - Linked to `Enrollment` and `Appointment`

4. **Enrollment**
   - Links clients to programs with statuses
   - Includes `start_date`, `end_date`, and optional notes

5. **Status**
   - Used across `Enrollment`, `Notification`, and `Appointment` to represent states (e.g., enrolled, scheduled, completed, read/unread)

6. **Notification**
   - Sent to users
   - Contains a message and associated status (e.g., read/unread)

7. **Appointment**
   - Links clients and doctors to specific programs
   - Tracks `appointment_date`, `status`, and doctor notes

---

## 💾 Database Schema Overview

```plaintext
User (1) —— (1) Client
User (1) —— (M) Notification
User (1) —— (M) Appointment [as doctor]
Client (1) —— (M) Enrollment —— (1) Program
Client (1) —— (M) Appointment —— (1) Doctor
Enrollment —— (1) Status
Notification —— (1) Status
Appointment —— (1) Status

```
## 🔑 Current Functionality
1. **Database structure defined with relationships**
2. **Roles and user modeling in place**
3. **Appointments and notifications architecture ready**
4. **Support for clients to have user accounts and access profiles**

