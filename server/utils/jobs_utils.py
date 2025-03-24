import os
import base64
import time
import requests
import json

API_BASE = "http://localhost:5000"

STORAGE_DIR = "storage"
UPLOAD_DIR = os.path.join(STORAGE_DIR, "uploads")
LOGS_DIR = os.path.join(STORAGE_DIR, "logs")
RESULTS_DIR = os.path.join(STORAGE_DIR, "results")
JOBS_FILE = os.path.join(STORAGE_DIR, "jobs.json")
LOCK_FILE = JOBS_FILE + ".lock"

EXP_FILE = os.path.join("exp_cfgs.json")

EXP_MCMC_ITERATIONS = 12_000      # Baseline is 12_000
EXP_MCMC_CAPMAX = 2_000_000      # Baseline is 2_000_000
EXP_FROSTING_GAUSS = 2_000_000   # Baseline is 2_000_000

def encode_image_as_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_exp_values():
    cfg_data = {}
    if os.path.exists(EXP_FILE):
        with open(EXP_FILE, 'r') as f:
            try:
                cfg_data = json.load(f)
            except json.decoder.JSONDecodeError:
                print("No exp_cfgs.json, returning empty json.")

    return cfg_data.get("mcmc_iterations", EXP_MCMC_ITERATIONS), cfg_data.get("mcmc_capMax", EXP_MCMC_CAPMAX), cfg_data.get("frosting_gauss", EXP_FROSTING_GAUSS)

def wait_for_job_status(job_id, api_base, target_status, timeout=14400): # 4 Stunden
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = requests.get(f"{api_base}/jobs/{job_id}")
        job = response.json()

        if target_status in job["status"]:
            return True
        elif "failed" in job["status"]:
            raise Exception(f"Job {job_id} failed while waiting for {target_status}")

        time.sleep(5)

    raise Exception(f"Timeout: Job {job_id} did not reach status {target_status} within {timeout} seconds")

def log_file_and_console(job_id, message: str):
    log_file = os.path.join(LOGS_DIR, f"{job_id}.log")

    with open(log_file, "a") as log:
        print(message, end="")
        log.write(message)
        log.flush()