import asyncio
import glob
import hashlib
import os
import shutil
from datetime import datetime

from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

from plaso_api.DockerHandler import DockerHandler
from .models import UploadData


def upload_page(request):
    files = UploadData.objects.order_by('added')

    c = {
        'files': files
    }
    return render(request, 'uploader/index.html', context=c)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def calculate_hash(file):
    md5_object = hashlib.md5()
    block_size = 8 * md5_object.block_size

    chunk = file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = file.read(block_size)

    md5_hash = md5_object.hexdigest()
    file.file.seek(0)
    return md5_hash


def save_file(request):
    if request.method == 'POST':
        for file in request.FILES.values():
            file_hash = calculate_hash(file)
            if not os.path.isdir(f"uploads/{file_hash}"):
                os.makedirs(f"uploads/{file_hash}/evidences")
                default_storage.save(f"{file_hash}/evidences/{file.name}", file)
                UploadData.objects.create(hashsum=file_hash, status="ready", name=file.name, size=sizeof_fmt(file.size))
            else:
                UploadData.objects.filter(hashsum=file_hash).update(added=datetime.now())
            UploadData.objects.filter(hashsum=file_hash).update(status="success_data_upload")
    return redirect('/')


def remove_one(request, id):
    file_object = UploadData.objects.get(id=id)
    file_object.delete()
    # TODO: Work with file fields here !! A base command or signals https://www.algotech.solutions/blog/python/deleting-unused-django-media-files/
    for dir in glob.glob(f"uploads/{file_object.hashsum}/*"):
        shutil.rmtree(dir)
    default_storage.delete(f"{file_object.hashsum}")
    return redirect('/')


def remove_all(request):
    files = UploadData.objects.order_by('added')
    for file_object in files:
        for dir in glob.glob(f"uploads/{file_object.hashsum}/*"):
            shutil.rmtree(dir)
        default_storage.delete(f"{file_object.hashsum}")
        file_object.delete()
    return redirect('/')


def analyze_one(request, id):
    d = ["success_data_upload",
         "processing_log2timeline",
         "success_log2timeline",
         "failed_log2timeline",
         "processing_pinfo",
         "success_pinfo",
         "failed_pinfo",
         "processing_psort",
         "success_psort",
         "failed_psort",
         "error"
         ]
    file_object = UploadData.objects.get(id=id)
    UploadData.objects.filter(id=id).update(status="processing_log2timeline")
    dh = DockerHandler()
    result = asyncio.run(dh.run_log2timeline(file_object.hashsum))
    if result == 0:
        UploadData.objects.filter(id=id).update(status="success_log2timeline")
    else:
        UploadData.objects.filter(id=id).update(status="failed_log2timeline")

    UploadData.objects.filter(id=id).update(status="processing_pinfo")
    result = asyncio.run(dh.run_pinfo(file_object.hashsum))
    if result == 0:
        UploadData.objects.filter(id=id).update(status="success_pinfo")
    else:
        UploadData.objects.filter(id=id).update(status="failed_pinfo")

    UploadData.objects.filter(id=id).update(status="processing_psort")
    result = asyncio.run(dh.run_psort(file_object.hashsum))
    if result == 0:
        UploadData.objects.filter(id=id).update(status="success_psort")
    else:
        UploadData.objects.filter(id=id).update(status="failed_psort")
    return redirect('/')


def analyze_all(request):
    return redirect("/")
