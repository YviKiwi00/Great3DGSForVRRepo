from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import PlainTextResponse
from typing import List
from services.jobs_service import get_all_jobs, start_new_job, get_job_details, get_job_logs

router = APIRouter()

@router.get("/jobs")
def get_jobs():
    return get_all_jobs()

@router.post("/jobs/start")
async def start_job(
    projectName: str = Form(...),
    files: List[UploadFile] = File(...)
):
    job_id = await start_new_job(projectName, files)
    return {"job_id": job_id}

@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    return get_job_details(job_id)

@router.get("/jobs/{job_id}/logs", response_class=PlainTextResponse)
def get_logs(job_id: str):
    return get_job_logs(job_id)