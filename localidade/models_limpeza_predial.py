from django.db import models
from unidade.models import Unidade
from utils.utils import generate_id_random


class LocalidadeLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=50,
    )

    lat_med = models.FloatField(
        blank=False,
        null=False,
    )

    long_med = models.FloatField(
        blank=False,
        null=False,
    )

    unidade = models.ForeignKey(
        to=Unidade,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="unidadelocalidadelimpezapredial",
    )

    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
    ]

    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Mobilizado'
    )

    class Meta:
        unique_together = ('nome', 'unidade', )

    def __str__(self):
        return f'{self.nome} -- {self.unidade}'