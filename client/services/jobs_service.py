import requests

API_BASE = "http://localhost:5000"

def fetch_jobs_from_server():
    response = requests.get(f"{API_BASE}/jobs")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch jobs: {response.text}")
    return response.json()