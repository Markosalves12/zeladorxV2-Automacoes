from django.db import models
from utils.utils import generate_id_random
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from utils.utils import resize_image


class AreaLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    nome = models.CharField(
        blank=False,
        null=False,
        max_length=100,
    )

    dimensao = models.FloatField(
        blank=True,
        null=True
    )

    servico = models.ForeignKey(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='servicocatalogoservicolimpezapredial'
    )

    localidade = models.ForeignKey(
        to=LocalidadeLimpezaPredial,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='localidadelimpezapredial'
    )

    foto = models.ImageField(
        upload_to="areaslimpezapredial/%Y/%m/%d/",
        blank=True,
        max_length=2000
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

    # class Meta:
    #     unique_together = ('nome', 'localidade')


    def save(self, *args, **kwargs):
        if self.foto:
            self.foto = resize_image(self.foto, max_width=500)

        super(AreaLimpezaPredial, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} | {self.localidade}'