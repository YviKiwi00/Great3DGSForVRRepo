from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.segmentation_service import (run_segmentation_preparation,
                                           run_gaussian_segmentation)

router = APIRouter()

@router.post("/jobs/{job_id}/segmentationPreparation")
def trigger_segmentation_preparation(job_id: str):
    try:
        response = run_segmentation_preparation(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/jobs/{job_id}/gaussianSegmentation")
def trigger_gaussian_segmentation(job_id: str):
    try:
        response = run_gaussian_segmentation(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)