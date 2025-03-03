import subprocess
import os

def run_colmap(job_id: str, source_path: str, resize: bool = False):
    script_path = os.path.join(
        os.path.dirname(__file__),
        "..", "great3dgsforvr", "3dgs-mcmc", "convert.py")

    cmd = [
        "python", script_path,
        "--source_path", source_path,
    ]

    if resize:
        cmd.append("--resize")

    log_file = f"storage/logs/{job_id}.log"

    with open(log_file, "a") as log:
        log.write(f"========== Starting Colmap-Conversion for Job {job_id} ==========\n")
        log.flush()

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Log-Streaming Loop
        for line in process.stdout:
            log.write(line)
            log.flush()

        exit_code = process.wait()

        if exit_code != 0:
            log.write(f"Colmap Conversion failed with code {exit_code}\n")
            log.flush()
            raise Exception(f"Colmap Conversion failed with code {exit_code}")

        log.write(f"========== Colmap Conversion for Job {job_id} finished. ==========\n")
        log.flush()