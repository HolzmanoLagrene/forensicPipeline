from django.db import models


class UploadData(models.Model):
    id = models.AutoField(primary_key=True)
    hashsum = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    size = models.CharField(max_length=20)

