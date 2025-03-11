import threading
import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              RESULTS_DIR)

# ===== Segmentation Preparation ===== #
def run_segmentation_preparation(job_id: str):
    jobs = load_jobs()
    if "running" in jobs[job_id]["status"]:
        raise Exception(f"Job {job_id} is running a process already!")

    jobs[job_id]["status"] = "running_segmentation_preparation"
    save_jobs(jobs)

    def worker():
        try:
            model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
            segmentation_preparation_subprocess(job_id, model_path)

            jobs = load_jobs()
            jobs[job_id]["status"] = "done_segmentation_preparation"
            save_jobs(jobs)
        except Exception as e:
            jobs = load_jobs()
            jobs[job_id]["status"] = "failed_segmentation_preparation"
            save_jobs(jobs)

            log_file_and_console(job_id, f"Error in Segmentation Preparation: {str(e)}\n")

    threading.Thread(target=worker, daemon=True).start()

def segmentation_preparation_subprocess(job_id: str, model_path: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "SAGS"))
    script_path = os.path.join(script_dir, "prepare_segmentation.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    cmd = [
        "python", script_path,
        "--job_id", job_id,
        "--model_path", model_path
    ]

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
        log_file_and_console(job_id, "Segmentation Preparation failed with code {exit_code}\n")
        raise Exception(f"Segmentation Preparation failed with code {exit_code}")

    log_file_and_console(job_id, f"========== Segmentation Preparation for Job {job_id} finished. ==========\n")


# ===== Gaussian Segmentation ===== #
def run_gaussian_segmentation(job_id: str):
    jobs = load_jobs()
    if "running" in jobs[job_id]["status"]:
        raise Exception(f"Job {job_id} is running a process already!")

    jobs[job_id]["status"] = "running_gaussian_segmentation"
    save_jobs(jobs)

    def worker():
        try:
            model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
            gaussian_segmentation_subprocess(job_id, model_path)

            jobs = load_jobs()
            jobs[job_id]["status"] = "done_gaussian_segmentation"
            save_jobs(jobs)
        except Exception as e:
            jobs = load_jobs()
            jobs[job_id]["status"] = "failed_gaussian_segmentation"
            save_jobs(jobs)

            log_file_and_console(job_id, f"Error in Gaussian Segmentation: {str(e)}\n")

    threading.Thread(target=worker, daemon=True).start()

def gaussian_segmentation_subprocess(job_id: str, model_path: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "SAGS"))
    script_path = os.path.join(script_dir, "gaussian_segmentation.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    cmd = [
        "python", script_path,
        "--job_id", job_id,
        "--model_path", model_path
    ]

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
        log_file_and_console(job_id, "Gaussian Segmentation failed with code {exit_code}\n")
        raise Exception(f"Gaussian Segmentation failed with code {exit_code}")

    log_file_and_console(job_id, f"========== Gaussian Segmentation for Job {job_id} finished. ==========\n")