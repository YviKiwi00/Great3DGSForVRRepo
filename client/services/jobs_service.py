import requests
from flask import jsonify

API_BASE = "http://localhost:5000"

def handle_image_upload(files, project_name):
    files_to_send = []
    for file in files:
        files_to_send.append(('files', (file.filename, file.stream, file.content_type)))

    response = requests.post(f"{API_BASE}/jobs/start", files=files_to_send, data={'project_name': project_name})
    response_data = response.json()

    if response.status_code != 200 or "job_id" not in response_data:
        raise Exception(f"Upload to server failed: {response.text}")

    return response_data

def fetch_jobs_from_server():
    response = requests.get(f"{API_BASE}/jobs")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch jobs: {response.text}")
    return response.json()

def fetch_job_details(job_id):
    response = requests.get(f"{API_BASE}/jobs/{job_id}")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch job details: {response.text}")
    return response.json()

def fetch_job_logs(job_id):
    response = requests.get(f"{API_BASE}/jobs/{job_id}/logs")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch logs: {response.text}")
    return response.text

def trigger_colmap(job_id):
    response = requests.post(f"{API_BASE}/jobs/{job_id}/colmap")
    if response.status_code != 200:
        raise Exception(f"Failed to start Colmap for job {job_id}: {response.text}")
    return response.json()

def trigger_mcmc(job_id):
    response = requests.post(f"{API_BASE}/jobs/{job_id}/mcmc")
    if response.status_code != 200:
        raise Exception(f"Failed to start MCMC for job {job_id}: {response.text}")
    return response.json()

def trigger_segmentation_preparation(job_id):
    response = requests.post(f"{API_BASE}/jobs/{job_id}/segmentationPreparation")
    if response.status_code != 200:
        raise Exception(f"Failed to start Segmentation Preparation for job {job_id}: {response.text}")
    return response.json()

def fetch_segment_prompt_image(job_id):
    response = requests.get(f"{API_BASE}/jobs/{job_id}/segmentationPromptImage")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch prompt image: {response.text}")
    return response.content

def send_prompt_to_server(job_id, point):
    response = requests.post(f"{API_BASE}/jobs/{job_id}/segmentationPrompt", json=point)
    if response.status_code != 200:
        raise Exception(f"Failed to send segmentation prompt: {response.text}")
    return response.json()

def confirm_segmentation_for_job(job_id):
    response = requests.post(f"{API_BASE}/jobs/{job_id}/confirmSegmentation")
    if response.status_code != 200:
        raise Exception(f"Failed to confirm segmentation: {response.text}")
    return response.json()

def trigger_frosting(job_id):
    response = requests.post(f"{API_BASE}/jobs/{job_id}/frosting")
    if response.status_code != 200:
        raise Exception(f"Failed to start Frosting for job {job_id}: {response.text}")
    return response.json()

def download_result(job_id):
    response = requests.get(f"{API_BASE}/jobs/{job_id}/downloadResult")

    if response.status_code != 200:
        return jsonify({"error": f"Failed to download result for job {job_id}: {response.text}"}), 500

    return response.content, response.status_code, {
        "Content-Type": response.headers["Content-Type"],
        "Content-Disposition": response.headers.get("Content-Disposition",
                                                    f'attachment; filename="{job_id}_result.zip"')
    }