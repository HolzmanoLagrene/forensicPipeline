# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from notebook.tasks import run_notebook_background
from docker_api import DockerHandler
from uploader.models import UploadData


def open_notebook(request, id):
    identifier = UploadData.objects.get(id=id).hashsum
    run_notebook_background.s(identifier).delay()
    return HttpResponseRedirect('http://127.0.0.1:8888')
