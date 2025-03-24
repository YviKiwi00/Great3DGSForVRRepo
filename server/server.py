import os
import sys
import uvicorn
import signal
from fastapi import FastAPI
from controllers.jobs_controller import router as jobs_router
from controllers.colmap_controller import router as colmap_router
from controllers.mcmc_controller import router as mcmc_router
from controllers.segmentation_controller import router as segmentation_router
from controllers.frosting_controller import router as frosting_router
from utils.jobs_utils import get_exp_values

from jobs_queue import start_worker, shutdown_handler

sys.path.append(os.path.dirname(__file__))

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

app = FastAPI()
app.include_router(jobs_router)
app.include_router(colmap_router)
app.include_router(mcmc_router)
app.include_router(segmentation_router)
app.include_router(frosting_router)

if __name__ == "__main__":
    mcmc_iterations, mcmc_cap_max, frosting_gauss = get_exp_values()
    print("Starting server with configuration:")
    print(f"MCMC_IT = {mcmc_iterations}")
    print(f"MCMC_CAP_MAX = {mcmc_cap_max}")
    print(f"FROSTING_GAUSS = {frosting_gauss}")

    start_worker()
    uvicorn.run(app, host="0.0.0.0", port=5000)