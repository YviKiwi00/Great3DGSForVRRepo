import os
import uuid
import shutil
import base64
import json
import threading

from typing import List
from fastapi import UploadFile
from fastapi.responses import FileResponse

from services.colmap_service import run_colmap
from services.mcmc_service import run_3dgsmcmc

STORAGE_DIR = "storage"
UPLOAD_DIR = os.path.join(STORAGE_DIR, "uploads")
LOGS_DIR = os.path.join(STORAGE_DIR, "logs")
JOBS_FILE = os.path.join(STORAGE_DIR, "jobs.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

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
        return f.read()

def get_prompt_image(job_id: str):
    image_folder = f"storage/uploads/{job_id}/input"
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        raise Exception("No images found for this job.")

    first_image = os.path.join(image_folder, images[0])
    return FileResponse(first_image)

def handle_segmentation_prompt(job_id: str, point: dict):
    x, y = point['x'], point['y']

    jobs = load_jobs()
    job = jobs.get(job_id)

    if not job:
        raise Exception(f"Job {job_id} not found")

    job["latest_prompt"] = {"x": x, "y": y}
    save_jobs(jobs)

    # TODO Segmentation Preview

    preview_paths = [
        "static/dummy1.jpg",
        "static/dummy2.jpg",
        "static/dummy3.jpg"
    ]
    previews = [encode_image_as_base64(p) for p in preview_paths]

    return {"previews": previews}

def encode_image_as_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def confirm_segmentation_for_job(job_id: str):
    jobs = load_jobs()
    job = jobs.get(job_id)

    if not job:
        raise Exception(f"Job {job_id} not found")

    # TODO Start Segmentation

    job["status"] = "awaiting_final_processing"
    save_jobs(jobs)

    return {"status": "ok"}

def send_final_result_zip(job_id):
    result_folder = f"storage/results/{job_id}"
    os.makedirs(result_folder, exist_ok=True)
    result_zip = os.path.join(result_folder, "final_result.zip")

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
        "status": "running",
        "log_file": os.path.join(LOGS_DIR, f"{job_id}.log")
    }
    save_jobs(jobs)

    # Start thread in background
    thread = threading.Thread(target=process_job, args=(job_id, project_folder))
    thread.daemon = True
    thread.start()

    return job_id

def process_job(job_id: str, folder: str):
    log_file = os.path.join(LOGS_DIR, f"{job_id}.log")
    with open(log_file, 'w') as log:
        log.write(f"Job {job_id} gestartet für Ordner: {folder}\n")
        log.flush()

    source_path = f"storage/uploads/{job_id}"
    output_path = f"storage/results/{job_id}"

    try:
        # COLMAP
        run_colmap(job_id, source_path, resize=True)
        # 3DGS MCMC Training
        run_3dgsmcmc(job_id, source_path, output_path)
        # TODO SegTrain

        jobs = load_jobs()
        jobs[job_id]["status"] = "ready_for_segmentation"
        save_jobs(jobs)

    except Exception as e:
        with open(log_file, 'a') as log:
            log.write(f"Error during training: {str(e)}\n")
            log.flush()

        jobs = load_jobs()
        jobs[job_id]["status"] = "failed"
        save_jobs(jobs)

