from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from typing import List
from services.jobs_service import (get_all_jobs,
                                   start_new_job,
                                   get_job_details,
                                   get_job_logs,
                                   get_prompt_image,
                                   handle_segmentation_prompt,
                                   confirm_segmentation_for_job,
                                   send_final_result_zip)

router = APIRouter()

@router.get("/jobs")
def get_jobs():
    try:
        return get_all_jobs()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/jobs/start")
def start_job(project_name: str = Form(...), files: List[UploadFile] = File(...)):
    try:
        response = start_new_job(project_name, files)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        response = get_job_details(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/jobs/{job_id}/logs", response_class=PlainTextResponse)
def get_logs(job_id: str):
    return get_job_logs(job_id)

@router.get("/jobs/{job_id}/segmentationPromptImage")
def get_segment_prompt_image(job_id: str):
    try:
        return get_prompt_image(job_id)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/jobs/{job_id}/segmentationPrompt")
def process_segmentation_prompt(job_id: str, point: dict):
    try:
        response = handle_segmentation_prompt(job_id, point)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/jobs/{job_id}/confirmSegmentation")
def confirm_segmentation(job_id: str):
    try:
        response = confirm_segmentation_for_job(job_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/jobs/{job_id}/downloadResult")
def download_result(job_id: str):
    return send_final_result_zip(job_id)