import threading
import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              UPLOAD_DIR,
                              RESULTS_DIR)

def run_frosting(job_id: str):
    jobs = load_jobs()
    if "running" in jobs[job_id]["status"]:
        raise Exception(f"Job {job_id} is running a process already!")

    jobs[job_id]["status"] = "running_frosting"
    save_jobs(jobs)

    def worker():
        try:
            source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{UPLOAD_DIR}", f"{job_id}"))
            output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
            frosting_subprocess(job_id, source_path, output_path)

            jobs = load_jobs()
            jobs[job_id]["status"] = "done_frosting"
            save_jobs(jobs)
        except Exception as e:
            jobs = load_jobs()
            jobs[job_id]["status"] = "failed_frosting"
            save_jobs(jobs)

            log_file_and_console(job_id, f"Error in Frosting: {str(e)}\n")

    threading.Thread(target=worker, daemon=True).start()

def frosting_subprocess(job_id: str, source_path: str, output_path: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "Frosting"))
    script_path = os.path.join(script_dir, "train_full_pipeline.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    export_obj = str(True)
    use_occlusion_culling = str(False)
    regularization_type = "dn_consistency"
    gaussians_in_frosting = str(2_000_000)

    cmd = [
        "python", script_path,
        "--scene_path", source_path,
        "--gs_output_dir", output_path,
        "--export_obj", export_obj,
        "--use_occlusion_culling", use_occlusion_culling,
        "--regularization_type", regularization_type,
        "--gaussians_in_frosting", gaussians_in_frosting,
    ]

    log_file_and_console(job_id, f"========== Starting Frosting Training for Job {job_id} ==========\n")

    start_time = datetime.now()
    log_file_and_console(job_id, f"===== Start-Time: {start_time} =====\n")

    process = subprocess.Popen(
        cmd,
        cwd=script_dir,
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
        log_file_and_console(job_id, f"Frosting Training failed with code {exit_code}\n")
        raise Exception(f"Frosting Training failed with code {exit_code}")

    log_file_and_console(job_id, f"========== Frosting Training for Job {job_id} finished. ==========\n")