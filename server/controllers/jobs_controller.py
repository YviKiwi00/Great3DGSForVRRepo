from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, FileResponse
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
    return get_all_jobs()

@router.post("/jobs/start")
async def start_job(
    project_name: str = Form(...),
    files: List[UploadFile] = File(...)
):
    job_id = await start_new_job(project_name, files)
    return {"job_id": job_id}

@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    return get_job_details(job_id)

@router.get("/jobs/{job_id}/logs", response_class=PlainTextResponse)
def get_logs(job_id: str):
    return get_job_logs(job_id)

@router.get("/jobs/{job_id}/segmentationPromptImage")
def get_segment_prompt_image(job_id: str):
    return get_prompt_image(job_id)

@router.post("/jobs/{job_id}/segmentationPrompt")
def process_segmentation_prompt(job_id: str, point: dict):
    return handle_segmentation_prompt(job_id, point)

@router.post("/jobs/{job_id}/confirmSegmentation")
def confirm_segmentation(job_id: str):
    return confirm_segmentation_for_job(job_id)

@router.get("/jobs/{job_id}/downloadResult")
def download_result(job_id: str):
    return send_final_result_zip(job_id)