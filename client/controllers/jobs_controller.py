from flask import Blueprint, jsonify
from services.jobs_service import fetch_jobs_from_server

jobs_blueprint = Blueprint('jobs', __name__)

@jobs_blueprint.route('/jobs', methods=['GET'])
def list_jobs():
    jobs = fetch_jobs_from_server()
    return jsonify(jobs)