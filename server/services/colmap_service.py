import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              UPLOAD_DIR)
from jobs_queue import enqueue_job

def run_colmap(job_id: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "job_queued"
    save_jobs(jobs)

    enqueue_job(job_id, colmap_subprocess, "COLMAP")

    return {"job_id": job_id, "status": jobs[job_id]["status"]}

def colmap_subprocess(job_id: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "3dgs-mcmc"))
    script_path = os.path.join(script_dir, "convert.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    source_path = os.path.join(UPLOAD_DIR, f"{job_id}")

    camera = "OPENCV"

    cmd = [
        "python", script_path,
        "--source_path", source_path,
        "--camera", camera,
        "--resize"
    ]

    jobs = load_jobs()
    jobs[job_id]["status"] = "running_colmap"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Starting Colmap-Conversion for Job {job_id} ==========\n")

    start_time = datetime.now()
    log_file_and_console(job_id, f"===== Start-Time: {start_time} =====\n")

    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Log-Streaming Loop
    for line in process.stdout:
        log_file_and_console(job_id, line)

    exit_code = process.wait()

    end_time = datetime.now()
    duration = end_time - start_time

    log_file_and_console(job_id, f"===== End-Time: {end_time}; Duration: {duration} =====\n")

    if exit_code != 0:
        jobs = load_jobs()
        jobs[job_id]["status"] = "failed_colmap"
        save_jobs(jobs)
        log_file_and_console(job_id, "Colmap Conversion failed with code {exit_code}\n")
        raise Exception(f"Colmap Conversion failed with code {exit_code}")

    jobs = load_jobs()
    jobs[job_id]["status"] = "done_colmap"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Colmap Conversion for Job {job_id} finished. ==========\n")