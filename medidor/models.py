from django.db import models
from utils.utils import generate_id_random


class DocsFromProcess(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    document = models.FileField(
        upload_to="documents/%Y/%m/%d/",
        blank=True,
        max_length=2000
    )

    def __str__(self):
        return self.id_random


