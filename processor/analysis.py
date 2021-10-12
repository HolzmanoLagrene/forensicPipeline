from plaso_api.DockerHandler import DockerHandler
from uploader.models import UploadData


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