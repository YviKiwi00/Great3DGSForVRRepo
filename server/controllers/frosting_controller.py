from fastapi import APIRouter
from services.frosting_service import run_frosting

router = APIRouter()

@router.post("/jobs/{job_id}/frosting")
def trigger_frosting(job_id: str):
    run_frosting(job_id)
    return {"status": "forsting_started"}