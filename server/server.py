import os
import sys
from fastapi import FastAPI
from controllers.jobs_controller import router as jobs_router
from controllers.colmap_controller import router as colmap_router
from controllers.mcmc_controller import router as mcmc_router
from controllers.segmentation_controller import router as segmentation_router

sys.path.append(os.path.dirname(__file__))

app = FastAPI()

app.include_router(jobs_router)
app.include_router(colmap_router)
app.include_router(mcmc_router)
app.include_router(segmentation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)