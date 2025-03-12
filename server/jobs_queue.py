import threading
import sys
import queue
from services.jobs_service import load_jobs, save_jobs
from utils.jobs_utils import log_file_and_console

job_queue = queue.Queue()

def job_worker():
    while True:
        job_id, process_function, process_name = job_queue.get()

        log_file_and_console(job_id, f"Starting {process_name} for job {job_id}...\n")

        try:
            process_function(job_id)
        except Exception as e:
            log_file_and_console(job_id, f"Error in {process_name} for job {job_id}: {str(e)}\n")

        log_file_and_console(job_id, f"{process_name} for job {job_id} completed.\n")

        jobs = load_jobs()
        if job_id in jobs and "queued_processes" in jobs[job_id]:
            jobs[job_id]["queued_processes"] = max(0, jobs[job_id]["queued_processes"] - 1)
            save_jobs(jobs)

        job_queue.task_done()

def enqueue_job(job_id, process_function, process_name):
    jobs = load_jobs()

    if job_id not in jobs:
        raise Exception(f"Job {job_id} not found!")

    if "queued_processes" not in jobs[job_id]:
        jobs[job_id]["queued_processes"] = 0
    jobs[job_id]["queued_processes"] += 1
    save_jobs(jobs)

    job_queue.put((job_id, process_function, process_name))
    log_file_and_console(job_id, f"Queued {process_name} for job {job_id}\n")

def start_worker():
    worker_thread = threading.Thread(target=job_worker)
    worker_thread.daemon = True
    worker_thread.start()

def shutdown_handler(signum, frame):
    print("Server shutting down, job queue gets emptied...\n")

    jobs = load_jobs()
    for job_id, job_data in jobs.items():
        if "running" in job_data["status"]:
            log_file_and_console(job_id, f"{job_data['status']} for {job_id} got cancelled because of Server-Shutdown.\n")
            job_data["status"] = "failed"
        if "job_queued" in job_data["status"]:
            log_file_and_console(job_id, f"Queued Processes for {job_id} got removed because of Server-Shutdown.\n")
            job_data["status"] = "removed_job_queue"
        job_data["queued_processes"] = 0

    save_jobs(jobs)

    with job_queue.mutex:
        job_queue.queue.clear()

    print("Server shut down, bye bye.")

    sys.exit(0)