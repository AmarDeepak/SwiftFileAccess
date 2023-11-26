from django.db import models
import uuid
from common.models import BaseTimestampedModel
import os
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User
class Directory(BaseTimestampedModel):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

def get_upload_path(instance, filename):
    return os.path.join(str(instance.directory.uid), filename)

class Files(BaseTimestampedModel):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=200)
