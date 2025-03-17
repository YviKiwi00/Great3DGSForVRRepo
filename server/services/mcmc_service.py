import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              UPLOAD_DIR,
                              RESULTS_DIR,
                              EXP_MCMC_ITERATIONS,
                              EXP_MCMC_CAPMAX)
from jobs_queue import enqueue_job

def run_mcmc(job_id: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "job_queued"
    save_jobs(jobs)

    enqueue_job(job_id, mcmc_subprocess, "MCMC")

    return {"job_id": job_id, "status": jobs[job_id]["status"]}

def mcmc_subprocess(job_id: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "3dgs-mcmc"))
    script_path = os.path.join(script_dir, "train.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    source_path = os.path.join(UPLOAD_DIR, f"{job_id}")
    output_path = os.path.join(RESULTS_DIR, f"{job_id}")

    iterations = str(EXP_MCMC_ITERATIONS)
    cap_max = str(EXP_MCMC_CAPMAX)
    scale_reg = str(0.01)
    opacity_reg = str(0.01)
    noise_lr = str(5e5)
    init_type = "random"

    cmd = [
        "python", script_path,
        "--source_path", source_path,
        "--model_path", output_path,
        "--iterations", iterations,
        "--cap_max", cap_max,
        "--scale_reg", scale_reg,
        "--opacity_reg", opacity_reg,
        "--noise_lr", noise_lr,
        "--init_type", init_type,
    ]

    jobs = load_jobs()
    jobs[job_id]["status"] = "running_mcmc"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Starting first 7000 Iterations of 3DGS-MCMC Training for Job {job_id} ==========\n")

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
        jobs[job_id]["status"] = "failed_mcmc"
        save_jobs(jobs)
        log_file_and_console(job_id, f"3DGS-MCMC Training failed with code {exit_code}\n")
        raise Exception(f"3DGS-MCMC Training failed with code {exit_code}")

    jobs = load_jobs()
    jobs[job_id]["status"] = "done_mcmc"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== 3DGS-MCMC Training for Job {job_id} finished. ==========\n")