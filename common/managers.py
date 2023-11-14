from django.db import models
from django.db.models.manager import BaseManager
from django.utils import timezone

class TimestampedQueryset(models.QuerySet):
    def update(self, **kwargs):
        if "modified" not in kwargs.keys():
            kwargs["modified"] = timezone.now()
        super().update(**kwargs)

class TimestampedManager(BaseManager.from_queryset(TimestampedQueryset)):
    use_in_migrations = True

    def __iter__(self):
        yield from self.all()