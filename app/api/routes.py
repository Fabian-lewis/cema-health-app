from flask import Blueprint, jsonify, request
from app.model import Client, Program, Enrollment, db
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api')

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

@api.route('/programs')
def get_programs():
    programs = Program.query.all()
    return jsonify([
        {'id': program.id, 'name': program.name}
        for program in programs
    ])

@api.route('/clients/<int:client_id>/enrollments')
def get_client_enrollments(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    enrollments = Enrollment.query.filter_by(client_id=client_id).all()
    return jsonify([
        {
            'programName': enrollment.program.name,
            'date': enrollment.date.strftime('%Y-%m-%d'),
            'status': enrollment.status
        }
        for enrollment in enrollments
    ])

@api.route('/clients/<int:client_id>/enroll', methods=['POST'])
def enroll_client(client_id):
    data = request.json
    program_ids = data.get('programIds', [])    
    
    if not program_ids:
        return jsonify({'error': 'No programs selected'}), 400
    
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    try:
        for program_id in program_ids:
            program = Program.query.get(program_id)
            if not program:
                return jsonify({'success': False, 'message': f'Program not found: {program_id}'}), 404
            
            enrollment = Enrollment(
                client_id=client_id,
                program_id=program_id,
                status_id=1,
                enrollment_date=datetime.now(),
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=program.duration * 7)
            )
            db.session.add(enrollment)
            
        db.session.commit()
        return jsonify({'success': True, 'message': 'Enrollment successful'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

