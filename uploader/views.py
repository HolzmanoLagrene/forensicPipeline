from django.core.management import call_command
from django.shortcuts import render, redirect

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


def save_file(request):
    if request.method == 'POST':
        for file in request.FILES.values():
            upload_data = UploadData(status="ready", name=file.name, size=sizeof_fmt(file.size), file_path=file)
            upload_data.save()
    return redirect('/')


def remove_one(request, id):
    file_object = UploadData.objects.get(id=id)
    file_object.delete()
    call_command('cleanup')
    return redirect('/')


def remove_all(request):
    UploadData.objects.all().delete()
    call_command('cleanup')
    return redirect('/')
