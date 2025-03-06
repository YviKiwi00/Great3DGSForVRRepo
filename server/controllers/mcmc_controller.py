from fastapi import APIRouter
from services.mcmc_service import run_mcmc

router = APIRouter()

@router.post("/jobs/{job_id}/mcmc")
def trigger_mcmc(job_id: str):
    run_mcmc(job_id)
    return {"status": "mcmc_started"}