import hashlib
import os
from datetime import datetime

from django.db import models


def media_file_name(instance, filename):
    h = instance.hashsum
    return os.path.join(f'{h}/evidence/{filename}')


class UploadData(models.Model):
    id = models.AutoField(primary_key=True)
    hashsum = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    file_path = models.FileField(upload_to=media_file_name)

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.file_path.chunks():
                md5.update(chunk)
            self.hashsum = md5.hexdigest()
        if not UploadData.objects.filter(hashsum=self.hashsum).exists():
            super(UploadData, self).save(*args, **kwargs)
        else:
            UploadData.objects.filter(hashsum=self.hashsum).update(added=datetime.now(),status="success_data_upload")
