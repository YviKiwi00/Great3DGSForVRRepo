from fastapi import APIRouter
from services.segmentation_service import (run_segmentation_preparation,
                                           run_gaussian_segmentation)

router = APIRouter()

@router.post("/jobs/{job_id}/segmentationPreparation")
def trigger_segmentation_preparation(job_id: str):
    run_segmentation_preparation(job_id)
    return {"status": "segmentation_preparation_started"}

@router.post("/jobs/{job_id}/gaussianSegmentation")
def trigger_segmentation_preparation(job_id: str):
    run_gaussian_segmentation(job_id)
    return {"status": "gaussian_segmentation_started"}