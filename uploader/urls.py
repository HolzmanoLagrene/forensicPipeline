from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = 'uploader'
urlpatterns = [
    path('', views.upload_page,name=""),
    path('upload', views.save_file),
    path('removeSingleId=<int:id>',views.remove_one,name="id"),
    path('removeAll', views.remove_all),
    path('analyzeSingleId=<int:id>', views.analyze_one, name="id"),
    path('analyzeAll', views.analyze_all),
]
