"""forensicPipeline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from logviewer import views as logviewer_views
from notebook import views as notebook_views
from processor import views as processor_views
from uploader import views as uploader_views

urlpatterns = [
    path('', uploader_views.upload_page, name=""),
    path('upload', uploader_views.save_file),
    path('removeSingleId=<int:id>', uploader_views.remove_one, name="id"),
    path('removeAll', uploader_views.remove_all),
    path('analyzeSingleId=<int:id>', processor_views.analyze_one, name="id"),
    path('analyzeAll', processor_views.analyze_all),
    path('showLogsOf=<int:id>Type=<str:type>', logviewer_views.show_logs),
    path('openNotebook=<int:id>', notebook_views.open_notebook),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
