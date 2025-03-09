import threading
import subprocess
import os

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              UPLOAD_DIR,
                              RESULTS_DIR)

def run_mcmc(job_id: str):
    jobs = load_jobs()
    if "running" in jobs[job_id]["status"]:
        raise Exception(f"Job {job_id} is running a process already!")

    jobs[job_id]["status"] = "running_mcmc"
    save_jobs(jobs)

    def worker():
        try:
            source_path = os.path.join(UPLOAD_DIR, f"{job_id}")
            output_path = os.path.join(RESULTS_DIR, f"{job_id}")
            mcmc_subprocess(job_id, source_path, output_path)

            jobs = load_jobs()
            jobs[job_id]["status"] = "done_mcmc"
            save_jobs(jobs)
        except Exception as e:
            jobs = load_jobs()
            jobs[job_id]["status"] = "failed_mcmc"
            save_jobs(jobs)

            log_file_and_console(job_id, f"Error in MCMC: {str(e)}\n")

    threading.Thread(target=worker, daemon=True).start()

def mcmc_subprocess(job_id: str, source_path: str, output_path: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "3dgs-mcmc"))
    script_path = os.path.join(script_dir, "train.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    cap_max = str(10000000)
    scale_reg = str(0.01)
    opacity_reg = str(0.01)
    noise_lr = str(5e5)
    init_type = "random"

    cmd = [
        "python", script_path,
        "--source_path", source_path,
        "--model_path", output_path,
        "--cap_max", cap_max,
        "--scale_reg", scale_reg,
        "--opacity_reg", opacity_reg,
        "--noise_lr", noise_lr,
        "--init_type", init_type,
    ]

    log_file_and_console(job_id, f"========== Starting first 7000 Iterations of 3DGS-MCMC Training for Job {job_id} ==========\n")

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

    if exit_code != 0:
        log_file_and_console(job_id, f"3DGS-MCMC Training failed with code {exit_code}\n")
        raise Exception(f"3DGS-MCMC Training failed with code {exit_code}")

    log_file_and_console(job_id, f"========== 3DGS-MCMC Training for Job {job_id} finished. ==========\n")