import subprocess
import os

def run_3dgsmcmc(job_id: str, source_path: str, output_path: str):
    script_path = os.path.join(
        os.path.dirname(__file__),
        "..", "great3dgsforvr", "3dgs-mcmc", "train.py"
    )

    cap_max = 10000000
    scale_reg = 0.01
    opacity_reg = 0.01
    noise_lr = 5e5
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

    log_file = f"storage/logs/{job_id}.log"

    with open(log_file, "a") as log:
        log.write(f"========== Starting first 7000 Iterations of 3DGS-MCMC Training for Job {job_id} ==========\n")
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
            log.write(f"3DGS-MCMC Training failed with code {exit_code}\n")
            log.flush()
            raise Exception(f"3DGS-MCMC Training failed with code {exit_code}")

        log.write(f"========== 3DGS-MCMC Training for Job {job_id} finished. ==========\n")
        log.flush()