import os
import sys
from fastapi import FastAPI
from controllers.jobs_controller import router as jobs_router

sys.path.append(os.path.dirname(__file__))

app = FastAPI()

app.include_router(jobs_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)