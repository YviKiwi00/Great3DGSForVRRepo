import requests

API_BASE = "http://localhost:5000"

def handle_image_upload(files, project_name):
    files_to_send = []
    for file in files:
        files_to_send.append(('files', (file.filename, file.stream, file.content_type)))

    response = requests.post(f"{API_BASE}/jobs/start", files=files_to_send, data={'project_name': project_name})
    response_data = response.json()

    if response.status_code != 200 or "job_id" not in response_data:
        raise Exception(f"Upload to server failed: {response.text}")

    return response_data["job_id"]