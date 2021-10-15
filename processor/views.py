from celery import chain, group
from django.shortcuts import redirect

from processor.tasks import *


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
    identifiers = [identifier.hashsum for identifier in UploadData.objects.all()]
    chains = []
    for identifier in identifiers:
        chains.append(
            chain(
                run_log2timeline_background.si(identifier).on_error(log_error.s()),
                run_pinfo_background.si(identifier).on_error(log_error.s()),
                run_psort_background.si(identifier).on_error(log_error.s())
            )
        )
    all_workflows = group(
        *chains
    )
    all_workflows.delay()
    return redirect("/")
