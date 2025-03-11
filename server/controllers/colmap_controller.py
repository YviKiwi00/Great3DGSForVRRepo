from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.colmap_service import run_colmap

router = APIRouter()

@router.post("/jobs/{job_id}/colmap")
def trigger_colmap(job_id: str):
    try:
        response = run_colmap(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)