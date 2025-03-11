import threading
import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              UPLOAD_DIR)

def run_colmap(job_id: str):
    jobs = load_jobs()
    if "running" in jobs[job_id]["status"]:
        raise Exception(f"Job {job_id} is running a process already!")

    jobs[job_id]["status"] = "running_colmap"
    save_jobs(jobs)

    def worker():
        try:
            source_path = os.path.join(UPLOAD_DIR, f"{job_id}")
            colmap_subprocess(job_id, source_path, resize=True)

            jobs = load_jobs()
            jobs[job_id]["status"] = "done_colmap"
            save_jobs(jobs)
        except Exception as e:
            jobs = load_jobs()
            jobs[job_id]["status"] = "failed_colmap"
            save_jobs(jobs)

            log_file_and_console(job_id, f"Error in Colmap: {str(e)}\n")

    threading.Thread(target=worker, daemon=True).start()

def colmap_subprocess(job_id: str, source_path: str, resize: bool = False):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "3dgs-mcmc"))
    script_path = os.path.join(script_dir, "convert.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    cmd = [
        "python", script_path,
        "--source_path", source_path,
    ]

    if resize:
        cmd.append("--resize")

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
        log_file_and_console(job_id, "Colmap Conversion failed with code {exit_code}\n")
        raise Exception(f"Colmap Conversion failed with code {exit_code}")

    log_file_and_console(job_id, f"========== Colmap Conversion for Job {job_id} finished. ==========\n")