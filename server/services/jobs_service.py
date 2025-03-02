import os
import uuid
import shutil
from typing import List
from fastapi import UploadFile
import json
import threading
import time

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

async def start_new_job(project_name: str, files: List[UploadFile]) -> str:
    job_id = str(uuid.uuid4())
    project_folder = os.path.join(UPLOAD_DIR, f"{project_name}_{job_id}")
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

    # Hintergrund-Thread starten
    threading.Thread(target=process_job, args=(job_id, project_folder)).start()

    return job_id

def process_job(job_id: str, folder: str):
    log_file = os.path.join(LOGS_DIR, f"{job_id}.log")
    with open(log_file, 'w') as log:
        log.write(f"Job {job_id} gestartet für Ordner: {folder}\n")
        log.flush()

        # Dummy-Rechenprozess simulieren (später: Calibration + 3DGS MCMC + SegTransform)
        time.sleep(5)
        log.write(f"Job {job_id} abgeschlossen.\n")

    jobs = load_jobs()
    jobs[job_id]["status"] = "ready_for_segmentation"
    save_jobs(jobs)