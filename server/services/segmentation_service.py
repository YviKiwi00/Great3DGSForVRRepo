import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              RESULTS_DIR)
from jobs_queue import enqueue_job

# ===== Segmentation Preparation ===== #
def run_segmentation_preparation(job_id: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "job_queued"
    save_jobs(jobs)

    enqueue_job(job_id, segmentation_preparation_subprocess, "SEG_PREP")

    return {"job_id": job_id, "status": jobs[job_id]["status"]}

def segmentation_preparation_subprocess(job_id: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "SAGS"))
    script_path = os.path.join(script_dir, "prepare_segmentation.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
    iterations_to_load = str(15_000)

    cmd = [
        "python", script_path,
        "--job_id", job_id,
        "--model_path", model_path,
        "--iteration", iterations_to_load
    ]

    jobs = load_jobs()
    jobs[job_id]["status"] = "running_segmentation_preparation"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Starting Segmentation Preparation for Job {job_id} ==========\n")

    start_time = datetime.now()
    log_file_and_console(job_id, f"===== Start-Time: {start_time} =====\n")

    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=script_dir
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
        jobs[job_id]["status"] = "failed_segmentation_preparation"
        save_jobs(jobs)
        log_file_and_console(job_id, "Segmentation Preparation failed with code {exit_code}\n")
        raise Exception(f"Segmentation Preparation failed with code {exit_code}")

    jobs = load_jobs()
    jobs[job_id]["status"] = "done_segmentation_preparation"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Segmentation Preparation for Job {job_id} finished. ==========\n")


# ===== Gaussian Segmentation ===== #
def run_gaussian_segmentation(job_id: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "job_queued"
    save_jobs(jobs)

    enqueue_job(job_id, gaussian_segmentation_subprocess, "GAUSSIAN_SEG")

    return {"job_id": job_id, "status": jobs[job_id]["status"]}

def gaussian_segmentation_subprocess(job_id: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "SAGS"))
    script_path = os.path.join(script_dir, "gaussian_segmentation.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
    iterations_to_load = str(15_000)

    cmd = [
        "python", script_path,
        "--job_id", job_id,
        "--model_path", model_path,
        "--iteration", iterations_to_load
    ]

    jobs = load_jobs()
    jobs[job_id]["status"] = "running_gaussian_segmentation"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Starting Gaussian Segmentation for Job {job_id} ==========\n")

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
        jobs[job_id]["status"] = "failed_gaussian_segmentation"
        save_jobs(jobs)
        log_file_and_console(job_id, "Gaussian Segmentation failed with code {exit_code}\n")
        raise Exception(f"Gaussian Segmentation failed with code {exit_code}")

    jobs = load_jobs()
    jobs[job_id]["status"] = "done_gaussian_segmentation"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Gaussian Segmentation for Job {job_id} finished. ==========\n")