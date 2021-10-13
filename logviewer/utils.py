import datetime
import glob
import json
import os.path
import re

from forensicPipeline.settings import MEDIA_ROOT
import pandas as pd
from uploader.models import UploadData
from json2html import *

def get_log2timeline_data(id):
    identifier = UploadData.objects.get(id=id).hashsum
    evidence_path = os.path.join(MEDIA_ROOT,identifier,"logs")
    data = []
    for file in glob.glob(f"{evidence_path}/*log2timeline*.log"):
        with open(file, "r") as log_:
            for dataline in log_.readlines():
                if dataline.endswith("Checking for pending tasks\n"):
                    continue
                year,month,day,hour,minute,second,msecond = re.match("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})", dataline).groups()
                datetime_ = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second), microsecond=int(msecond) * 1000)
                log_info = re.sub("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})", "", dataline)
                log_info = log_info.rstrip("\n").lstrip(" ")
                data.append({
                    "timestamp":datetime_,
                    "log_info":log_info
                })
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp")
    data_dict = df.to_dict(orient="records")
    return data_dict

def get_pinfo_data(id):
    identifier = UploadData.objects.get(id=id).hashsum
    evidence_path = os.path.join(MEDIA_ROOT,identifier,"plaso","pinfo.json")
    with open(evidence_path,"r") as in_:
        data = json.load(in_)
    del data["sessions"]["session"]["enabled_parser_names"]
    return json2html.convert(json=data)


def get_psort_data(id):
    identifier = UploadData.objects.get(id=id).hashsum
    evidence_path = os.path.join(MEDIA_ROOT,identifier,"logs","psort.log")
    data = []
    last_datetime = None
    with open(evidence_path, "r") as log_:
        for dataline in log_.readlines():
            try:
                year,month,day,hour,minute,second,msecond = re.match("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})", dataline).groups()
                datetime_ = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second), microsecond=int(msecond) * 1000)
                log_info = re.sub("([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{3})", "", dataline)
                log_info = log_info.rstrip("\n").lstrip(" ")
                last_datetime = datetime_
            except AttributeError as e:
                datetime_ =last_datetime
                log_info = dataline
            data.append({
                "timestamp":datetime_,
                "log_info":log_info
            })
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp")
    data_dict = df.to_dict(orient="records")
    return data_dict