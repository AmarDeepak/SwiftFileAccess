from django.db import models
import uuid
from common.models import BaseTimestampedModel
import os
# Create your models here.

class Directory(BaseTimestampedModel):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

def get_upload_path(instance, filename):
    print(os.path.join(str(instance.directory.uid), filename))
    # import pdb; pdb.set_trace()
    return os.path.join('file/static/',str(instance.directory.uid), filename)

class Files(BaseTimestampedModel):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)