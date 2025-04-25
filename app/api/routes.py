from flask import Blueprint, jsonify, request, current_app
from app.model import Client, Program, Enrollment, Appointment, db
from datetime import datetime, timedelta, date
from sqlalchemy.orm import joinedload

api = Blueprint('api', __name__, url_prefix='/api')


"""   Search for clients @ api.route('/clients/search')
This is a get request that takes in a search term
It then returns a list of clients that match the search criteria.
It returns the client id, name, email, gender, phone, age, and the programs they are enrolled in 
It also returns the user that registered the client
"""
@api.route('/clients/search')
def search_clients():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    results = Client.query.filter(Client.full_name.ilike(f"%{query}%")).all()
    return jsonify([
        {'id': client.id, 'name': client.full_name, 'email': client.email}
        for client in results
    ])



"""   Get all programs @ api.route('/programs')
This is a get request that returns a list of all programs
"""
@api.route('/programs')
def get_programs():
    programs = Program.query.all()
    return jsonify([
        {'id': program.id, 'name': program.name}
        for program in programs
    ])


"""   Get all enrollments for a client @ api.route('/clients/<int:client_id>/enrollments')
This is a get request that takes in a client id
It then returns a list of all enrollments for the client
"""
@api.route('/clients/<int:client_id>/enrollments', methods=['GET'])
def get_client_enrollments(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    enrollments = Enrollment.query.filter_by(client_id=client_id).all()
    
    result = []
    for enrollment in enrollments:
        program = getattr(enrollment, 'program', None)
        result.append({
            'programName': program.name if program else 'N/A',
            'date': enrollment.enrollment_date.strftime('%Y-%m-%d') if enrollment.enrollment_date else 'N/A',
            'status': enrollment.status.name if enrollment.status else 'N/A'
        })
    
    return jsonify(result)


"""   Enroll client to a program @ api.route('/clients/<int:client_id>/enroll', methods=['POST'])
This is a post request that takes in a client id and a list of program ids
It then enrolls the client to the programs
"""
@api.route('/clients/<int:client_id>/enroll', methods=['POST'])
def enroll_client(client_id):
    data = request.json
    program_ids = data.get('programIds', [])    

    if not program_ids:
        return jsonify({'error': 'No programs selected'}), 400

    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    # Check for duplicate enrollments using a query
    conflicts = Enrollment.query.filter(
        Enrollment.client_id == client_id,
        Enrollment.program_id.in_(program_ids),
        Enrollment.status_id == 1  # active enrollments
    ).all()

    if conflicts:
        conflict_program_ids = [e.program_id for e in conflicts]

        # Fetch program names in one query
        conflict_programs = Program.query.filter(Program.id.in_(conflict_program_ids)).all()
        conflict_names = [p.name for p in conflict_programs]
            

        return jsonify({'success': False, 'message': f'Client already enrolled in the following program(s): {conflict_names}'}), 400

    try:
        for program_id in program_ids:
            program = Program.query.get(program_id)
            if not program:
                return jsonify({'success': False, 'message': f'Program not found: {program_id}'}), 404

            enrollment = Enrollment(
                client_id=client_id,
                program_id=program_id,
                status_id=1,  # assuming 1 is active
                enrollment_date=datetime.now(),
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(weeks=program.duration)
            )
            db.session.add(enrollment)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Enrollment successful'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


"""   Search for clients @ api.route('/search-clients')
This is a get request that takes in a search term, program id, and age
It then returns a list of clients that match the search criteria.
It returns the client id, name, email, gender, phone, age, and the programs they are enrolled in 
It also returns the user that registered the client
"""
@api.route('/search-clients')
def search_clients_api():
    search_term = request.args.get('q', '')
    program_id = request.args.get('program', '')
    age = request.args.get('age', '')

    try:
        """
        This is the query that gets the clients, 
            - their enrollments, 
            - the programs they are enrolled in, 
            - the status of the enrollments, 
            - and the user that registered the client
        """
        query = db.session.query(Client).options(
            joinedload(Client.enrollments).joinedload(Enrollment.program),
            joinedload(Client.enrollments).joinedload(Enrollment.status),
            joinedload(Client.registered_by_user) # This is the user that registered the client
        )

        if search_term:
            query = query.filter(Client.full_name.ilike(f"%{search_term}%"))

        if program_id:
            query = query.join(Client.enrollments).filter(Enrollment.program_id == program_id)

        if age:
            try:
                ageLower, ageUpper = map(int, age.split('-'))

                today = date.today()
                
                # Person just turned age_upper -> born 'today - age_upper years'
                dob_start = today - timedelta(days=ageUpper * 365)

                # Person is about to turn age_lower -> born 'today - age_lower years'
                dob_end = today - timedelta(days=(ageLower + 1) * 365)

                query = query.filter(Client.date_of_birth.between(dob_start, dob_end))
            except ValueError:
                pass

        clients = query.all()

        return jsonify({
            
            'clients': [
                {
                    'id': client.id,
                    'name': client.full_name,
                    'email': client.email,
                    'gender': client.gender,
                    'phone': client.phone,
                    'age': (date.today().year - client.date_of_birth.year),
                    'registered_by': client.registered_by_user.username if client.registered_by_user else None,
                    'enrollments': [
                        {
                            'program': enrollment.program.name,
                            'status': enrollment.status.name,
                            'start_date': enrollment.start_date.isoformat(),
                            'end_date': enrollment.end_date.isoformat()
                        }
                        for enrollment in client.enrollments
                    ]
                }
                for client in clients
            ]
        })

    except Exception as e:
        current_app.logger.error(f"Error in search_clients_api: {str(e)}")
        return jsonify({'error': 'An error occurred while searching clients'}), 500


"""   Get client profile @ api.route('/client/<int:client_id>', methods=['GET'])
This api exposes the client profile to the frontend
It returns the client profile, their enrollments, their dropped enrollments, and their appointments
"""
@api.route('/client/<int:client_id>', methods=['GET'])
def get_client_profile_api(client_id):
    client = Client.query.get_or_404(client_id)

    enrollments = Enrollment.query.filter_by(client_id=client_id, status_id=1).all()
    dropped_enrollments = Enrollment.query.filter_by(client_id=client_id, status_id=3).all()
    appointments = Appointment.query.filter_by(client_id=client_id).all()

    data = {
        'id': client.id,
        'name': client.full_name,
        'gender': client.gender,
        'email': client.email,
        'phone': client.phone,
        'registered_at': client.registered_at.strftime('%Y-%m-%d'),
        'active_enrollments': [
            {
                'program': e.program.name,
                'status': e.status.name,
                'start_date': e.start_date.strftime('%Y-%m-%d'),
                'end_date': e.end_date.strftime('%Y-%m-%d'),
            } for e in enrollments
        ],
        'dropped_enrollments': [
            {
                'program': e.program.name,
                'status': e.status.name,
                'start_date': e.start_date.strftime('%Y-%m-%d'),
                'end_date': e.end_date.strftime('%Y-%m-%d'),
            } for e in dropped_enrollments
        ],
        'appointments': [
            {
                'date': a.date.strftime('%Y-%m-%d'),
                'status': a.status.name,
                'doctor': a.doctor.full_name if a.doctor else 'N/A'
            } for a in appointments
        ]
    }

    return jsonify(data)


