# custom mixin
from django.db import models
from django.utils import timezone


class DatesModelMixin(models.Model):

    created = models.DateTimeField(
        verbose_name="Дата создания"
    )
    updated = models.DateTimeField(
        verbose_name="Дата последнего обновления"
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
