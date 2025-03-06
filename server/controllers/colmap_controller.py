from fastapi import APIRouter
from services.colmap_service import run_colmap

router = APIRouter()

@router.post("/jobs/{job_id}/colmap")
def trigger_colmap(job_id: str):
    run_colmap(job_id)
    return {"status": "colmap_started"}