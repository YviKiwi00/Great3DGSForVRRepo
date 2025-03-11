from flask import Blueprint, request, jsonify
from services.upload_service import handle_image_upload

upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/imageUpload', methods=['POST'])
def image_upload():
    files = request.files.getlist('files')
    project_name = request.form.get('projectName', 'UnnamedProject')

    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    response = handle_image_upload(files, project_name)
    return response.json()