import subprocess
import os
from datetime import datetime

from services.jobs_service import (load_jobs,
                                   save_jobs)
from utils.jobs_utils import (log_file_and_console,
                              UPLOAD_DIR,
                              RESULTS_DIR)
from jobs_queue import enqueue_job

def run_frosting(job_id: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "job_queued"
    save_jobs(jobs)

    enqueue_job(job_id, frosting_whole_subprocess, "FROSTING_WHOLE")
    enqueue_job(job_id, frosting_seg_subprocess, "FROSTING_SEG")

    return {"job_id": job_id, "status": jobs[job_id]["status"]}

def frosting_whole_subprocess(job_id: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "Frosting"))
    script_path = os.path.join(script_dir, "train_full_pipeline.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{UPLOAD_DIR}", f"{job_id}"))
    gs_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}", "frosting", "whole"))

    os.makedirs(results_dir, exist_ok=True)

    ply_name = "point_cloud.ply"

    export_obj = str(True)
    use_occlusion_culling = str(False)
    regularization_type = "dn_consistency"
    gaussians_in_frosting = str(4_000_000)

    cmd = [
        "python", script_path,
        "--scene_path", source_path,
        "--gs_output_dir", gs_output_dir,
        "--results_dir", results_dir,
        "--ply_name", ply_name,
        "--export_obj", export_obj,
        "--use_occlusion_culling", use_occlusion_culling,
        "--regularization_type", regularization_type,
        "--gaussians_in_frosting", gaussians_in_frosting,
    ]

    jobs = load_jobs()
    jobs[job_id]["status"] = "running_frosting"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Starting Frosting Training for whole Scene for Job {job_id} ==========\n")

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
        jobs = load_jobs()
        jobs[job_id]["status"] = "failed_frosting"
        save_jobs(jobs)
        log_file_and_console(job_id, f"Frosting Training for whole scene failed with code {exit_code}\n")
        raise Exception(f"Frosting Training for whole scene failed with code {exit_code}")

    jobs = load_jobs()
    jobs[job_id]["status"] = "done_frosting"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Frosting Training for whole scene for Job {job_id} finished. ==========\n")

def frosting_seg_subprocess(job_id: str):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "great3dgsforvr", "Frosting"))
    script_path = os.path.join(script_dir, "train_full_pipeline.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir

    source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{UPLOAD_DIR}", f"{job_id}"))
    gs_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}"))
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"{RESULTS_DIR}", f"{job_id}", "frosting", "segmented"))

    os.makedirs(results_dir, exist_ok=True)

    ply_name = "point_cloud_seg_gd.ply"

    export_obj = str(True)
    use_occlusion_culling = str(False)
    regularization_type = "dn_consistency"
    gaussians_in_frosting = str(4_000_000)

    cmd = [
        "python", script_path,
        "--scene_path", source_path,
        "--gs_output_dir", gs_output_dir,
        "--results_dir", results_dir,
        "--ply_name", ply_name,
        "--export_obj", export_obj,
        "--use_occlusion_culling", use_occlusion_culling,
        "--regularization_type", regularization_type,
        "--gaussians_in_frosting", gaussians_in_frosting,
    ]

    jobs = load_jobs()
    jobs[job_id]["status"] = "running_frosting"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Starting Frosting Training for segmented object for Job {job_id} ==========\n")

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
        jobs = load_jobs()
        jobs[job_id]["status"] = "failed_frosting"
        save_jobs(jobs)
        log_file_and_console(job_id, f"Frosting Training for segmented object failed with code {exit_code}\n")
        raise Exception(f"Frosting Training for segmented object failed with code {exit_code}")

    jobs = load_jobs()
    jobs[job_id]["status"] = "done_frosting"
    save_jobs(jobs)

    log_file_and_console(job_id, f"========== Frosting Training for segmented object for Job {job_id} finished. ==========\n")