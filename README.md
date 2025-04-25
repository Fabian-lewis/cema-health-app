# 🏥 Health Program Management System

A Flask-based web application built to manage health programs, clients, appointments, and notifications for clinics or health organizations. It features role-based access for admins, doctors, and clients.

---

## 🚀 Technologies Used

- **Flask** – Lightweight Python web framework  
- **Flask-SQLAlchemy** – ORM for SQLite database handling  
- **SQLite** – Lightweight database for fast development  
- **HTML/CSS/JavaScript** – Frontend interface  

---

## 📌 Key Features

### 🔐 Role-Based Dashboards

#### 1. **Admin Dashboard**
- View and manage all users (doctors, clients)
- Create, edit, and delete health programs
- Monitor client enrollments
- Track and manage appointments and their statuses
- (Planned) Admin reports and analytics
- (Planned) Send notifications

#### 2. **Doctor Dashboard**
- View appointments assigned to them
- Add notes after client visits
- Monitor program enrollments and statuses for their clients
- Update appointment statuses (Scheduled, Completed, etc.)
- 

### 📝 Other Core Pages

#### 4. **Client Registration**
- Submit personal info (name, DOB, gender, phone, email)
- Auto-create profile in system
- (Planned) Email confirmation

#### 5. **Enroll Clients**
- Search for and select a client
- Select the program to enroll the client
- Enroll user
- (If user is already enrolled in a program then he/she cannot be enrolled again)

#### 6. **Search Client**
- Search for a client from the registered list of clients
- Enter clients name or filter by age or program
- Results populate in the results table showing name, age, gender, phone, enrollments and actions
- Click on view action to access the Clients Profile

#### 7. **Clients Profile**
- Accessed by searching for the client in search page
- Displays clients information categorized in different groups (Personal information, enrolled programs, upcoming appointments, dropped programs, meta data)
- Personal Information - displays a clients personal info (name, date of birth, email etc)
- Enrolled Programs - displays programs clients have been enrolled in
- Dropped Programs - Displays programs that a user has been dropped off from
- upcoming appointments (planned) - to display booked appointments for the client

### 📌Admin Specific Pages

#### 1. **Manage Users Page**
- Admins can add and view all the existing users in the system
- Insert data for the new user in the new user form
- Existing user form displays existing users and delete and view actions for each user
- View action displays the user detais in view_user page
- Delete deletes user

### 2. **View Clients Page**
- Displays all the registered clients
- Add new client feature to add a new client
- View user action (on table) to view a clients profile
- Delete user action (on table) to delete a clients profile
- (planned) Edit user action (on table) to edit a clients profile
- (planned) Export to CSV - get all users in downloadable CSV file

### 3. **Reports Page**
- (Plannned) - To display metric statistics and analysis 


---

## 🧩 Core Models & Relationships

### 1. **User**
- Fields: `username`, `email`, `phone`, `password_hash`, `role`, `created_at`
- Roles: `'admin'`, `'doctor'`, `'client'`
- Relations:
  - One-to-one: `Client` (for profile)
  - One-to-many: `Appointment` (as doctor), `Notification`

### 2. **Client**
- Fields: `full_name`, `date_of_birth`, `gender`, `phone`, `email`
- Linked to `User`
- Relations:
  - Many-to-many: `Program` (via `Enrollment`)
  - One-to-many: `Appointment`

### 3. **Program**
- Fields: `name`, `description`, `start_date`, `duration`
- Linked to: `Enrollment`, `Appointment`

### 4. **Enrollment**
- Links `Client` ↔ `Program`
- Fields: `start_date`, `end_date`, `status_id`, `notes`

### 5. **Appointment**
- Links `Client` ↔ `Doctor` ↔ `Program`
- Tracks appointment date, status, and doctor notes

### 6. **Notification**
- Linked to a `User`
- Contains a message and `status_id` (read/unread)

### 7. **Status**
- Shared by: `Enrollment`, `Appointment`, `Notification`
- Represents status types (e.g., Enrolled, Completed, Read)

---

## 🧱 Database Schema Overview

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
## ✅ Current System Functionality
- Full database schema with defined relationships
- User roles and access control implemented
- User and Client registration implemented
- Clients have user accounts and personalized profiles
- Enrollment logic with duplication checks (active status only)
- Search functionality with links to client's profile

## 🛠️ What to Work On
  1. Add admin reports and analytics
  2. Implement email notifications
  3. Improve form validation and error messages
  4. Notifications module
  5. Appointments module - schedule and book
 
## 📷 Screenshots

### 1. **Login Module**

