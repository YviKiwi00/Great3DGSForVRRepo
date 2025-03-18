from flask import Blueprint, jsonify, request

from services.jobs_service import (handle_image_upload,
                                   fetch_jobs_from_server,
                                   fetch_job_details,
                                   fetch_job_logs,
                                   trigger_colmap,
                                   trigger_mcmc,
                                   trigger_segmentation_preparation,
                                   trigger_frosting_whole,
                                   trigger_frosting_seg,
                                   fetch_segment_prompt_image,
                                   send_prompt_to_server,
                                   confirm_segmentation_for_job,
                                   download_result)

jobs_blueprint = Blueprint('jobs', __name__)

@jobs_blueprint.route('/imageUpload', methods=['POST'])
def image_upload():
    files = request.files.getlist('files')
    project_name = request.form.get('projectName', 'UnnamedProject')

    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    response = handle_image_upload(files, project_name)
    return jsonify(response)

@jobs_blueprint.route('/jobs', methods=['GET'])
def list_jobs():
    return jsonify(fetch_jobs_from_server())

@jobs_blueprint.route('/jobs/<job_id>', methods=['GET'])
def get_job_details(job_id):
    return jsonify(fetch_job_details(job_id))

@jobs_blueprint.route('/jobs/<job_id>/logs', methods=['GET'])
def get_job_logs(job_id):
    return fetch_job_logs(job_id)

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
    return jsonify(confirm_segmentation_for_job(job_id))

@jobs_blueprint.route('/jobs/<job_id>/frosting_whole', methods=['POST'])
def start_frosting_whole(job_id):
    return jsonify(trigger_frosting_whole(job_id))

@jobs_blueprint.route('/jobs/<job_id>/frosting_seg', methods=['POST'])
def start_frosting_seg(job_id):
    return jsonify(trigger_frosting_seg(job_id))

@jobs_blueprint.route('/jobs/<job_id>/download', methods=['GET'])
def download_final_result(job_id):
    return download_result(job_id)
