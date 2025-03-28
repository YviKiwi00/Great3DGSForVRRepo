from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.frosting_service import run_frosting_whole, run_frosting_seg

router = APIRouter()

@router.post("/jobs/{job_id}/frosting_whole")
def trigger_frosting_whole(job_id: str):
    try:
        response = run_frosting_whole(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/jobs/{job_id}/frosting_seg")
def trigger_frosting(job_id: str):
    try:
        response = run_frosting_seg(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)