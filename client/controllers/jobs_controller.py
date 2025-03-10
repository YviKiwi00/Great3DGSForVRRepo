from flask import Blueprint, jsonify, request

from services.jobs_service import (fetch_jobs_from_server,
                                   fetch_job_details,
                                   fetch_job_logs,
                                   trigger_colmap,
                                   trigger_mcmc,
                                   trigger_segmentation_preparation,
                                   trigger_frosting,
                                   fetch_segment_prompt_image,
                                   send_prompt_to_server,
                                   confirm_segmentation_for_job)

jobs_blueprint = Blueprint('jobs', __name__)

@jobs_blueprint.route('/jobs', methods=['GET'])
def list_jobs():
    jobs = fetch_jobs_from_server()
    return jsonify(jobs)

@jobs_blueprint.route('/jobs/<job_id>', methods=['GET'])
def get_job_details(job_id):
    job_details = fetch_job_details(job_id)
    return jsonify(job_details)

@jobs_blueprint.route('/jobs/<job_id>/logs', methods=['GET'])
def get_job_logs(job_id):
    logs = fetch_job_logs(job_id)
    return logs

@jobs_blueprint.route('/jobs/<job_id>/colmap', methods=['POST'])
def start_colmap(job_id):
    return jsonify(trigger_colmap(job_id))

@jobs_blueprint.route('/jobs/<job_id>/mcmc', methods=['POST'])
def start_mcmc(job_id):
    return jsonify(trigger_mcmc(job_id))

@jobs_blueprint.route('/jobs/<job_id>/segmentationPreparation', methods=['POST'])
def start_segmentation_preparation(job_id):
    return jsonify(trigger_segmentation_preparation(job_id))

@jobs_blueprint.route('/jobs/<job_id>/segmentationPromptImage', methods=['GET'])
def get_segment_prompt_image(job_id):
    return fetch_segment_prompt_image(job_id)

@jobs_blueprint.route('/jobs/<job_id>/segmentationPrompt', methods=['POST'])
def send_segmentation_prompt(job_id):
    data = request.get_json()
    return jsonify(send_prompt_to_server(job_id, data))

@jobs_blueprint.route('/jobs/<job_id>/confirmSegmentation', methods=['POST'])
def confirm_segmentation(job_id):
    confirm_segmentation_for_job(job_id)
    return jsonify({"status": "ok"})

@jobs_blueprint.route('/jobs/<job_id>/frosting', methods=['POST'])
def start_frosting(job_id):
    return jsonify(trigger_frosting(job_id))
