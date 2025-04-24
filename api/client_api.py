from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/client/<client_id>', methods=['GET'])
def get_client_profile(client_id):
    # Simulated example response
    return jsonify({
        'id': client_id,
        'name': 'Jane Doe',
        'enrolled_programs': ['HIV', 'Malaria']
    })