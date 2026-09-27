from django.db import models
from utils.utils import generate_id_random, resize_image
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado

# Create your models here.
class CheckListJardinagem(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    servico_agendado = models.ForeignKey(
        to=ServicoJardinagemAgendado,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='rServicoAgendadosToChecklist'
    )

    descricao = models.CharField(
        max_length=255
    )

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Concluído', 'Concluído'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendente'
    )

    foto_comprovacao = models.ImageField(
        upload_to='checklist_jardinagem/%Y/%m/%d/',
        blank=True,
        null=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if self.foto_comprovacao:
            self.foto_comprovacao = resize_image(self.foto_comprovacao, max_width=500)

        super(CheckListJardinagem, self).save(*args, **kwargs)

    def __str__(self):
        return f"Checklist: {self.descricao} ({self.get_status_display()})"


class CheckListLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    servico_agendado = models.ForeignKey(
        to=ServicoLimpezaPredialAgendado,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='rTerrenoAreas'
    )

    descricao = models.CharField(
        max_length=255
    )

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Concluído', 'Concluído'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendente'
    )

    foto_comprovacao = models.ImageField(
        upload_to='checklist_limpeza_predial/%Y/%m/%d/',
        blank=True,
        null=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if self.foto_comprovacao:
            self.foto_comprovacao = resize_image(self.foto_comprovacao, max_width=500)

        super(CheckListLimpezaPredial, self).save(*args, **kwargs)

    def __str__(self):
        return f"Checklist: {self.descricao} ({self.get_status_display()})"