# Generated by Django 3.2.8 on 2021-10-19 12:59

from django.db import migrations, models
import uploader.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hashsum', models.CharField(max_length=50)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=20)),
                ('file_path', models.FileField(upload_to=uploader.models.media_file_name)),
            ],
        ),
    ]