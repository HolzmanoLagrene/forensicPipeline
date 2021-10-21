from celery.utils.log import get_task_logger
from celery.states import FAILURE
from celery.exceptions import Ignore

from forensicPipeline.celery import app
from docker_api.DockerHandler import *
from uploader.models import UploadData

logger = get_task_logger(__name__)


@app.task(name="log2timeline", bind=True)
def run_log2timeline_background(self, evidence_id):
    UploadData.objects.filter(hashsum=evidence_id).update(status="processing_log2timeline")
    status_code = run_log2timeline(evidence_id)
    if status_code == 0:
        UploadData.objects.filter(hashsum=evidence_id).update(status="success_log2timeline")
    else:
        logger.info(status_code)
        UploadData.objects.filter(hashsum=evidence_id).update(status="failed_log2timeline")
        self.update_state(state=FAILURE, meta=f'Error: {status_code}')

        raise Ignore()


@app.task
def log_error(request, exc, traceback):
    print('THIS IS A PROVOCED ERROR')


@app.task(name="pinfo", bind=True)
def run_pinfo_background(self, evidence_id):
    UploadData.objects.filter(hashsum=evidence_id).update(status="processing_pinfo")
    status_code = run_pinfo(evidence_id)
    UploadData.objects.filter(hashsum=evidence_id).update(status="success_pinfo")
    if status_code == 0:
        UploadData.objects.filter(hashsum=evidence_id).update(status="success_pinfo")
    else:
        logger.info(status_code)
        UploadData.objects.filter(hashsum=evidence_id).update(status="failed_pinfo")
        self.update_state(state=FAILURE, meta=f'Error: {status_code}')

        raise Ignore()


@app.task(name="psort", bind=True)
def run_psort_background(self, evidence_id):
    UploadData.objects.filter(hashsum=evidence_id).update(status="processing_psort")
    status_code = run_psort(evidence_id)
    if status_code == 0:
        UploadData.objects.filter(hashsum=evidence_id).update(status="success_psort")
    else:
        logger.info(status_code)
        UploadData.objects.filter(hashsum=evidence_id).update(status="failed_psort")
        self.update_state(state=FAILURE, meta=f'Error: {status_code}')

        raise Ignore()
