import requests

API_BASE = "http://localhost:5000"

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