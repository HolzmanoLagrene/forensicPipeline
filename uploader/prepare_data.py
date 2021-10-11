import numpy as np
import pandas as pd
from pandas import json_normalize
import json
import html

from .models import DataPoint

data_path = "/home/treebeard/Projects/demoPage/uploader/static/uploader/test_data.json"

def load_data():
    json_ = json.load(open(data_path))
    data = []
    for k,v in json_.items():
        norm_ = json_normalize(v).to_dict("rows")[0]
        data.append(norm_)
    return pd.DataFrame(data)

def clean_data(df):
    df = df[[col for col in df.columns if not "__" in col]]
    df = df.replace("-",np.nan)
    df = df.dropna(axis=1,how="all").fillna("")
    df = df.applymap(str).applymap(html.escape)
    return df

def filter_data(df, query_param):
    return df

def sort_data(df, sort_param,order_param):
    return df

def slice_data(df, offset, limit):
    return df

def generate_output(df):
    data = df.to_dict("rows")
    return  {
        "totalCount":len(df),
        "totalNotFiltered":len(df),
        "rows":data
    }

def store(search_param,sort_param,order_param,offset_param,limit_param):
    df = load_data()
    df = clean_data(df)
    df = filter_data(df, search_param)
    df = sort_data(df, sort_param,order_param)
    df = slice_data(df, offset_param,limit_param)
    entries =  df.to_dict("rows")
    for entry in entries:
        DataPoint.objects.create(data=entry)

