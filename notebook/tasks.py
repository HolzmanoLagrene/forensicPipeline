from celery.utils.log import get_task_logger

from forensicPipeline.celery import app
from plaso_api.DockerHandler import run_jupyter_notebook
from uploader.models import UploadData

logger = get_task_logger(__name__)


@app.task(name="notebook")
def run_notebook_background(id):
    status_code = run_jupyter_notebook(id)
