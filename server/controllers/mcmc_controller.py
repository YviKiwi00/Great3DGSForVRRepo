from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.mcmc_service import run_mcmc

router = APIRouter()

@router.post("/jobs/{job_id}/mcmc")
def trigger_mcmc(job_id: str):
    try:
        response = run_mcmc(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)