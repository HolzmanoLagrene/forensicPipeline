from celery.utils.log import get_task_logger

from forensicPipeline.celery import app
from plaso_api.DockerHandler import *
from uploader.models import UploadData

logger = get_task_logger(__name__)


@app.task(name="log2timeline")
def run_log2timeline_background(id):
    UploadData.objects.filter(hashsum=id).update(status="processing_log2timeline")
    status_code = run_log2timeline(id)
    if status_code == 0:
        UploadData.objects.filter(hashsum=id).update(status="success_log2timeline")
    else:
        logger.info(status_code)
        UploadData.objects.filter(hashsum=id).update(status="failed_log2timeline")


@app.task
def log_error(request, exc, traceback):
    print('THIS IS A PROVOCED ERROR')


@app.task(name="pinfo")
def run_pinfo_background(id):
    UploadData.objects.filter(hashsum=id).update(status="processing_pinfo")
    status_code = run_pinfo(id)
    UploadData.objects.filter(hashsum=id).update(status="success_pinfo")
    if status_code == 0:
        UploadData.objects.filter(hashsum=id).update(status="success_pinfo")
    else:
        logger.info(status_code)
        UploadData.objects.filter(hashsum=id).update(status="failed_pinfo")


@app.task(name="psort")
def run_psort_background(id):
    UploadData.objects.filter(hashsum=id).update(status="processing_psort")
    status_code = run_psort(id)
    if status_code == 0:
        UploadData.objects.filter(hashsum=id).update(status="success_psort")
    else:
        logger.info(status_code)
        UploadData.objects.filter(hashsum=id).update(status="failed_psort")
