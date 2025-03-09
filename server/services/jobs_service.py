import os
import uuid
import shutil
import json
import threading
import requests
import subprocess

from typing import List
from fastapi import UploadFile
from fastapi.responses import FileResponse
from utils.jobs_utils import ( API_BASE,
                               UPLOAD_DIR,
                               LOGS_DIR,
                               RESULTS_DIR,
                               JOBS_FILE,
                               wait_for_job_status,
                               log_file_and_console )

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_jobs():
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_jobs(jobs):
    with open(JOBS_FILE, 'w') as f:
        json.dump(jobs, f, indent=2)

def get_all_jobs():
    jobs = load_jobs()
    return [
        {
            "id": job_id,
            "project_name": data["project_name"],
            "status": data["status"]
        }
        for job_id, data in jobs.items()
    ]

def get_job_details(job_id: str):
    jobs = load_jobs()
    job = jobs.get(job_id)

    if not job:
        raise Exception(f"Job {job_id} not found")

    return {
        "id": job_id,
        "project_name": job["project_name"],
        "status": job["status"],
        "log_file": job.get("log_file", "")
    }

def get_job_logs(job_id: str) -> str:
    jobs = load_jobs()
    job = jobs.get(job_id)

    if not job or "log_file" not in job:
        return f"Log für Job {job_id} nicht gefunden."

    log_path = job["log_file"]
    if not os.path.exists(log_path):
        return f"Logdatei {log_path} nicht gefunden."

    with open(log_path, "r") as f:
        lines = f.readlines()

    tail = lines[-2000:] if len(lines) > 2000 else lines

    return "".join(tail)

def get_prompt_image(job_id: str):
    image_file = os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "SAGS", "render_images", f"render_image_{job_id}.png")
    return FileResponse(image_file)

def handle_segmentation_prompt(job_id: str, point: dict):
    x, y = point['x'], point['y']

    jobs = load_jobs()
    job = jobs.get(job_id)

    if not job:
        raise Exception(f"Job {job_id} not found")

    job["latest_prompt"] = {"x": x, "y": y}
    save_jobs(jobs)

    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "SAGS"))
    env = {**os.environ, "PYTHONPATH": script_dir}

    result = subprocess.run(
        ["python", "-c",
         f"import json; import preview_segmentation as prev_seg; print(json.dumps(prev_seg.preview_segmentation('{job_id}', {x}, {y})))"],
        env=env,
        cwd=script_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Segmentation Preview failed: {result.stderr}")

    previews = json.loads(result.stdout.strip())

    # preview_paths = [
    #     "static/dummy1.jpg",
    #     "static/dummy2.jpg",
    #     "static/dummy3.jpg"
    # ]
    # previews = [encode_image_as_base64(p) for p in preview_paths]

    return {"previews": previews}

def confirm_segmentation_for_job(job_id: str):
    jobs = load_jobs()
    job = jobs.get(job_id)

    if not job:
        raise Exception(f"Job {job_id} not found")

    # Gaussian Segmentation
    response = requests.post(f"{API_BASE}/jobs/{job_id}/gaussianSegmentation")
    if response.status_code != 200:
        raise Exception(f"Gaussian Segmentation failed: {response.text}")

    return response.json()

def send_final_result_zip(job_id):
    result_zip = os.path.join(RESULTS_DIR, f"final_result_{job_id}.zip")

    if not os.path.exists(result_zip):
        raise Exception(f"Result ZIP for job {job_id} not found")

    return FileResponse(result_zip, filename=f"{job_id}_result.zip")

async def start_new_job(project_name: str, files: List[UploadFile]) -> str:
    job_id = str(uuid.uuid4())
    project_folder = os.path.join(UPLOAD_DIR, f"{job_id}")
    os.makedirs(project_folder)

    input_folder = os.path.join(project_folder, "input")
    os.makedirs(input_folder)

    for file in files:
        file_path = os.path.join(input_folder, file.filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

    jobs = load_jobs()
    jobs[job_id] = {
        "project_name": project_name,
        "status": "started",
        "log_file": os.path.join(LOGS_DIR, f"{job_id}.log")
    }
    save_jobs(jobs)

    # Start thread in background
    thread = threading.Thread(target=process_job, args=(job_id, project_folder))
    thread.daemon = True
    thread.start()

    return job_id

def process_job(job_id: str, folder: str):
    log_file_and_console(job_id, f"Job {job_id} started for {folder}\n")

    try:
        # COLMAP
        response = requests.post(f"{API_BASE}/jobs/{job_id}/colmap")
        if response.status_code != 200:
            raise Exception(f"Colmap failed: {response.text}")
        wait_for_job_status(job_id, API_BASE, "done")

        # 3DGS MCMC Training
        response = requests.post(f"{API_BASE}/jobs/{job_id}/mcmc")
        if response.status_code != 200:
            raise Exception(f"MCMC failed: {response.text}")
        wait_for_job_status(job_id, API_BASE, "done")

        # Segmentation Preparation
        response = requests.post(f"{API_BASE}/jobs/{job_id}/segmentationPreparation")
        if response.status_code != 200:
            raise Exception(f"Segmentation Preparation failed: {response.text}")
        wait_for_job_status(job_id, API_BASE, "done")

    except Exception as e:
        log_file_and_console(job_id, f"Error during training: {str(e)}\n")

        jobs = load_jobs()
        if not "failed" in jobs[job_id]["status"]:
            jobs[job_id]["status"] = "failed"
            save_jobs(jobs)

