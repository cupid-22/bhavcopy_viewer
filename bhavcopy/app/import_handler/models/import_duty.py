from django.db import models

from bhavcopy.app.standard_util.models import CoreModel


class ImportDuty(CoreModel):
    name = models.TextField(blank=True)
    other_field1 = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
