from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from services.jobs_service import start_new_job

router = APIRouter()

@router.post("/jobs/start")
async def start_job(
    projectName: str = Form(...),
    files: List[UploadFile] = File(...)
):
    job_id = await start_new_job(projectName, files)
    return {"job_id": job_id}