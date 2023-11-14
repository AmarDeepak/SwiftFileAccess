import json

from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from common.managers import TimestampedManager
import logging
from django.core import serializers
# Create your models here.


logger = logging.getLogger(__name__)

class BaseTimestampedModel(models.Model):
    created = AutoCreatedField("created", db_index=True)
    modified = AutoLastModifiedField("modified", db_index=True)

    objects = TimestampedManager()

    class Meta:
        abstract = True

    def _log(self, created):
        if created:
            logger.info(
                "Model Created",
                extra={"json": self.json(), "class": self.__class__.__name__},
            )
        else:
            logger.info(
                "Model Updated",
                extra={"json":self.json(), "class": self.__class__.__name__},
            )
    def json(self):
        return json.loads(serializers.serialize("json",[self]))[0]

    def save(self, *args, **kwargs):
        created = self.pk is None

        super().save(*args, **kwargs)

        try:
            self._log(created)
        except Exception:
            logger.exception("unable to log change", extra={"class": self.__class__})