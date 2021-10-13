from django.shortcuts import render, redirect

# Create your views here.
from logviewer.utils import get_log2timeline_data, get_psort_data, get_pinfo_data


def show_logs(request,id,type):
    if type == "log2timeline":
        data = get_log2timeline_data(id)
        c = {
            'data': data,
            'title':"Log2timeline"
        }
        return render(request, 'logviewer/logs_log2timeline.html', context=c)
    elif type == "pinfo":
        data = get_pinfo_data(id)
        c = {
            'html': data,
            'title':"Extraction Information"
        }
        return render(request, 'logviewer/logs_pinfo.html', context=c)
    elif type == "psort":
        data = get_psort_data(id)
        c = {
            'data': data,
            'title':"FileUpload"
        }
        return render(request, 'logviewer/logs_log2timeline.html', context=c)
    else:
        return redirect("/")