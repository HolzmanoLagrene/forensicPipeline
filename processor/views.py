from celery import chain
from django.shortcuts import redirect, render

from processor.tasks import *


# Create your views here.

def show_logs(request,id,type):
    hashsum = UploadData.objects.get(id=id).hashsum
    with open(f"uploads/{hashsum}/logs/log2timeline.log") as in_:
        text = in_.read()
    c = {
        'text': text
    }
    return render(request, 'processor/logs.html', context=c)

def analyze_one(request, id):
    identifier = UploadData.objects.get(id=id).hashsum

    total_analysis_workflow = chain(
        run_log2timeline_background.si(identifier).on_error(log_error.s()),
        run_pinfo_background.si(identifier).on_error(log_error.s()),
        run_psort_background.si(identifier).on_error(log_error.s())
    )
    total_analysis_workflow.delay()
    return redirect('/')


def analyze_all(request):
    return redirect("/")
